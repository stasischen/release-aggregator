#!/usr/bin/env python3
"""TLG-006 validator for unit_blueprint_v1 draft.

Checks:
- TLG-001 top-level contract essentials
- TLG-002 mandatory node suffix coverage
- TLG-003 rubric threshold/range checks on interactive nodes
- TLG-004 repair link resolvability via registry (from payload.pattern_meta)
- Reading overlay consistency checks (question_id/evidence mapping)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MANDATORY_SUFFIXES = ["L1", "L2", "L3", "D1", "G1", "G2", "P1", "P2", "P3", "P4", "P5", "P6", "R1"]
INTERACTIVE_OUTPUT_MODES = {"chunk_assembly", "frame_fill", "response_builder", "pattern_transform", "guided", "review_retrieval"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def suffix_of(node_id: str) -> str:
    return node_id.split("-")[-1]


def load_repair_ids(path: Path) -> set[str]:
    data = load_json(path)
    return {str(e.get("repair_id", "")) for e in data.get("entries", []) if e.get("repair_id")}


def validate(blueprint: dict[str, Any], repair_ids: set[str] | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if blueprint.get("version") != "unit_blueprint_v1":
        errors.append("ERR_UNSUPPORTED_VERSION_V1: version must be unit_blueprint_v1")
    if blueprint.get("adapter_version") != "frontend_unit_adapter_v1":
        errors.append("ERR_UNSUPPORTED_ADAPTER_VERSION: adapter_version must be frontend_unit_adapter_v1")

    unit = blueprint.get("unit") or {}
    support_langs = unit.get("support_langs", [])
    if not isinstance(support_langs, list) or not {"zh_tw", "en"}.issubset(set(support_langs)):
        errors.append("ERR_MISSING_SUPPORT_LANGS: support_langs must include zh_tw and en")

    sequence = blueprint.get("sequence") or []
    suffixes = {suffix_of(str(n.get("node_id", ""))) for n in sequence}
    missing_suffixes = [s for s in MANDATORY_SUFFIXES if s not in suffixes]
    if missing_suffixes:
        errors.append(f"ERR_TLG_MISSING_MANDATORY_NODE: missing {missing_suffixes}")

    for node in sequence:
        node_id = str(node.get("node_id", ""))
        output_mode = str(node.get("output_mode", "none"))
        payload = node.get("payload") or {}

        if output_mode in INTERACTIVE_OUTPUT_MODES:
            rubric = payload.get("rubric")
            if not isinstance(rubric, dict):
                errors.append(f"ERR_TLG_RUBRIC_MISSING: {node_id}")
                continue

            threshold = rubric.get("pass_threshold")
            min_attempts = rubric.get("min_attempts")
            max_hints = rubric.get("max_hints_for_pass")
            required_elements = rubric.get("required_elements", [])

            if not isinstance(threshold, (int, float)) or threshold < 0.5 or threshold > 1.0:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} pass_threshold={threshold}")
            if not isinstance(min_attempts, int) or min_attempts < 1 or min_attempts > 5:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} min_attempts={min_attempts}")
            if not isinstance(max_hints, int) or max_hints < 0 or max_hints > 5:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} max_hints_for_pass={max_hints}")
            if not isinstance(required_elements, list) or len(required_elements) == 0:
                errors.append(f"ERR_TLG_REQUIRED_ELEMENTS_EMPTY: {node_id}")

        if node_id.endswith("-P4") and output_mode == "response_builder":
            if not payload.get("trigger_type") or not payload.get("repair_goal"):
                errors.append(f"ERR_TLG_MISSING_REPAIR_METADATA: {node_id}")

        pattern_meta = payload.get("pattern_meta") or {}
        repair_links = pattern_meta.get("repair_links", [])
        if repair_ids is not None and isinstance(repair_links, list):
            for rid in repair_links:
                rid_text = str(rid)
                if rid_text and rid_text not in repair_ids:
                    errors.append(f"ERR_TLG_PATTERN_REPAIR_LINK_UNRESOLVED: {node_id} -> {rid_text}")

        reading_overlay = payload.get("reading_overlay")
        if isinstance(reading_overlay, dict):
            q_ids = {q.get("question_id") for q in reading_overlay.get("question_blueprint", []) if isinstance(q, dict)}
            em_ids = {e.get("question_id") for e in reading_overlay.get("evidence_mapping", []) if isinstance(e, dict)}
            if q_ids and em_ids and not q_ids.issubset(em_ids):
                errors.append(f"ERR_TLR_EVIDENCE_QUESTION_MISMATCH: {node_id}")
            if not reading_overlay.get("evidence_mapping"):
                errors.append(f"ERR_TLR_MISSING_EVIDENCE_MAPPING: {node_id}")

    if not blueprint.get("scheduled_followups"):
        warnings.append("WARN_TLG_MISSING_FOLLOWUPS: scheduled_followups is empty")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate unit_blueprint_v1 against TLG-001..006 core rules")
    parser.add_argument("--blueprint", required=True, help="Path to unit_blueprint_v1 JSON")
    parser.add_argument("--repair-registry", help="Optional repair registry path for repair link resolution")
    args = parser.parse_args()

    blueprint = load_json(Path(args.blueprint))
    repair_ids = load_repair_ids(Path(args.repair_registry)) if args.repair_registry else None

    errors, warnings = validate(blueprint, repair_ids)

    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)

    if errors:
        print(f"TLG-006 UNIT RESULT: FAIL (errors={len(errors)}, warnings={len(warnings)})")
        return 1
    print(f"TLG-006 UNIT RESULT: PASS (warnings={len(warnings)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
