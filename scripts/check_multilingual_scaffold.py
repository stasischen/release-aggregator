#!/usr/bin/env python3
"""Check scaffold blueprint against profile constraints.

Focus: modular production gates (coverage/sequencing/resource links), not content quality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_ROLES = {"controlled_output", "immersion_output", "review_retrieval"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate scaffold contract readiness")
    parser.add_argument("--blueprint", required=True)
    parser.add_argument("--profile", required=True)
    args = parser.parse_args()

    blueprint = load_json(Path(args.blueprint))
    profile = load_json(Path(args.profile))

    sequence = blueprint.get("sequence") or []
    constraints = profile.get("constraints") or {}

    errors: list[str] = []
    warnings: list[str] = []

    min_node_count = int(constraints.get("min_node_count", 1))
    if len(sequence) < min_node_count:
        errors.append(f"MIN_NODE_COUNT failed: {len(sequence)} < {min_node_count}")

    roles_present = {n.get("learning_role") for n in sequence}
    for role in constraints.get("required_learning_roles") or []:
        if role not in roles_present:
            errors.append(f"MISSING_ROLE: {role}")

    output_mode_counts: dict[str, int] = {}
    for node in sequence:
        mode = node.get("output_mode")
        if not isinstance(mode, str):
            continue
        output_mode_counts[mode] = output_mode_counts.get(mode, 0) + 1

    for mode, target in (constraints.get("output_mode_targets") or {}).items():
        count = output_mode_counts.get(mode, 0)
        if count < int(target):
            errors.append(f"OUTPUT_MODE_TARGET unmet: {mode}={count}, need >= {target}")

    id_set = {n.get("id") for n in sequence if n.get("id")}
    for node in sequence:
        node_id = node.get("id", "<unknown>")
        seq = node.get("sequencing") or {}
        deps = seq.get("depends_on_ids") or []
        for dep in deps:
            if dep not in id_set:
                errors.append(f"BAD_DEPENDENCY: {node_id} depends on missing id {dep}")

        if node.get("learning_role") in OUTPUT_ROLES:
            links = node.get("resource_links")
            if constraints.get("require_resource_links_for_output_nodes", False):
                if not isinstance(links, dict):
                    errors.append(f"MISSING_RESOURCE_LINKS: {node_id}")
                else:
                    has_any = any(
                        bool(links.get(k)) for k in ("lesson_ids", "grammar_note_ids", "dictionary_terms")
                    )
                    if not has_any:
                        warnings.append(f"THIN_RESOURCE_LINKS: {node_id} has no lesson/grammar/dictionary links")

    if errors:
        print("Scaffold check FAILED")
        for err in errors:
            print(f"- ERROR: {err}")
        for warn in warnings:
            print(f"- WARN: {warn}")
        return 1

    print("Scaffold check OK")
    for warn in warnings:
        print(f"- WARN: {warn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
