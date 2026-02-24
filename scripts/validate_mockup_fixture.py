#!/usr/bin/env python3
"""Lightweight smoke checks for HTML mockup fixtures.

Checks:
- JSON syntax (fixture + schema)
- basic fixture structure
- common mixed-script typos in Korean strings (e.g. 7時, 二 잔, 하端)
- legacy alias usage warnings (answers_ko vs reference_answers_ko)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MOCKUP_DIR = ROOT / "docs" / "tasks" / "mockups"
FIXTURE_PATH = MOCKUP_DIR / "a1_u04_unit_blueprint_v0.json"
SCHEMA_PATH = MOCKUP_DIR / "unit_blueprint_v0.schema.json"


MIXED_PATTERNS = [
    (re.compile(r"7時"), "Found Chinese 時 in Korean string; likely should be '7시'."),
    (re.compile(r"二\s*잔"), "Found Chinese 二 in Korean quantity; likely should be '두 잔'."),
    (re.compile(r"하端"), "Found Chinese 端 in Korean word; likely should be '하단'."),
    (re.compile(r"外部\s*음식"), "Found Chinese 外部 mixed into Korean phrase; likely should be '외부 음식'."),
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_strings(obj: Any, path: str = "$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        fixture = load_json(FIXTURE_PATH)
    except Exception as e:
        print(f"ERROR: failed to parse fixture JSON: {FIXTURE_PATH}: {e}")
        return 2

    try:
        _schema = load_json(SCHEMA_PATH)
    except Exception as e:
        print(f"ERROR: failed to parse schema JSON: {SCHEMA_PATH}: {e}")
        return 2

    # Basic shape checks
    if fixture.get("version") != "unit_blueprint_v0":
        errors.append("fixture.version must be 'unit_blueprint_v0'")
    if not isinstance(fixture.get("sequence"), list) or not fixture["sequence"]:
        errors.append("fixture.sequence must be a non-empty array")

    # Mixed-script typo scan
    for s_path, value in iter_strings(fixture):
        for pattern, msg in MIXED_PATTERNS:
            if pattern.search(value):
                errors.append(f"{s_path}: {msg} Value={value!r}")

    # Alias usage scan
    for node in fixture.get("sequence", []):
        payload = node.get("payload") or {}
        if "answers_ko" in payload:
            warnings.append(
                f"{node.get('id', '<unknown>')}: uses legacy payload.answers_ko; prefer reference_answers_ko"
            )

    # Lightweight bilingual list length checks
    for node in fixture.get("sequence", []):
        payload = node.get("payload") or {}
        if "notice_items" in payload and "notice_items_zh_tw" in payload:
            if len(payload["notice_items"]) != len(payload["notice_items_zh_tw"]):
                warnings.append(
                    f"{node.get('id')}: notice_items and notice_items_zh_tw lengths differ "
                    f"({len(payload['notice_items'])} vs {len(payload['notice_items_zh_tw'])})"
                )

    if errors:
        print("Fixture validation FAILED")
        for e in errors:
            print(f"- ERROR: {e}")
        for w in warnings:
            print(f"- WARN: {w}")
        return 1

    print("Fixture validation OK")
    for w in warnings:
        print(f"- WARN: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

