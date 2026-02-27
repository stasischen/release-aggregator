#!/usr/bin/env python3
"""Generate unit blueprint scaffold from a profile + template registry.

This keeps scaffold topology reusable while allowing locale/language overrides.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_template_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    templates = registry.get("templates") or []
    return {t["template_id"]: t for t in templates if "template_id" in t}


def apply_suffix(base_title: str, suffix: str | None) -> str:
    if not suffix:
        return base_title
    return f"{base_title}：{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate multilingual scaffold blueprint")
    parser.add_argument("--profile", required=True, help="Path to profile JSON")
    parser.add_argument("--templates", required=True, help="Path to template registry JSON")
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--title-zh-tw", required=True)
    parser.add_argument("--theme-zh-tw", required=True)
    parser.add_argument("--level", required=True)
    parser.add_argument("--target-language", default="ko")
    parser.add_argument("--learner-locale-source", default="zh-TW")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    profile = load_json(Path(args.profile))
    registry = load_json(Path(args.templates))
    template_map = build_template_map(registry)

    if args.level not in set(profile.get("target_levels") or []):
        raise SystemExit(f"level {args.level} not in profile.target_levels")

    suffix_to_node_id: dict[str, str] = {}
    for plan in profile.get("node_plan", []):
        suffix = plan["node_suffix"]
        suffix_to_node_id[suffix] = f"{args.unit_id}-{suffix}"

    sequence: list[dict[str, Any]] = []
    for plan in profile.get("node_plan", []):
        template_id = plan["template_id"]
        if template_id not in template_map:
            raise SystemExit(f"template_id not found: {template_id}")

        node = copy.deepcopy(template_map[template_id])
        node.pop("template_id", None)
        node["id"] = suffix_to_node_id[plan["node_suffix"]]
        node["title_zh_tw"] = apply_suffix(node.get("title_zh_tw", "未命名節點"), plan.get("title_suffix_zh_tw"))

        depends_on_suffixes = plan.get("depends_on_suffixes") or []
        if depends_on_suffixes:
            node["sequencing"] = {
                "depends_on_ids": [suffix_to_node_id[s] for s in depends_on_suffixes],
                "is_optional": bool(plan.get("optional", False)),
                "unlock_behavior": "after_dependencies",
            }

        if node.get("learning_role") in {"controlled_output", "immersion_output", "review_retrieval"}:
            node.setdefault(
                "resource_links",
                {
                    "lesson_ids": [],
                    "grammar_note_ids": [],
                    "dictionary_terms": [],
                    "tool_routes": ["/study/grammar-notes", "/study/dictionary"],
                },
            )

        sequence.append(node)

    blueprint = {
        "version": "unit_blueprint_v0",
        "adapter_contract": {
            "adapter_version": "frontend_unit_adapter_v0",
            "stability": "proposed",
            "fallback_locale_order": [args.learner_locale_source, "en"],
            "notes": f"Generated from profile {profile.get('profile_id')} ({profile.get('version')}).",
        },
        "unit": {
            "unit_id": args.unit_id,
            "title_zh_tw": args.title_zh_tw,
            "target_language": args.target_language,
            "learner_locale_source": args.learner_locale_source,
            "level": args.level,
            "theme_zh_tw": args.theme_zh_tw,
            "output_ratio_target": profile.get("default_output_ratio_target", 0.5),
            "can_do_zh_tw": [
                f"TODO: can-do #1 for {args.title_zh_tw}",
                f"TODO: can-do #2 for {args.title_zh_tw}",
            ],
        },
        "sequence": sequence,
        "scheduled_followups": [],
        "scaffold_meta": {
            "profile_id": profile.get("profile_id"),
            "profile_version": profile.get("version"),
            "template_registry_id": registry.get("registry_id"),
            "template_registry_version": registry.get("version"),
            "constraints": profile.get("constraints", {}),
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Generated scaffold: {output_path}")
    print(f"Nodes: {len(sequence)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
