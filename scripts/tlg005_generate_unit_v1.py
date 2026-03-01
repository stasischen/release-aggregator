#!/usr/bin/env python3
"""TLG-005 generator starter for unit_blueprint_v1.

Inputs:
- base generator input (tlg005_generator_input_v1)
- pattern library (TLG-004)
- optional reading overlay input (tlg005_reading_generator_input_v1)

Output:
- unit_blueprint_v1 draft JSON
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MANDATORY_SUFFIXES = ["L1", "L2", "L3", "D1", "G1", "G2", "P1", "P2", "P3", "P4", "P5", "P6", "R1"]

NODE_PROFILES = {
    "L1": {"learning_role": "immersion_input", "content_form": "dialogue"},
    "L2": {"learning_role": "immersion_input", "content_form": "comprehension_check"},
    "L3": {"learning_role": "immersion_input", "content_form": "notice"},
    "D1": {"learning_role": "structure_pattern", "content_form": "functional_phrase_pack"},
    "G1": {"learning_role": "structure_pattern", "content_form": "pattern_card"},
    "G2": {"learning_role": "structure_grammar", "content_form": "grammar_note"},
    "P1": {"learning_role": "controlled_output", "content_form": "practice_card"},
    "P2": {"learning_role": "controlled_output", "content_form": "practice_card"},
    "P3": {"learning_role": "controlled_output", "content_form": "practice_card"},
    "P4": {"learning_role": "controlled_output", "content_form": "practice_card"},
    "P5": {"learning_role": "immersion_output", "content_form": "roleplay_prompt"},
    "P6": {"learning_role": "immersion_output", "content_form": "message_prompt"},
    "R1": {"learning_role": "review_retrieval", "content_form": "review_card"},
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def suffix_of(node_id: str) -> str:
    return node_id.split("-")[-1]


def build_pattern_map(pattern_library: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for entry in pattern_library.get("entries", []):
        pid = entry.get("pattern_id")
        if isinstance(pid, str):
            out[pid] = entry
    return out


def make_node_summary(pattern_entry: dict[str, Any] | None) -> tuple[str, str, str]:
    if not pattern_entry:
        return "", "", ""
    frame = str(pattern_entry.get("frame", "")).strip()
    zh = str((pattern_entry.get("teaching_notes") or {}).get("zh_tw", "")).strip()
    en = str((pattern_entry.get("teaching_notes") or {}).get("en", "")).strip()
    return frame, zh, en


def attach_reading_overlay(sequence: list[dict[str, Any]], reading_overlay: dict[str, Any] | None) -> None:
    if not reading_overlay:
        return
    by_node = {n.get("node_id"): n for n in reading_overlay.get("reading_nodes", []) if isinstance(n, dict)}
    for node in sequence:
        node_id = node.get("node_id")
        if node_id in by_node:
            node.setdefault("payload", {})["reading_overlay"] = by_node[node_id]


def build_blueprint(base_input: dict[str, Any], pattern_library: dict[str, Any], default_support_lang: str, reading_overlay: dict[str, Any] | None) -> dict[str, Any]:
    pattern_map = build_pattern_map(pattern_library)
    sequence: list[dict[str, Any]] = []

    for node in base_input.get("nodes", []):
        node_id = str(node.get("node_id", ""))
        suffix = suffix_of(node_id)
        profile = NODE_PROFILES.get(suffix, {"learning_role": "controlled_output", "content_form": "practice_card"})

        pattern_id = str(node.get("pattern_id", ""))
        pattern_entry = pattern_map.get(pattern_id)
        summary_target, summary_zh, summary_en = make_node_summary(pattern_entry)

        payload = dict(node.get("payload") or {})
        if pattern_entry:
            payload["pattern_meta"] = {
                "pattern_id": pattern_id,
                "can_do": pattern_entry.get("can_do", ""),
                "required_elements": pattern_entry.get("required_elements", []),
                "acceptable_variants": pattern_entry.get("acceptable_variants", []),
                "transform_types": pattern_entry.get("transform_types", []),
                "repair_links": pattern_entry.get("repair_links", []),
                "transfer_contexts": pattern_entry.get("transfer_contexts", []),
            }

        sequence.append(
            {
                "node_id": node_id,
                "learning_role": profile["learning_role"],
                "content_form": profile["content_form"],
                "output_mode": node.get("output_mode", "none"),
                "summary_target_lang": summary_target,
                "summary_zh_tw": summary_zh,
                "summary_en": summary_en,
                "payload": payload,
            }
        )

    attach_reading_overlay(sequence, reading_overlay)

    used_pattern_ids = [str(n.get("pattern_id", "")) for n in base_input.get("nodes", []) if n.get("pattern_id")]
    unique_pattern_ids = sorted(set(used_pattern_ids))

    skill_targets = []
    for i, pid in enumerate(unique_pattern_ids, start=1):
        entry = pattern_map.get(pid)
        if not entry:
            continue
        skill_targets.append(
            {
                "skill_id": f"SK-{i:03d}",
                "can_do": entry.get("can_do", ""),
                "pattern_refs": [pid],
                "success_criteria": entry.get("required_elements", []),
                "transfer_contexts": entry.get("transfer_contexts", []),
            }
        )

    can_do = [st["can_do"] for st in skill_targets if st.get("can_do")]

    return {
        "version": "unit_blueprint_v1",
        "adapter_version": "frontend_unit_adapter_v1",
        "unit": {
            "unit_id": base_input.get("unit_id", ""),
            "level": base_input.get("level", "A1"),
            "target_lang": base_input.get("target_lang", "ko"),
            "support_langs": ["zh_tw", "en"],
            "default_support_lang": default_support_lang,
            "can_do": can_do,
            "skill_targets": skill_targets,
        },
        "sequence": sequence,
        "scheduled_followups": [
            {
                "timing": "+1_unit",
                "followup_type": "review",
                "goal_target_lang": "retrieve core pattern and respond accurately",
                "goal_zh_tw": "回想核心句型並正確回應",
                "goal_en": "retrieve core pattern and respond accurately",
                "retrieval_targets": unique_pattern_ids[:3],
            },
            {
                "timing": "+3_units",
                "followup_type": "transfer",
                "goal_target_lang": "transfer pattern to a new context",
                "goal_zh_tw": "把句型遷移到新情境",
                "goal_en": "transfer pattern to a new context",
                "retrieval_targets": unique_pattern_ids[:3],
            },
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate unit_blueprint_v1 draft from TLG inputs")
    parser.add_argument("--input", required=True, help="Path to tlg005_generator_input_v1 JSON")
    parser.add_argument("--pattern-library", required=True, help="Path to TLG-004 pattern library JSON")
    parser.add_argument("--output", required=True, help="Output path for unit_blueprint_v1 JSON")
    parser.add_argument("--reading-overlay", help="Optional path to tlg005_reading_generator_input_v1 JSON")
    parser.add_argument("--default-support-lang", default="zh_tw", choices=["zh_tw", "en"])
    args = parser.parse_args()

    base_input = load_json(Path(args.input))
    pattern_library = load_json(Path(args.pattern_library))
    reading_overlay = load_json(Path(args.reading_overlay)) if args.reading_overlay else None

    blueprint = build_blueprint(base_input, pattern_library, args.default_support_lang, reading_overlay)

    suffixes = {suffix_of(n.get("node_id", "")) for n in blueprint.get("sequence", [])}
    missing = [s for s in MANDATORY_SUFFIXES if s not in suffixes]
    if missing:
        print(f"Warning: missing mandatory node suffixes in generated sequence: {missing}")

    save_json(Path(args.output), blueprint)
    print(f"Wrote unit blueprint: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
