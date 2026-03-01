#!/usr/bin/env python3
"""Convert target language pattern library between JSON and human-readable Markdown.

Markdown format is intentionally strict so it can round-trip with scripts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ARRAY_FIELDS = {
    "levels",
    "required_elements",
    "acceptable_variants",
    "constraints",
    "transform_types",
    "repair_links",
    "transfer_contexts",
}

ENTRY_FIELD_ORDER = [
    "level",
    "can_do",
    "frame",
    "required_elements",
    "acceptable_variants",
    "constraints",
    "transform_types",
    "repair_links",
    "transfer_contexts",
    "variant_of",
    "teaching_notes.zh_tw",
    "teaching_notes.en",
]

ENTRY_REQUIRED_FIELDS = [
    "level",
    "can_do",
    "frame",
    "required_elements",
    "acceptable_variants",
    "constraints",
    "transform_types",
    "repair_links",
    "transfer_contexts",
    "teaching_notes.zh_tw",
    "teaching_notes.en",
]

ALLOWED_LEVELS = {"A1", "A2"}
ALLOWED_TRANSFORM_TYPES = {
    "politeness_shift",
    "speech_level_shift",
    "tense_shift",
    "negation",
    "question_statement",
    "slot_substitution",
    "time_expression_shift",
    "context_retarget",
    "connective_extension",
    "modality_shift",
}
REPAIR_ID_RE = re.compile(r"^R-[A-Z]{2,3}-(HON|FORM|ORDER|PART|PRAG)-\d{3}$")
SLOT_RE = re.compile(r"\{([a-z0-9_]+)\}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    header_line = "| " + " | ".join(headers) + " |"
    align_line = "| " + " | ".join([":---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return [header_line, align_line, *body]


def parse_table(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int]:
    i = start
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].startswith("|"):
        raise ValueError(f"Expected markdown table at line {i + 1}")

    header = split_markdown_row(lines[i])
    i += 1
    if i >= len(lines) or not lines[i].startswith("|"):
        raise ValueError(f"Expected table separator at line {i + 1}")
    i += 1

    rows: list[list[str]] = []
    while i < len(lines) and lines[i].startswith("|"):
        row = split_markdown_row(lines[i])
        if len(row) != len(header):
            raise ValueError(f"Row width mismatch at line {i + 1}")
        rows.append(row)
        i += 1

    return header, rows, i


def split_markdown_row(line: str) -> list[str]:
    """Split markdown table row, allowing escaped pipes (\\|) inside cells."""
    raw = line.strip()
    if not (raw.startswith("|") and raw.endswith("|")):
        raise ValueError(f"Invalid markdown table row: {line}")
    content = raw[1:-1]

    cells: list[str] = []
    buf: list[str] = []
    escape = False
    for ch in content:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == "|":
            cells.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def to_json_array_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_json_array_text(text: str) -> list[str]:
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array but got: {text}")
    for item in data:
        if not isinstance(item, str):
            raise ValueError(f"Expected string array but got: {text}")
    return data


def json_to_markdown(data: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Target Language Pattern Library")
    lines.append("")
    lines.append("## Library")

    lib_rows = [
        ["library_id", str(data.get("library_id", ""))],
        ["version", str(data.get("version", ""))],
        ["target_lang", str(data.get("target_lang", ""))],
        ["domain", str(data.get("domain", ""))],
        ["levels", to_json_array_text(data.get("levels", []))],
        ["entry_count", str(len(data.get("entries", [])))],
    ]
    lines.extend(render_table(["field", "value"], lib_rows))
    lines.append("")

    for entry in data.get("entries", []):
        lines.append(f"## Entry: {entry.get('pattern_id', '')}")
        lines.append("")

        teaching_notes = entry.get("teaching_notes") or {}
        entry_rows = []
        for field in ENTRY_FIELD_ORDER:
            if field.startswith("teaching_notes."):
                key = field.split(".", 1)[1]
                value = teaching_notes.get(key, "")
            else:
                value = entry.get(field)

            if field in ARRAY_FIELDS:
                text = to_json_array_text(value or [])
            else:
                text = "" if value is None else str(value)
            entry_rows.append([field, text])

        lines.extend(render_table(["field", "value"], entry_rows))
        lines.append("")

        lines.append("### Slots")
        slots = entry.get("slots") or []
        slot_rows: list[list[str]] = []
        if slots:
            for slot in slots:
                slot_rows.append(
                    [
                        str(slot.get("name", "")),
                        str(slot.get("description", "")),
                        "true" if bool(slot.get("required", False)) else "false",
                        str(slot.get("value_type", "")),
                        to_json_array_text(slot.get("examples", [])),
                    ]
                )
        else:
            slot_rows.append(["(none)", "", "false", "", "[]"])

        lines.extend(render_table(["name", "description", "required", "value_type", "examples"], slot_rows))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_library(rows: list[list[str]]) -> dict[str, Any]:
    d = {k: v for k, v in rows}
    expected_entry_count = d.get("entry_count", "").strip()
    return {
        "library_id": d.get("library_id", ""),
        "version": d.get("version", ""),
        "target_lang": d.get("target_lang", ""),
        "domain": d.get("domain", ""),
        "levels": parse_json_array_text(d.get("levels", "[]")),
        "_expected_entry_count": expected_entry_count,
        "entries": [],
    }


def parse_entry_table(rows: list[list[str]]) -> dict[str, str]:
    d = {k: v for k, v in rows}
    missing = [k for k in ENTRY_REQUIRED_FIELDS if k not in d]
    if missing:
        raise ValueError(f"Entry table missing fields: {missing}")
    return d


def parse_slots_table(rows: list[list[str]]) -> list[dict[str, Any]]:
    if len(rows) == 1 and rows[0][0] == "(none)":
        return []

    slots: list[dict[str, Any]] = []
    for row in rows:
        name, description, required_text, value_type, examples_text = row
        if required_text not in {"true", "false"}:
            raise ValueError(f"Invalid required value in slot row: {required_text}")
        slots.append(
            {
                "name": name,
                "description": description,
                "required": required_text == "true",
                "value_type": value_type,
                "examples": parse_json_array_text(examples_text),
            }
        )
    return slots


def markdown_to_json(md_text: str) -> dict[str, Any]:
    lines = md_text.splitlines()
    i = 0

    while i < len(lines) and lines[i].strip() != "## Library":
        i += 1
    if i >= len(lines):
        raise ValueError("Missing '## Library' section")
    i += 1

    lib_header, lib_rows, i = parse_table(lines, i)
    if lib_header != ["field", "value"]:
        raise ValueError("Library table must use headers: field, value")
    result = parse_library(lib_rows)

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if not line.startswith("## Entry: "):
            i += 1
            continue

        pattern_id = line[len("## Entry: ") :].strip()
        i += 1

        entry_header, entry_rows, i = parse_table(lines, i)
        if entry_header != ["field", "value"]:
            raise ValueError(f"Entry {pattern_id} table must use headers: field, value")
        d = parse_entry_table(entry_rows)

        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines) or lines[i].strip() != "### Slots":
            raise ValueError(f"Entry {pattern_id} missing ### Slots section")
        i += 1

        slots_header, slots_rows, i = parse_table(lines, i)
        if slots_header != ["name", "description", "required", "value_type", "examples"]:
            raise ValueError(f"Entry {pattern_id} slot table has invalid headers")

        entry: dict[str, Any] = {
            "pattern_id": pattern_id,
            "level": d["level"],
            "can_do": d["can_do"],
            "frame": d["frame"],
            "slots": parse_slots_table(slots_rows),
            "required_elements": parse_json_array_text(d["required_elements"]),
            "acceptable_variants": parse_json_array_text(d["acceptable_variants"]),
            "constraints": parse_json_array_text(d["constraints"]),
            "transform_types": parse_json_array_text(d["transform_types"]),
            "repair_links": parse_json_array_text(d["repair_links"]),
            "transfer_contexts": parse_json_array_text(d["transfer_contexts"]),
            "teaching_notes": {
                "zh_tw": d["teaching_notes.zh_tw"],
                "en": d["teaching_notes.en"],
            },
        }
        if d.get("variant_of", "").strip():
            entry["variant_of"] = d["variant_of"].strip()
        result["entries"].append(entry)

    expected_entry_count = result.pop("_expected_entry_count", "")
    if expected_entry_count:
        try:
            expected = int(expected_entry_count)
            actual = len(result["entries"])
            if expected != actual:
                print(
                    f"Warning: entry_count mismatch in Markdown header (expected={expected}, actual={actual})",
                    file=sys.stderr,
                )
        except ValueError:
            print(
                f"Warning: invalid entry_count in Markdown header ({expected_entry_count!r})",
                file=sys.stderr,
            )

    return result


def cmd_json_to_md(input_path: Path, output_path: Path) -> int:
    data = load_json(input_path)
    md = json_to_markdown(data)
    output_path.write_text(md, encoding="utf-8")
    print(f"Wrote Markdown: {output_path}")
    return 0


def cmd_md_to_json(input_path: Path, output_path: Path) -> int:
    md_text = input_path.read_text(encoding="utf-8")
    data = markdown_to_json(md_text)
    save_json(output_path, data)
    print(f"Wrote JSON: {output_path}")
    return 0


def extract_frame_slots(frame: str) -> set[str]:
    return set(SLOT_RE.findall(frame or ""))


def validate_library(data: dict[str, Any], repair_registry_ids: set[str] | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if data.get("version") != "target_lang_pattern_library_v1":
        errors.append("ERR_TLG_PATTERN_LIB_VERSION_INVALID: version must be target_lang_pattern_library_v1")

    entries = data.get("entries")
    if not isinstance(entries, list):
        return ["ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD: entries must be a list"], warnings

    seen_ids: set[str] = set()
    for i, entry in enumerate(entries, start=1):
        entry_ref = entry.get("pattern_id") or f"index={i}"
        required_fields = [
            "pattern_id",
            "level",
            "can_do",
            "frame",
            "slots",
            "required_elements",
            "acceptable_variants",
            "constraints",
            "transform_types",
            "repair_links",
            "transfer_contexts",
            "teaching_notes",
        ]
        missing = [f for f in required_fields if f not in entry]
        if missing:
            errors.append(f"ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD: {entry_ref} missing {missing}")
            continue

        pattern_id = str(entry["pattern_id"])
        if pattern_id in seen_ids:
            errors.append(f"ERR_TLG_PATTERN_ID_DUPLICATED: {pattern_id}")
        seen_ids.add(pattern_id)

        if entry.get("level") not in ALLOWED_LEVELS:
            errors.append(f"ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD: {pattern_id} has invalid level")

        frame_slots = extract_frame_slots(str(entry.get("frame", "")))
        slot_defs = entry.get("slots", [])
        slot_names = {s.get("name") for s in slot_defs if isinstance(s, dict)}
        if frame_slots != slot_names:
            errors.append(
                f"ERR_TLG_PATTERN_SLOT_FRAME_MISMATCH: {pattern_id} frame_slots={sorted(frame_slots)} slot_defs={sorted(slot_names)}"
            )

        teaching_notes = entry.get("teaching_notes") or {}
        zh_note = str(teaching_notes.get("zh_tw", "")).strip()
        en_note = str(teaching_notes.get("en", "")).strip()
        if not zh_note:
            errors.append(f"ERR_TLG_PATTERN_EMPTY_ZH_TW_NOTE: {pattern_id}")
        if not en_note:
            warnings.append(f"WARN_TLG_PATTERN_EN_NOTE_STUB: {pattern_id}")

        transfer_contexts = entry.get("transfer_contexts", [])
        if len(transfer_contexts) < 2:
            errors.append(f"ERR_TLG_PATTERN_NO_TRANSFER_CONTEXT: {pattern_id}")

        transform_types = entry.get("transform_types", [])
        if len(transform_types) < 2:
            errors.append(f"ERR_TLG_PATTERN_NO_TRANSFORM_TYPE: {pattern_id}")
        invalid_transforms = [t for t in transform_types if t not in ALLOWED_TRANSFORM_TYPES]
        if invalid_transforms:
            errors.append(f"ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD: {pattern_id} invalid transform_types={invalid_transforms}")

        repair_links = entry.get("repair_links", [])
        if not repair_links:
            warnings.append(f"WARN_TLG_PATTERN_WEAK_REPAIR_LINK: {pattern_id} has no repair_links")
        for rid in repair_links:
            rid_text = str(rid)
            if not REPAIR_ID_RE.match(rid_text):
                warnings.append(f"WARN_TLG_PATTERN_WEAK_REPAIR_LINK: {pattern_id} invalid format {rid_text}")
            if repair_registry_ids is not None and rid_text not in repair_registry_ids:
                errors.append(f"ERR_TLG_PATTERN_REPAIR_LINK_UNRESOLVED: {pattern_id} -> {rid_text}")

        variant_of = str(entry.get("variant_of", "")).strip()
        if variant_of and variant_of == pattern_id:
            errors.append(f"ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD: {pattern_id} variant_of cannot self-reference")

    return errors, warnings


def load_repair_registry_ids(path: Path) -> set[str]:
    data = load_json(path)
    entries = data.get("entries", [])
    ids = set()
    for entry in entries:
        rid = entry.get("repair_id")
        if isinstance(rid, str) and rid.strip():
            ids.add(rid.strip())
    return ids


def cmd_validate(input_path: Path, repair_registry_path: Path | None) -> int:
    data = load_json(input_path)
    repair_registry_ids = load_repair_registry_ids(repair_registry_path) if repair_registry_path else None
    errors, warnings = validate_library(data, repair_registry_ids=repair_registry_ids)

    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)

    print(
        f"Validation summary: errors={len(errors)}, warnings={len(warnings)}, entries={len(data.get('entries', []))}"
    )
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pattern library JSON/Markdown codec")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    p_json_to_md = subparsers.add_parser("json-to-md", help="Convert pattern library JSON to Markdown")
    p_json_to_md.add_argument("--input", required=True)
    p_json_to_md.add_argument("--output", required=True)

    p_md_to_json = subparsers.add_parser("md-to-json", help="Convert pattern library Markdown to JSON")
    p_md_to_json.add_argument("--input", required=True)
    p_md_to_json.add_argument("--output", required=True)

    p_validate = subparsers.add_parser("validate", help="Validate pattern library contract for TLG-004/TLG-006 gates")
    p_validate.add_argument("--input", required=True)
    p_validate.add_argument("--repair-registry", required=False, help="Optional repair strategy registry JSON path")

    args = parser.parse_args()

    if args.cmd == "json-to-md":
        return cmd_json_to_md(Path(args.input), Path(args.output))
    if args.cmd == "md-to-json":
        return cmd_md_to_json(Path(args.input), Path(args.output))
    if args.cmd == "validate":
        repair_registry = Path(args.repair_registry) if args.repair_registry else None
        return cmd_validate(Path(args.input), repair_registry)

    raise ValueError(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
