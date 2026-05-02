#!/usr/bin/env python3
"""Manifest-driven production assembler prototype for PRG."""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


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


class CandidateInventory:
    """Inventory of available candidate lessons from staging."""

    def __init__(self, lessons: dict[str, dict[str, Any]], root: Path):
        self.lessons = lessons
        self.root = root

    def resolve_path(self, rel_path: str) -> Path:
        """Correctly resolve path by avoiding redundant prefixes from root."""
        # Normalize rel_path
        p = Path(rel_path.replace("\\", "/"))
        
        # If the path is absolute, return it
        if p.is_absolute():
            return p
            
        # Detect redundant segments
        # If root is .../assets/content/production and rel_path is assets/content/production/...
        # Result should be root.parent.parent.parent / assets/content/production/...
        root_parts = self.root.parts
        p_parts = p.parts
        
        # Check for overlap
        overlap_index = -1
        for i in range(1, min(len(root_parts), len(p_parts)) + 1):
            if root_parts[-i:] == p_parts[:i]:
                overlap_index = i
        
        if overlap_index != -1:
            # Overlap found! Reconstruct path.
            # Example: root=A/B/C, rel=C/D -> Result=A/B/C/D
            # Actually, standard join(A/B/C, C/D) -> A/B/C/C/D
            # So we strip the overlap from the root or the rel path.
            base = Path(*root_parts[:-overlap_index])
            return base / p
            
        return self.root / p

    @classmethod
    def load_from_manifest(cls, manifest_path: Path, root: Optional[Path] = None) -> CandidateInventory:
        """Load inventory from a manifest.json file."""
        data = load_json(manifest_path)
        lessons = {}
        # If root is not provided, use the manifest's parent
        final_root = root or manifest_path.parent
        for lesson in data.get("lessons", []):
            level_id = lesson.get("level_id")
            if isinstance(level_id, str):
                lessons[level_id] = lesson
        return cls(lessons, final_root)

    @classmethod
    def scan_directory(cls, staging_root: Path) -> CandidateInventory:
        """Adapter: Scan staging directory to build a candidate inventory."""
        lessons = {}
        
        # Scanning logic remains the same (it creates relative paths without redundancy)
        # Dialogue: core/dialogue/**/*.json
        dialogue_root = staging_root / "core/dialogue"
        if dialogue_root.exists():
            for f in dialogue_root.rglob("*.json"):
                rel_path = f.relative_to(staging_root)
                lesson_id = f.stem
                lessons[lesson_id] = {
                    "level_id": lesson_id,
                    "path": str(rel_path).replace("\\", "/"),
                    "type": "dialogue"
                }

        # Video: core/video/*.json
        video_root = staging_root / "core/video"
        if video_root.exists():
            for f in video_root.glob("*.json"):
                rel_path = f.relative_to(staging_root)
                lesson_id = f.stem
                lessons[lesson_id] = {
                    "level_id": lesson_id,
                    "path": str(rel_path).replace("\\", "/"),
                    "type": "video"
                }

        # Article: core/article/*.json
        article_root = staging_root / "core/article"
        if article_root.exists():
            for f in article_root.glob("*.json"):
                rel_path = f.relative_to(staging_root)
                lesson_id = f.stem
                lessons[lesson_id] = {
                    "level_id": lesson_id,
                    "path": str(rel_path).replace("\\", "/"),
                    "type": "article"
                }

        return cls(lessons, staging_root)


def find_candidate(lesson_id: str, content_type: str, inventory: CandidateInventory) -> dict[str, Any] | None:
    """Find a candidate lesson with legacy naming gap support."""
    # 1. Exact match
    if lesson_id in inventory.lessons:
        return inventory.lessons[lesson_id]

    # 2. Legacy naming gap: B1/B2/C1 and A1/A2 dialogue prefix mismatch
    if content_type == "dialogue":
        prefixes = [
            "ko_l1_dialogue_", "ko_l2_dialogue_", 
            "ko_l3_dialogue_", "ko_l4_dialogue_", 
            "ko_l5_dialogue_"
        ]
        for prefix in prefixes:
            if lesson_id.startswith(prefix):
                short_id = lesson_id[len(prefix):]
                # Try matching by short ID (e.g., b1_01)
                if short_id in inventory.lessons:
                    return inventory.lessons[short_id]
                # Try matching by case-insensitive name with underscore/dash normalization
                for candidate_id in inventory.lessons:
                    if candidate_id.replace("-", "_").lower() == short_id.replace("-", "_").lower():
                        return inventory.lessons[candidate_id]

    return None


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

        for field in [
            "viewer_verified",
            "qa_gate_passed",
            "staging_only",
        ]:
            if not isinstance(entry.get(field), bool):
                errors.append(f"{prefix}.{field} must be a boolean")

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
                "can_do": entry.get("can_do"),
                "knowledge_refs": entry.get("knowledge_refs", []),
                "key_sentence_preview": entry.get("key_sentence_preview"),
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
        "updated_at": utc_now(),
        "units": ordered_units,
        "lessons": ordered_lessons,
    }


def build_manifest_lesson(candidate: dict[str, Any], entry: dict[str, Any], lang: str) -> dict[str, Any]:
    lesson_id = entry["lesson_id"]
    lesson = copy.deepcopy(candidate)
    lesson["level_id"] = lesson.get("level_id") or lesson_id
    lesson["lesson_id"] = lesson.get("lesson_id") or lesson_id
    lesson["unit_id"] = lesson.get("unit_id") or entry["unit_id"]
    lesson["lang"] = lesson.get("lang") or entry.get("lang") or lang
    lesson["type"] = normalize_content_type(lesson.get("type") or entry["content_type"])

    for field in [
        "title",
        "subtitle",
        "theme_tags",
        "skill_tags",
        "status_flags",
    ]:
        if lesson.get(field) is None and entry.get(field) is not None:
            lesson[field] = entry.get(field)

    return lesson


def assemble_release(
    release_manifest_path: Path,
    candidate_inventory: CandidateInventory,
    output_dir: Path,
    strict_mode: bool,
    allow_unassigned_units: bool,
    lang: str,
    study_discovery_path: str,
) -> dict[str, Any]:
    release_manifest = load_json(release_manifest_path)

    parse_errors = validate_release_manifest(release_manifest)
    if parse_errors:
        raise ValueError("Release manifest validation failed:\n- " + "\n- ".join(parse_errors))

    eligible_entries = [
        entry
        for entry in release_manifest["entries"]
        if entry["release_status"] == "production" and not entry.get("staging_only", False)
    ]
    if not eligible_entries:
        raise ValueError("Release manifest has no production-eligible entries after filtering")

    gaps: list[dict[str, Any]] = []
    packaged_manifest_lessons: list[dict[str, Any]] = []
    packaged_entries: list[dict[str, Any]] = []

    for entry in eligible_entries:
        lesson_id = entry["lesson_id"]
        content_type = entry["content_type"]
        
        candidate = find_candidate(lesson_id, content_type, candidate_inventory)
        
        if candidate is None:
            gaps.append({
                "lesson_id": lesson_id,
                "reason": "missing_candidate",
                "severity": "error",
                "details": f"No candidate found in inventory for {content_type} lesson.",
                "candidate_path": None,
                "manifest_path": str(release_manifest_path)
            })
            continue

        candidate_path = candidate.get("path")
        if not isinstance(candidate_path, str) or not candidate_path:
            gaps.append({
                "lesson_id": lesson_id,
                "reason": "invalid_candidate_entry",
                "severity": "error",
                "details": "Candidate match found but entry is missing a path field.",
                "candidate_path": candidate_path,
                "manifest_path": str(release_manifest_path)
            })
            continue

        # Resolved path for disk verification
        abs_candidate_path = candidate_inventory.resolve_path(candidate_path)

        # Asset mismatch check (if manifest explicitly contains a path)
        manifest_asset_path = entry.get("asset_path")
        if isinstance(manifest_asset_path, str) and manifest_asset_path:
            if manifest_asset_path != candidate_path:
                gaps.append({
                    "lesson_id": lesson_id,
                    "reason": "asset_path_mismatch",
                    "severity": "error",
                    "details": f"Release manifest specifies {manifest_asset_path} but candidate is at {candidate_path}",
                    "candidate_path": candidate_path,
                    "manifest_path": str(release_manifest_path)
                })

        # Content type mismatch check
        candidate_content_type = normalize_content_type(candidate.get("type") or content_type)
        if candidate_content_type != content_type:
            gaps.append({
                "lesson_id": lesson_id,
                "reason": "content_type_mismatch",
                "severity": "error",
                "details": f"Release manifest expects {content_type} but candidate is {candidate_content_type}",
                "candidate_path": candidate_path,
                "manifest_path": str(release_manifest_path)
            })

        # Disk check
        if not abs_candidate_path.exists():
            gaps.append({
                "lesson_id": lesson_id,
                "reason": "disk_missing",
                "severity": "error",
                "details": f"Candidate file not found on disk at: {abs_candidate_path}",
                "candidate_path": str(abs_candidate_path),
                "manifest_path": str(release_manifest_path)
            })

        # Unit check
        if not allow_unassigned_units and entry["unit_id"] == "__unassigned__":
            gaps.append({
                "lesson_id": lesson_id,
                "reason": "unresolved_unit_id",
                "severity": "error",
                "details": "Lesson is assigned to __unassigned__ unit, which is disabled in strict catalog mode.",
                "candidate_path": candidate_path,
                "manifest_path": str(release_manifest_path)
            })

        # Only add to packaged list if no error gaps for this lesson? 
        # Actually, if we have gaps, we should still allow planning mode to finish.
        # Strict mode will fail later.
        packaged_manifest_lessons.append(build_manifest_lesson(candidate, entry, lang))
        packaged_entries.append(entry)

    if strict_mode and gaps:
        print(f"ERROR: {len(gaps)} validation gaps found in STRICT MODE.")
        for gap in gaps[:10]:
            print(f"  - [{gap['reason']}] {gap['lesson_id']}: {gap['details']}")
        if len(gaps) > 10:
            print(f"    ... and {len(gaps)-10} more.")
        raise ValueError("Production release assembly failed due to validation gaps.")

    derived_manifest = {
        "version": "1.0.0",
        "lang": lang,
        "last_updated": utc_now(),
        "files": {
            "study_discovery": study_discovery_path,
        },
        "lessons": packaged_manifest_lessons,
    }
    derived_catalog = build_catalog_from_entries(packaged_entries)
    
    production_plan = {
        "generated_at": utc_now(),
        "release_manifest": str(release_manifest_path).replace("\\", "/"),
        "candidate_root": str(candidate_inventory.root).replace("\\", "/"),
        "summary": {
            "manifest_entries": len(release_manifest["entries"]),
            "eligible_entries": len(eligible_entries),
            "packaged_lessons": len(packaged_manifest_lessons),
            "packaged_units": len(derived_catalog["units"]),
            "gap_count": len(gaps),
        },
        "gaps": gaps,
        "allowlisted_lessons": [entry["lesson_id"] for entry in packaged_entries],
    }

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "manifest.json", derived_manifest)
    write_json(output_dir / "lesson_catalog.json", derived_catalog)
    write_json(output_dir / "production_plan.json", production_plan)
        
    return production_plan


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    aggregator_root = script_dir.parent.parent
    content_ko_staging = aggregator_root.parent / "content-ko/dist_unified/staging/ko"

    parser = argparse.ArgumentParser(description="Prototype manifest-driven production assembler")
    parser.add_argument(
        "--release-manifest",
        type=Path,
        default=aggregator_root / "staging/prd.release_manifest.seed.json",
    )
    parser.add_argument(
        "--candidate-source",
        type=str,
        help="Path to candidate manifest.json or a staging directory to scan",
        default=str(content_ko_staging) if content_ko_staging.exists() else None,
    )
    parser.add_argument(
        "--candidate-root",
        type=Path,
        default=None,
        help="Base root for manifest paths (optional, used to resolve overlaps)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=aggregator_root / "staging/prototype_output",
    )
    parser.add_argument(
        "--lang",
        default="ko",
        help="Root language code to emit in production manifest.json",
    )
    parser.add_argument(
        "--study-discovery-path",
        default="assets/content/production/lesson_catalog.json",
        help="Frontend asset path for the generated lesson_catalog.json",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=True,
        help="Fail closed on any gap (default: True)",
    )
    parser.add_argument(
        "--planning",
        action="store_false",
        dest="strict",
        help="Planning mode: report all gaps in plan JSON but generate artifacts anyway",
    )
    parser.add_argument(
        "--allow-unassigned-units",
        action="store_true",
        help="Allow __unassigned__ unit_ids in output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    
    if args.candidate_source is None:
        print("ERROR: No candidate source available.")
        # Explicit path from requirement: e:\Githubs\lingo\content-ko\dist_unified\staging\ko
        script_dir = Path(__file__).resolve().parent
        aggregator_root = script_dir.parent.parent
        expected_default = aggregator_root.parent / "content-ko/dist_unified/staging/ko"
        print(f"Default expected path: {expected_default}")
        print("Required: Re-run with --candidate-source <path>")
        return 1

    source_path = Path(args.candidate_source)
    if not source_path.exists():
        print(f"ERROR: Candidate source not found at: {source_path}")
        return 1

    if source_path.is_dir():
        print(f"Candidate Source: Directory ({source_path}) - Using Scanner Adapter")
        inventory = CandidateInventory.scan_directory(source_path)
    else:
        print(f"Candidate Source: Manifest ({source_path})")
        # If explicitly providing a manifest, root defaults to manifest dir unless overridden
        root = args.candidate_root or source_path.parent
        inventory = CandidateInventory.load_from_manifest(source_path, root)

    try:
        plan = assemble_release(
            release_manifest_path=args.release_manifest,
            candidate_inventory=inventory,
            output_dir=args.output_dir,
            strict_mode=args.strict,
            allow_unassigned_units=args.allow_unassigned_units,
            lang=args.lang,
            study_discovery_path=args.study_discovery_path,
        )
        mode_str = "STRICT" if args.strict else "PLANNING"
        print(
            f"Assembled production plan ({mode_str}): "
            f"{plan['summary']['packaged_lessons']} lessons, "
            f"{plan['summary']['packaged_units']} units. "
            f"Gaps found: {plan['summary']['gap_count']}."
        )
        print(f"Outputs written to {args.output_dir}")
        return 0
    except ValueError as e:
        print(f"FATAL: {e}")
        return 1
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
