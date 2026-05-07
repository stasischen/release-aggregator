#!/usr/bin/env python3
"""Validate runtime content contracts that frontend code is allowed to read.

This intentionally uses the Python standard library only so it can run in CI
before project dependencies are installed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


LL_CORE_FILES = [
    "sources_index.json",
    "sentences.json",
    "knowledge.json",
    "topics.json",
    "vocab_sets.json",
    "links.json",
]

LL_I18N_FILES = [
    "sources.json",
    "sentences.json",
    "knowledge.json",
    "topics.json",
    "vocab_sets.json",
]

DEPRECATED_LEARNING_LIBRARY_ALIASES = {
    "knowledge_index.json",
    "sentences_index.json",
    "topics_index.json",
    "vocab_sets_index.json",
}

DICTIONARY_I18N_FORBIDDEN_FILES = {
    "mapping.json",
    "mapping_v2.json",
    "surface_candidates.v1.json",
    "surface_mapping_v2.json",
}

DICTIONARY_RESOLVER_FILES = [
    "surface_candidates.v1.json",
]

DICTIONARY_CORE_FORBIDDEN_DISPLAY_KEYS = {
    "definitions",
    "translation",
    "meaning",
    "description",
    "gloss",
    "localized",
    "i18n",
}

DICTIONARY_LEARNER_LOCALE_KEYS = {
    "zh",
    "zh_tw",
    "zh-tw",
    "zh_hant",
    "zh-hant",
}

LL_SIDECAR_SOURCE_TYPES = {
    "shared_bank",
    "video",
    "dialogue",
    "article",
    "knowledge_collection",
}

LL_SIDECAR_STATUSES = {
    "active",
    "needs_review",
    "deprecated",
}

LL_TURN_BASED_SOURCE_TYPES = {
    "video",
    "dialogue",
    "article",
}

LL_LEGACY_BRIDGE_MARKERS = (
    "_load_legacy_source_i18n",
    "_load_legacy_learning_library_i18n",
    "content/i18n/<locale>/learning_library",
    "content/i18n/<locale>/video",
    "content/i18n/<locale>/dialogue",
)

LL_LEGACY_BRIDGE_FLAG_MARKERS = (
    "allow_legacy_i18n_bridge",
    "allow_legacy_learning_library_i18n",
    "enable_legacy_i18n_bridge",
    "--allow-legacy-i18n-bridge",
    "ALLOW_LEGACY_I18N_BRIDGE",
)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json: {path}: {exc}") from None


def _require_object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _require_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    return value


def _check_exact_file_set(actual: Iterable[Any], expected: list[str], label: str, errors: list[str]) -> list[str]:
    values = [item for item in actual if isinstance(item, str)]
    non_strings = [item for item in actual if not isinstance(item, str)]
    if non_strings:
        errors.append(f"{label} contains non-string entries: {non_strings!r}")

    actual_set = set(values)
    expected_set = set(expected)
    missing = sorted(expected_set - actual_set)
    extra = sorted(actual_set - expected_set)
    deprecated = sorted(actual_set & DEPRECATED_LEARNING_LIBRARY_ALIASES)

    if missing:
        errors.append(f"{label} missing required files: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} contains unexpected files: {', '.join(extra)}")
    if deprecated:
        errors.append(f"{label} contains deprecated aliases: {', '.join(deprecated)}")
    return values


def _non_empty_translation_count(payload: Any) -> int:
    count = 0
    if isinstance(payload, dict):
        translation = payload.get("translation")
        if isinstance(translation, str) and translation.strip():
            count += 1
        for value in payload.values():
            count += _non_empty_translation_count(value)
    elif isinstance(payload, list):
        for item in payload:
            count += _non_empty_translation_count(item)
    return count


def _require_non_empty_string(value: Any, label: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
        return ""
    return value


def validate_learning_library_manifest(
    manifest_path: Path,
    *,
    require_locale: str | None = None,
    min_sentence_translations: int = 0,
) -> list[str]:
    errors: list[str] = []

    try:
        manifest = _require_object(load_json(manifest_path), str(manifest_path), errors)
    except ValueError as exc:
        return [str(exc)]

    lang = manifest.get("lang")
    if not isinstance(lang, str) or not lang:
        errors.append("learning library manifest must declare non-empty lang")

    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        errors.append("learning library manifest must declare non-empty version")

    modules = _require_list(manifest.get("modules"), "modules", errors)
    module_set = {item for item in modules if isinstance(item, str)}
    for required_module in ("core", "i18n"):
        if required_module not in module_set:
            errors.append(f"modules missing required module: {required_module}")

    files = _require_object(manifest.get("files"), "files", errors)
    core_files = _check_exact_file_set(
        _require_list(files.get("core"), "files.core", errors),
        LL_CORE_FILES,
        "files.core",
        errors,
    )

    i18n = _require_object(files.get("i18n"), "files.i18n", errors)
    if require_locale and require_locale not in i18n:
        errors.append(f"files.i18n missing required locale: {require_locale}")
    if not i18n:
        errors.append("files.i18n must declare at least one locale")

    manifest_root = manifest_path.parent
    for filename in core_files:
        if not (manifest_root / "core" / filename).is_file():
            errors.append(f"files.core references missing artifact: core/{filename}")

    for locale, entries in i18n.items():
        if not isinstance(locale, str) or not locale:
            errors.append(f"files.i18n has invalid locale key: {locale!r}")
            continue
        locale_files = _check_exact_file_set(
            _require_list(entries, f"files.i18n.{locale}", errors),
            LL_I18N_FILES,
            f"files.i18n.{locale}",
            errors,
        )
        for filename in locale_files:
            if not (manifest_root / "i18n" / locale / filename).is_file():
                errors.append(f"files.i18n.{locale} references missing artifact: i18n/{locale}/{filename}")

    if min_sentence_translations > 0:
        coverage_locale = require_locale or next((key for key in i18n if isinstance(key, str)), None)
        if coverage_locale:
            sentence_path = manifest_root / "i18n" / coverage_locale / "sentences.json"
            try:
                translation_count = _non_empty_translation_count(load_json(sentence_path))
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if translation_count < min_sentence_translations:
                    errors.append(
                        "sentence i18n coverage below baseline: "
                        f"{translation_count} < {min_sentence_translations} ({coverage_locale})"
                    )

    return errors


def validate_learning_library_i18n_sidecar_manifest(
    manifest_path: Path,
    *,
    min_sentence_coverage: float = 0.0,
) -> list[str]:
    errors: list[str] = []

    try:
        manifest = _require_object(load_json(manifest_path), str(manifest_path), errors)
    except ValueError as exc:
        return [str(exc)]

    schema_version = _require_non_empty_string(manifest.get("schema_version"), "schema_version", errors)
    if schema_version and schema_version != "learning-library-i18n-manifest-v1":
        errors.append(f"schema_version must be learning-library-i18n-manifest-v1: {schema_version}")

    study_language = _require_non_empty_string(manifest.get("study_language"), "study_language", errors)
    learner_language = _require_non_empty_string(manifest.get("learner_language"), "learner_language", errors)

    files = _require_object(manifest.get("files"), "files", errors)
    required_files = {
        "sources": "sources.json",
        "sentences": "sentences.json",
        "knowledge": "knowledge.json",
    }
    root = manifest_path.parent
    resolved_files: dict[str, Path] = {}
    for key, expected_name in required_files.items():
        filename = files.get(key)
        if filename != expected_name:
            errors.append(f"files.{key} must be {expected_name}")
            continue
        path = root / expected_name
        if not path.is_file():
            errors.append(f"files.{key} references missing sidecar: {expected_name}")
        else:
            resolved_files[key] = path

    if errors:
        return errors

    sources = _require_object(load_json(resolved_files["sources"]), str(resolved_files["sources"]), errors)
    sentences = _require_object(load_json(resolved_files["sentences"]), str(resolved_files["sentences"]), errors)
    knowledge = _require_object(load_json(resolved_files["knowledge"]), str(resolved_files["knowledge"]), errors)

    for label, payload, expected_version in (
        ("sources", sources, "learning-library-i18n-sources-v1"),
        ("sentences", sentences, "learning-library-i18n-sentences-v1"),
        ("knowledge", knowledge, "learning-library-i18n-knowledge-v1"),
    ):
        value = _require_non_empty_string(payload.get("schema_version"), f"{label}.schema_version", errors)
        if value and value != expected_version:
            errors.append(f"{label}.schema_version must be {expected_version}: {value}")
        if payload.get("study_language") != study_language:
            errors.append(f"{label}.study_language must match manifest study_language")
        if payload.get("learner_language") != learner_language:
            errors.append(f"{label}.learner_language must match manifest learner_language")

    source_entries = _require_object(sources.get("entries"), "sources.entries", errors)
    sentence_entries = _require_object(sentences.get("entries"), "sentences.entries", errors)
    knowledge_entries = _require_object(knowledge.get("entries"), "knowledge.entries", errors)

    for source_id, row in source_entries.items():
        label = f"sources.entries.{source_id}"
        source = _require_object(row, label, errors)
        if source.get("source_id") != source_id:
            errors.append(f"{label}.source_id must match entry key")
        source_type = source.get("source_type")
        if source_type not in LL_SIDECAR_SOURCE_TYPES:
            errors.append(f"{label}.source_type is invalid: {source_type!r}")
        _require_non_empty_string(source.get("title"), f"{label}.title", errors)
        if source.get("status") not in LL_SIDECAR_STATUSES:
            errors.append(f"{label}.status is invalid: {source.get('status')!r}")
        _require_list(source.get("source_refs"), f"{label}.source_refs", errors)

    total_sentence_rows = 0
    translated_sentence_rows = 0
    for source_id, block_value in sentence_entries.items():
        block_label = f"sentences.entries.{source_id}"
        block = _require_object(block_value, block_label, errors)
        if block.get("source_id") != source_id:
            errors.append(f"{block_label}.source_id must match entry key")
        source_type = block.get("source_type")
        if source_type not in LL_SIDECAR_SOURCE_TYPES:
            errors.append(f"{block_label}.source_type is invalid: {source_type!r}")
        rows = _require_object(block.get("sentences"), f"{block_label}.sentences", errors)
        for sentence_id, row_value in rows.items():
            row_label = f"{block_label}.sentences.{sentence_id}"
            row = _require_object(row_value, row_label, errors)
            total_sentence_rows += 1
            if row.get("sentence_id") != sentence_id:
                errors.append(f"{row_label}.sentence_id must match entry key")
            status = row.get("status")
            if status not in LL_SIDECAR_STATUSES:
                errors.append(f"{row_label}.status is invalid: {status!r}")
            translation = row.get("translation")
            has_translation = isinstance(translation, str) and bool(translation.strip())
            if has_translation:
                translated_sentence_rows += 1
            if status == "active" and not has_translation:
                errors.append(f"{row_label}.translation must be non-empty when status is active")
            _require_list(row.get("source_refs"), f"{row_label}.source_refs", errors)
            if source_type in LL_TURN_BASED_SOURCE_TYPES:
                _require_non_empty_string(row.get("turn_id"), f"{row_label}.turn_id", errors)

    if total_sentence_rows == 0:
        errors.append("sentences.entries must contain at least one sentence row")
    elif min_sentence_coverage > 0:
        coverage = translated_sentence_rows / total_sentence_rows
        if coverage < min_sentence_coverage:
            errors.append(
                "sidecar sentence i18n coverage below baseline: "
                f"{translated_sentence_rows}/{total_sentence_rows} = {coverage:.2%} < {min_sentence_coverage:.2%}"
            )

    for knowledge_id, row_value in knowledge_entries.items():
        row_label = f"knowledge.entries.{knowledge_id}"
        row = _require_object(row_value, row_label, errors)
        if row.get("knowledge_id") != knowledge_id:
            errors.append(f"{row_label}.knowledge_id must match entry key")
        _require_non_empty_string(row.get("title"), f"{row_label}.title", errors)
        if row.get("status") not in LL_SIDECAR_STATUSES:
            errors.append(f"{row_label}.status is invalid: {row.get('status')!r}")
        _require_list(row.get("source_refs"), f"{row_label}.source_refs", errors)

    return errors


def validate_package_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = _require_object(load_json(manifest_path), str(manifest_path), errors)
    except ValueError as exc:
        return [str(exc)]

    for field in ("version", "target", "learner_lang"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"package manifest must declare non-empty {field}")

    modules = _require_object(manifest.get("modules"), "modules", errors)
    dictionary = modules.get("dictionary")
    if dictionary is not None:
        dictionary_module = _require_object(dictionary, "modules.dictionary", errors)
        core_path = dictionary_module.get("core")
        if not isinstance(core_path, str) or not core_path.strip():
            errors.append("modules.dictionary.core must be a non-empty string")
        else:
            resolved_core_path = (manifest_path.parent / "core" / core_path).resolve()
            if not resolved_core_path.is_file():
                errors.append(f"modules.dictionary.core references missing artifact: core/{core_path}")
            else:
                errors.extend(validate_dictionary_core_payload(resolved_core_path))

        dictionary_i18n = _require_object(dictionary_module.get("i18n"), "modules.dictionary.i18n", errors)
        if not dictionary_i18n:
            errors.append("modules.dictionary.i18n must declare at least one locale")
        for locale, entries in dictionary_i18n.items():
            if not isinstance(locale, str) or not locale:
                errors.append(f"modules.dictionary.i18n has invalid locale key: {locale!r}")
                continue
            paths = _require_list(entries, f"modules.dictionary.i18n.{locale}", errors)
            for raw_path in paths:
                if not isinstance(raw_path, str):
                    continue
                filename = Path(raw_path).name
                if filename in DICTIONARY_I18N_FORBIDDEN_FILES:
                    errors.append(f"modules.dictionary.i18n.{locale} references resolver/non-i18n file: {raw_path}")
                if not (manifest_path.parent / "i18n" / raw_path).resolve().is_file():
                    errors.append(f"modules.dictionary.i18n.{locale} references missing artifact: i18n/{raw_path}")

        resolver_paths = _check_exact_file_set(
            _require_list(dictionary_module.get("resolver"), "modules.dictionary.resolver", errors),
            DICTIONARY_RESOLVER_FILES,
            "modules.dictionary.resolver",
            errors,
        )
        for raw_path in resolver_paths:
            if not (manifest_path.parent / "resolver" / raw_path).resolve().is_file():
                errors.append(f"modules.dictionary.resolver references missing artifact: resolver/{raw_path}")

    learning_library = modules.get("learning_library")
    if learning_library is None:
        return errors

    ll_module = _require_object(learning_library, "modules.learning_library", errors)
    for bucket in ("core", "i18n"):
        paths = _require_list(ll_module.get(bucket), f"modules.learning_library.{bucket}", errors)
        for raw_path in paths:
            if not isinstance(raw_path, str):
                continue
            name = Path(raw_path).name
            if name in DEPRECATED_LEARNING_LIBRARY_ALIASES:
                errors.append(f"modules.learning_library.{bucket} references deprecated alias: {raw_path}")
            if not (manifest_path.parent / raw_path).resolve().is_file():
                errors.append(f"modules.learning_library.{bucket} references missing artifact: {raw_path}")

    return errors


def validate_dictionary_core_payload(core_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = _require_object(load_json(core_path), str(core_path), errors)
    except ValueError as exc:
        return [str(exc)]

    atoms = _require_list(payload.get("atoms"), "dictionary_core.atoms", errors)
    for index, atom_value in enumerate(atoms):
        if not isinstance(atom_value, dict):
            errors.append(f"dictionary_core.atoms[{index}] must be an object")
            continue
        atom_id = str(atom_value.get("atom_id") or atom_value.get("id") or f"#{index}")
        for key in atom_value:
            if key in DICTIONARY_CORE_FORBIDDEN_DISPLAY_KEYS:
                errors.append(f"dictionary core atom {atom_id} contains forbidden display field: {key}")
            if str(key).lower() in DICTIONARY_LEARNER_LOCALE_KEYS:
                errors.append(f"dictionary core atom {atom_id} contains learner locale key: {key}")
        for path in _find_forbidden_dictionary_core_nested_keys(atom_value):
            errors.append(f"dictionary core atom {atom_id} contains forbidden nested display/locale key: {path}")
    return errors


def _find_forbidden_dictionary_core_nested_keys(value: Any, prefix: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            path = f"{prefix}.{key_text}" if prefix else key_text
            if prefix and (
                key in DICTIONARY_CORE_FORBIDDEN_DISPLAY_KEYS
                or key_lower in DICTIONARY_LEARNER_LOCALE_KEYS
            ):
                hits.append(path)
            hits.extend(_find_forbidden_dictionary_core_nested_keys(nested, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            path = f"{prefix}[{index}]" if prefix else f"[{index}]"
            hits.extend(_find_forbidden_dictionary_core_nested_keys(item, path))
    return hits


def validate_learning_library_pipeline_legacy_bridge(
    source_path: Path,
    *,
    policy: str,
) -> list[str]:
    try:
        source = source_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"missing file: {source_path}"]

    marker_hits = [marker for marker in LL_LEGACY_BRIDGE_MARKERS if marker in source]
    flag_hits = [marker for marker in LL_LEGACY_BRIDGE_FLAG_MARKERS if marker in source]

    if policy == "allow":
        return []

    if policy == "flagged":
        if marker_hits and not flag_hits:
            return [
                "Learning Library legacy i18n bridge markers exist without an explicit fallback flag: "
                + ", ".join(marker_hits)
            ]
        return []

    if policy == "forbid":
        if marker_hits:
            return [
                "Learning Library legacy i18n bridge markers are forbidden after fccdr-07 retirement: "
                + ", ".join(marker_hits)
            ]
        return []

    return [f"unknown legacy bridge policy: {policy}"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--learning-library-manifest", type=Path)
    parser.add_argument("--learning-library-i18n-sidecar-manifest", type=Path)
    parser.add_argument("--package-manifest", type=Path)
    parser.add_argument("--content-pipeline-learning-library-source", type=Path)
    parser.add_argument(
        "--legacy-learning-library-bridge-policy",
        choices=("allow", "flagged", "forbid"),
        default="allow",
    )
    parser.add_argument("--require-locale", default=None)
    parser.add_argument("--min-sentence-translations", type=int, default=0)
    parser.add_argument("--min-sidecar-sentence-coverage", type=float, default=0.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if (
        not args.learning_library_manifest
        and not args.learning_library_i18n_sidecar_manifest
        and not args.package_manifest
        and not args.content_pipeline_learning_library_source
    ):
        parser.error(
            "provide --learning-library-manifest, --learning-library-i18n-sidecar-manifest, "
            "--package-manifest, and/or --content-pipeline-learning-library-source"
        )

    errors: list[str] = []
    if args.learning_library_manifest:
        errors.extend(
            validate_learning_library_manifest(
                args.learning_library_manifest,
                require_locale=args.require_locale,
                min_sentence_translations=args.min_sentence_translations,
            )
        )
    if args.learning_library_i18n_sidecar_manifest:
        errors.extend(
            validate_learning_library_i18n_sidecar_manifest(
                args.learning_library_i18n_sidecar_manifest,
                min_sentence_coverage=args.min_sidecar_sentence_coverage,
            )
        )
    if args.package_manifest:
        errors.extend(validate_package_manifest(args.package_manifest))
    if args.content_pipeline_learning_library_source:
        errors.extend(
            validate_learning_library_pipeline_legacy_bridge(
                args.content_pipeline_learning_library_source,
                policy=args.legacy_learning_library_bridge_policy,
            )
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("content contracts ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
