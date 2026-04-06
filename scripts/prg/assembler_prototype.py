#!/usr/bin/env python3
"""Manifest-driven production assembler prototype for PRG."""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RELEASE_STATUS_VALUES = {"draft", "staging_only", "production"}
CONTENT_TYPE_VALUES = {"dialogue", "video", "article", "grammar-heavy"}
COURSE_TYPE_VALUES = {"lesson", "bonus", "supplemental"}


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
    if raw_value in CONTENT_TYPE_VALUES:
        return raw_value
    return "dialogue"


def validate_release_manifest(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["release manifest root must be a JSON object"]

    entries = payload.get("entries")
    if not isinstance(entries, list):
        return ["release manifest must contain an entries array"]

    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in [
            "unit_id",
            "lesson_id",
            "release_status",
            "content_type",
            "course_type",
            "contract_version",
        ]:
            if not isinstance(entry.get(field), str) or not entry.get(field):
                errors.append(f"{prefix}.{field} must be a non-empty string")

        if entry.get("release_status") not in RELEASE_STATUS_VALUES:
            errors.append(f"{prefix}.release_status is invalid: {entry.get('release_status')}")
        if entry.get("content_type") not in CONTENT_TYPE_VALUES:
            errors.append(f"{prefix}.content_type is invalid: {entry.get('content_type')}")
        if entry.get("course_type") not in COURSE_TYPE_VALUES:
            errors.append(f"{prefix}.course_type is invalid: {entry.get('course_type')}")

        source_refs = entry.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs or not all(
            isinstance(item, str) and item for item in source_refs
        ):
            errors.append(f"{prefix}.source_refs must be a non-empty string array")

        for field in ["viewer_verified", "qa_gate_passed", "staging_only"]:
            if not isinstance(entry.get(field), bool):
                errors.append(f"{prefix}.{field} must be a boolean")

    return errors


def build_catalog_from_entries(entries: list[dict[str, Any]]) -> dict[str, Any]:
    units: dict[str, dict[str, Any]] = {}
    lessons: list[dict[str, Any]] = []

    for entry in entries:
        unit_id = entry["unit_id"]
        if unit_id not in units:
            units[unit_id] = {
                "id": unit_id,
                "order": entry.get("unit_order") if isinstance(entry.get("unit_order"), int) else 9999,
                "level": entry.get("unit_level") or "Unknown",
                "title": entry.get("unit_title") or {"en": "Unassigned"},
                "subtitle": entry.get("unit_subtitle") or {"en": "Requires reconciliation"},
            }

        lessons.append(
            {
                "lesson_id": entry["lesson_id"],
                "unit_id": unit_id,
                "order_in_unit": entry.get("order_in_unit"),
                "estimated_minutes": entry.get("estimated_minutes"),
                "title": entry.get("title"),
                "subtitle": entry.get("subtitle"),
                "theme_tags": entry.get("theme_tags", []),
                "skill_tags": entry.get("skill_tags", []),
                "status_flags": entry.get("status_flags", []),
            }
        )

    ordered_units = sorted(units.values(), key=lambda item: (item.get("order", 9999), item["id"]))
    ordered_lessons = sorted(
        lessons,
        key=lambda item: (
            item["unit_id"],
            item.get("order_in_unit") if isinstance(item.get("order_in_unit"), int) else 9999,
            item["lesson_id"],
        ),
    )

    return {
        "version": 1,
        "updated_at": datetime.now(timezone.utc).date().isoformat(),
        "units": ordered_units,
        "lessons": ordered_lessons,
    }


def assemble_release(
    release_manifest_path: Path,
    candidate_manifest_path: Path,
    output_dir: Path,
    candidate_root: Path | None,
    strict_catalog: bool,
) -> dict[str, Any]:
    release_manifest = load_json(release_manifest_path)
    candidate_manifest = load_json(candidate_manifest_path)

    parse_errors = validate_release_manifest(release_manifest)
    if parse_errors:
        raise ValueError("Release manifest validation failed:\n- " + "\n- ".join(parse_errors))

    candidate_lessons = candidate_manifest.get("lessons", [])
    candidate_by_lesson_id = {
        lesson["level_id"]: lesson
        for lesson in candidate_lessons
        if isinstance(lesson, dict) and isinstance(lesson.get("level_id"), str)
    }

    eligible_entries = [
        entry
        for entry in release_manifest["entries"]
        if entry["release_status"] == "production" and entry["staging_only"] is False
    ]
    if not eligible_entries:
        raise ValueError("Release manifest has no production-eligible entries after filtering")

    errors: list[str] = []
    packaged_manifest_lessons: list[dict[str, Any]] = []
    packaged_entries: list[dict[str, Any]] = []

    for entry in eligible_entries:
        lesson_id = entry["lesson_id"]
        candidate = candidate_by_lesson_id.get(lesson_id)
        if candidate is None:
            errors.append(f"Missing candidate manifest entry for allowlisted lesson {lesson_id}")
            continue

        candidate_path = candidate.get("path")
        if not isinstance(candidate_path, str) or not candidate_path:
            errors.append(f"Candidate manifest entry for {lesson_id} is missing path")
            continue

        manifest_asset_path = entry.get("asset_path")
        if isinstance(manifest_asset_path, str) and manifest_asset_path and manifest_asset_path != candidate_path:
            errors.append(
                f"Asset path mismatch for {lesson_id}: release manifest={manifest_asset_path} candidate manifest={candidate_path}"
            )

        if Path(candidate_path).stem != lesson_id:
            errors.append(
                f"Asset filename mismatch for {lesson_id}: candidate path stem={Path(candidate_path).stem}"
            )

        candidate_content_type = normalize_content_type(candidate.get("type"))
        if candidate_content_type != entry["content_type"]:
            errors.append(
                f"Content type mismatch for {lesson_id}: release manifest={entry['content_type']} candidate manifest={candidate_content_type}"
            )

        if candidate_root is not None:
            candidate_file = candidate_root / candidate_path
            if not candidate_file.exists():
                errors.append(f"Candidate asset missing on disk for {lesson_id}: {candidate_file}")

        if strict_catalog and entry["unit_id"] == "__unassigned__":
            errors.append(f"Allowlisted lesson {lesson_id} has unresolved unit_id __unassigned__")

        packaged_manifest_lessons.append(copy.deepcopy(candidate))
        packaged_entries.append(entry)

    if errors:
        raise ValueError("Production release assembly failed:\n- " + "\n- ".join(errors))

    derived_manifest = {
        "version": candidate_manifest.get("version", "1.0.0"),
        "last_updated": utc_now(),
        "packages": candidate_manifest.get("packages", {}),
        "lessons": packaged_manifest_lessons,
    }
    derived_catalog = build_catalog_from_entries(packaged_entries)
    production_plan = {
        "generated_at": utc_now(),
        "release_manifest": str(release_manifest_path),
        "candidate_manifest": str(candidate_manifest_path),
        "summary": {
            "manifest_entries": len(release_manifest["entries"]),
            "eligible_entries": len(eligible_entries),
            "packaged_lessons": len(packaged_manifest_lessons),
            "packaged_units": len(derived_catalog["units"]),
        },
        "allowlisted_lessons": [entry["lesson_id"] for entry in packaged_entries],
    }

    write_json(output_dir / "manifest.json", derived_manifest)
    write_json(output_dir / "lesson_catalog.json", derived_catalog)
    write_json(output_dir / "production_plan.json", production_plan)
    return production_plan


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    aggregator_root = script_dir.parent.parent
    frontend_root = aggregator_root.parent / "lingo-frontend-web"

    parser = argparse.ArgumentParser(description="Prototype manifest-driven production assembler")
    parser.add_argument(
        "--release-manifest",
        type=Path,
        default=aggregator_root / "staging/prd.release_manifest.seed.json",
    )
    parser.add_argument(
        "--candidate-manifest",
        type=Path,
        default=frontend_root / "assets/content/production/manifest.json",
    )
    parser.add_argument(
        "--candidate-root",
        type=Path,
        default=frontend_root,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=aggregator_root / "staging/prototype_output",
    )
    parser.add_argument(
        "--skip-asset-existence-check",
        action="store_true",
        help="Skip on-disk candidate asset existence checks and generate planning artifacts from manifest metadata only",
    )
    parser.add_argument(
        "--allow-unassigned-units",
        action="store_true",
        help="Allow __unassigned__ unit_ids in planning output instead of failing closed",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan = assemble_release(
        release_manifest_path=args.release_manifest,
        candidate_manifest_path=args.candidate_manifest,
        output_dir=args.output_dir,
        candidate_root=None if args.skip_asset_existence_check else args.candidate_root,
        strict_catalog=not args.allow_unassigned_units,
    )
    print(
        "Assembled production plan with "
        f"{plan['summary']['packaged_lessons']} lessons across "
        f"{plan['summary']['packaged_units']} units."
    )
    print(f"Outputs written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
