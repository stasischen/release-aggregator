#!/usr/bin/env python3
"""Seed the initial production release manifest from legacy production assets."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


UNASSIGNED_UNIT_ID = "__unassigned__"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def normalize_content_type(raw_value: Any) -> str:
    if raw_value == "grammar":
        return "grammar-heavy"
    if raw_value in {"dialogue", "video", "article", "grammar-heavy"}:
        return raw_value
    return "dialogue"


def normalize_course_type(raw_value: Any) -> str:
    if raw_value in {"lesson", "bonus", "supplemental"}:
        return raw_value
    return "lesson"


def infer_alias_candidates(lesson_id: str, catalog_lessons: list[dict[str, Any]]) -> list[str]:
    suffix = "_".join(lesson_id.split("_")[3:])
    if not suffix:
        return []

    matches: list[str] = []
    for lesson in catalog_lessons:
        candidate_id = lesson.get("lesson_id")
        if isinstance(candidate_id, str) and candidate_id.endswith(suffix):
            matches.append(candidate_id)
    return matches[:5]


def seed_release_manifest(
    production_manifest_path: Path,
    study_discovery_path: Path,
    output_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    manifest_data = load_json(production_manifest_path)
    catalog_data = load_json(study_discovery_path)

    manifest_lessons = manifest_data.get("lessons", [])
    catalog_lessons = catalog_data.get("lessons", [])
    catalog_units = catalog_data.get("units", [])

    catalog_by_lesson_id = {
        lesson["lesson_id"]: lesson
        for lesson in catalog_lessons
        if isinstance(lesson, dict) and isinstance(lesson.get("lesson_id"), str)
    }
    units_by_id = {
        unit["id"]: unit
        for unit in catalog_units
        if isinstance(unit, dict) and isinstance(unit.get("id"), str)
    }

    entries: list[dict[str, Any]] = []
    unmatched_manifest_lessons: list[dict[str, Any]] = []
    matched_lesson_ids: set[str] = set()

    for manifest_lesson in manifest_lessons:
        lesson_id = manifest_lesson.get("level_id")
        if not isinstance(lesson_id, str):
            raise ValueError("manifest.json contains a lesson without a string level_id")

        catalog_lesson = catalog_by_lesson_id.get(lesson_id)
        unit = (
            units_by_id.get(catalog_lesson.get("unit_id"))
            if isinstance(catalog_lesson, dict)
            else None
        )

        notes: list[str] = ["Initial seed from legacy production assets."]
        unit_id = UNASSIGNED_UNIT_ID

        if isinstance(catalog_lesson, dict):
            matched_lesson_ids.add(lesson_id)
            unit_id = catalog_lesson.get("unit_id", UNASSIGNED_UNIT_ID)
        else:
            alias_candidates = infer_alias_candidates(lesson_id, catalog_lessons)
            unmatched_manifest_lessons.append(
                {
                    "lesson_id": lesson_id,
                    "path": manifest_lesson.get("path"),
                    "content_type": manifest_lesson.get("type"),
                    "alias_candidates": alias_candidates,
                }
            )
            notes.append("Missing catalog lesson mapping; requires reconciliation.")
            if alias_candidates:
                notes.append("Possible catalog aliases: " + ", ".join(alias_candidates))

        title = manifest_lesson.get("title")
        if isinstance(catalog_lesson, dict) and catalog_lesson.get("title") is not None:
            title = catalog_lesson.get("title")

        entries.append(
            {
                "unit_id": unit_id,
                "lesson_id": lesson_id,
                "release_status": "production",
                "content_type": normalize_content_type(manifest_lesson.get("type")),
                "course_type": normalize_course_type(manifest_lesson.get("category")),
                "source_refs": [f"legacy_manifest:{lesson_id}"],
                "contract_version": "cm-v1.0.0",
                "viewer_verified": True,
                "qa_gate_passed": True,
                "staging_only": False,
                "asset_path": manifest_lesson.get("path"),
                "lang": manifest_lesson.get("lang"),
                "title": title,
                "subtitle": catalog_lesson.get("subtitle") if isinstance(catalog_lesson, dict) else None,
                "unit_title": unit.get("title") if isinstance(unit, dict) else None,
                "unit_subtitle": unit.get("subtitle") if isinstance(unit, dict) else None,
                "unit_level": unit.get("level") if isinstance(unit, dict) else None,
                "unit_order": unit.get("order") if isinstance(unit, dict) else None,
                "order_in_unit": catalog_lesson.get("order_in_unit") if isinstance(catalog_lesson, dict) else None,
                "estimated_minutes": catalog_lesson.get("estimated_minutes") if isinstance(catalog_lesson, dict) else None,
                "theme_tags": catalog_lesson.get("theme_tags", []) if isinstance(catalog_lesson, dict) else [],
                "skill_tags": catalog_lesson.get("skill_tags", []) if isinstance(catalog_lesson, dict) else [],
                "status_flags": catalog_lesson.get("status_flags", []) if isinstance(catalog_lesson, dict) else [],
                "notes": " ".join(notes),
            }
        )

    catalog_only_lessons = sorted(
        lesson_id for lesson_id in catalog_by_lesson_id.keys() if lesson_id not in matched_lesson_ids
    )

    seeded_manifest = {
        "version": "1.0.0",
        "updated_at": utc_now(),
        "entries": entries,
    }
    seed_report = {
        "generated_at": utc_now(),
        "sources": {
            "manifest_json": str(production_manifest_path),
            "study_discovery_json": str(study_discovery_path),
        },
        "summary": {
            "manifest_lessons": len(manifest_lessons),
            "catalog_lessons": len(catalog_lessons),
            "matched_lessons": len(matched_lesson_ids),
            "unmatched_manifest_lessons": len(unmatched_manifest_lessons),
            "catalog_only_lessons": len(catalog_only_lessons),
        },
        "unmatched_manifest_lessons": unmatched_manifest_lessons,
        "catalog_only_lessons": catalog_only_lessons,
    }

    write_json(output_path, seeded_manifest)
    write_json(report_path, seed_report)
    return seed_report


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    aggregator_root = script_dir.parent.parent
    frontend_root = aggregator_root.parent / "lingo-frontend-web"

    parser = argparse.ArgumentParser(description="Seed the initial PRD release manifest")
    parser.add_argument(
        "--production-manifest",
        type=Path,
        default=frontend_root / "assets/content/production/manifest.json",
    )
    parser.add_argument(
        "--study-discovery",
        type=Path,
        default=frontend_root / "assets/content/production/study_discovery.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=aggregator_root / "staging/prd.release_manifest.seed.json",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=aggregator_root / "staging/prd.release_manifest.seed.report.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = seed_release_manifest(
        production_manifest_path=args.production_manifest,
        study_discovery_path=args.study_discovery,
        output_path=args.output,
        report_path=args.report,
    )
    print(
        "Seeded release manifest with "
        f"{report['summary']['manifest_lessons']} manifest lessons; "
        f"{report['summary']['unmatched_manifest_lessons']} unmatched manifest lessons; "
        f"{report['summary']['catalog_only_lessons']} discovery-only lessons."
    )
    print(f"Seed report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
