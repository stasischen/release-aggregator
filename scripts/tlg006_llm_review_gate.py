#!/usr/bin/env python3
"""TLG-006 LLM reasonability review gate.

This gate consumes:
- unit_blueprint_v1 JSON
- tlg006_llm_review_report_v1 JSON
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCORE_KEYS = [
    "theme_coherence",
    "node_payload_alignment",
    "progression_logic",
    "task_authenticity",
    "redundancy_control",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_report_shape(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("version") != "tlg006_llm_review_report_v1":
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: version")
    if not isinstance(report.get("unit_id"), str) or not report.get("unit_id"):
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: unit_id")
    if report.get("overall_decision") not in {"pass", "revise", "fail"}:
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: overall_decision")

    scores = report.get("scores")
    if not isinstance(scores, dict):
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: scores")
    else:
        for key in SCORE_KEYS:
            v = scores.get(key)
            if not isinstance(v, int) or v < 1 or v > 5:
                errors.append(f"ERR_LLM_REVIEW_SCHEMA_INVALID: scores.{key}")

    if not isinstance(report.get("blocking_findings"), list):
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: blocking_findings")
    if not isinstance(report.get("node_reviews"), list) or not report.get("node_reviews"):
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: node_reviews")
    if not isinstance(report.get("summary_zh_tw"), str) or not report.get("summary_zh_tw").strip():
        errors.append("ERR_LLM_REVIEW_SCHEMA_INVALID: summary_zh_tw")
    return errors


def run_gate(blueprint: dict[str, Any], report: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    unit = blueprint.get("unit") or {}
    unit_id = str(unit.get("unit_id", ""))
    if str(report.get("unit_id", "")) != unit_id:
        errors.append(f"ERR_LLM_REVIEW_UNIT_ID_MISMATCH: report={report.get('unit_id')} blueprint={unit_id}")

    if report.get("overall_decision") == "fail":
        errors.append("ERR_LLM_REVIEW_DECISION_FAIL")

    scores = report.get("scores") or {}
    for key in SCORE_KEYS:
        score = int(scores.get(key, 0))
        if score < 4:
            errors.append(f"ERR_LLM_REVIEW_SCORE_TOO_LOW: {key}={score}")

    blocking_findings = report.get("blocking_findings") or []
    for finding in blocking_findings:
        if isinstance(finding, dict) and finding.get("severity") == "blocker":
            errors.append(
                "ERR_LLM_REVIEW_BLOCKING_FINDING: "
                f"{finding.get('code', 'UNKNOWN')} "
                f"{finding.get('node_id', '')} "
                f"{finding.get('message', '')}".strip()
            )

    expected_node_ids = {str(n.get("node_id", "")) for n in blueprint.get("sequence", []) if n.get("node_id")}
    reviewed_node_ids = {
        str(nr.get("node_id", ""))
        for nr in report.get("node_reviews", [])
        if isinstance(nr, dict) and nr.get("node_id")
    }
    missing = sorted(expected_node_ids - reviewed_node_ids)
    if missing:
        errors.append(f"ERR_LLM_REVIEW_NODE_COVERAGE_MISSING: {missing}")

    for nr in report.get("node_reviews", []):
        if not isinstance(nr, dict):
            continue
        verdict = nr.get("verdict")
        node_id = nr.get("node_id", "")
        if verdict == "needs_revision":
            warnings.append(f"WARN_LLM_REVIEW_NODE_NEEDS_REVISION: {node_id}")
        if verdict == "off_theme":
            errors.append(f"ERR_UNIT_THEME_DRIFT: {node_id}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LLM review gate on unit_blueprint_v1")
    parser.add_argument("--blueprint", required=True, help="Path to unit_blueprint_v1 JSON")
    parser.add_argument("--report", required=True, help="Path to tlg006_llm_review_report_v1 JSON")
    args = parser.parse_args()

    blueprint = load_json(Path(args.blueprint))
    report = load_json(Path(args.report))

    errors = validate_report_shape(report)
    warnings: list[str] = []
    if not errors:
        g_errors, g_warnings = run_gate(blueprint, report)
        errors.extend(g_errors)
        warnings.extend(g_warnings)

    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)

    if errors:
        print(f"TLG-006 LLM REVIEW RESULT: FAIL (errors={len(errors)}, warnings={len(warnings)})")
        return 1

    print(f"TLG-006 LLM REVIEW RESULT: PASS (warnings={len(warnings)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
