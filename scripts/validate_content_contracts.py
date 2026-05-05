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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--learning-library-manifest", type=Path)
    parser.add_argument("--package-manifest", type=Path)
    parser.add_argument("--require-locale", default=None)
    parser.add_argument("--min-sentence-translations", type=int, default=0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.learning_library_manifest and not args.package_manifest:
        parser.error("provide --learning-library-manifest and/or --package-manifest")

    errors: list[str] = []
    if args.learning_library_manifest:
        errors.extend(
            validate_learning_library_manifest(
                args.learning_library_manifest,
                require_locale=args.require_locale,
                min_sentence_translations=args.min_sentence_translations,
            )
        )
    if args.package_manifest:
        errors.extend(validate_package_manifest(args.package_manifest))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("content contracts ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
