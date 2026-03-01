#!/usr/bin/env python3
"""Convert unit_blueprint_v1 to modular viewer preview fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


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


def map_duration_min(suffix: str) -> int:
    if suffix.startswith("L"):
        return 4
    if suffix in {"D1", "G1", "G2"}:
        return 5
    if suffix in {"P5", "P6"}:
        return 6
    return 4


def map_skill_focus(content_form: str) -> list[str]:
    if content_form in {"dialogue", "comprehension_check", "notice", "review_card"}:
        return ["listening", "reading"]
    if content_form in {"roleplay_prompt"}:
        return ["speaking"]
    if content_form in {"message_prompt"}:
        return ["writing"]
    return ["speaking", "writing"]


def map_candidate_type(content_form: str) -> str:
    if content_form == "functional_phrase_pack":
        return "dictionary_pack"
    if content_form in {"pattern_card", "grammar_note"}:
        return "grammar_note"
    return "path_node"


def ensure_minimal_payload(node: dict[str, Any]) -> dict[str, Any]:
    payload = dict(node.get("payload") or {})
    content_form = str(node.get("content_form", "")).strip()
    summary_target = str(node.get("summary_target_lang", "")).strip() or "..."
    summary_zh = str(node.get("summary_zh_tw", "")).strip() or "..."
    title_zh = str(node.get("title_zh_tw", "")).strip() or "本節點任務"
    node_contract = payload.get("node_contract") or {}
    node_goal = str(node_contract.get("node_goal_zh_tw", "")).strip() or "完成本節點任務"

    if content_form == "dialogue":
        payload.setdefault(
            "dialogue_turns",
            [
                {"speaker": "A", "text": summary_target, "zh_tw": f"{title_zh}：{summary_zh}"},
                {"speaker": "B", "text": "네, 알겠습니다.", "zh_tw": "好，我明白了。"},
            ],
        )
    elif content_form == "comprehension_check":
        payload.setdefault(
            "items",
            [
                {
                    "prompt_ko": summary_target,
                    "prompt_zh_tw": f"{title_zh}：根據報到情境作答（目標：{node_goal}）。",
                    "response_choices_ko": ["네", "아니요"],
                    "accepted_responses_ko": ["네"],
                }
            ],
        )
    elif content_form == "notice":
        payload.setdefault("notice_items", [summary_target])
        payload.setdefault("notice_items_zh_tw", [f"{title_zh}：{summary_zh}"])
    elif content_form == "functional_phrase_pack":
        payload.setdefault("tasks", [{"prompt_zh_tw": f"{title_zh}：用本節詞塊完成「{node_goal}」相關組句。"}])
    elif content_form == "pattern_card":
        payload.setdefault("frame", summary_target)
        payload.setdefault("usage_hint_zh_tw", f"{title_zh}：優先用此句型完成「{node_goal}」。")
    elif content_form in {"roleplay_prompt", "message_prompt"}:
        payload.setdefault("prompt_zh_tw", f"{title_zh}：請依照情境完成輸出（必須達成：{node_goal}）。")
    elif content_form == "review_card":
        payload.setdefault(
            "prompts_zh_tw",
            [
                f"{title_zh}：不用看提示，先說出一個可完成「{node_goal}」的句子。",
                "再說一個同主題但不同詞彙的變化句。",
            ],
        )
        payload.setdefault("reference_answers_ko", [summary_target])

    return payload


def convert(source: dict[str, Any], title_zh_tw: str, theme_zh_tw: str) -> dict[str, Any]:
    unit = source.get("unit") or {}
    sequence = source.get("sequence") or []

    out_sequence = []
    for node in sequence:
        node_id = str(node.get("node_id", "")).strip()
        suffix = suffix_of(node_id)
        content_form = str(node.get("content_form", "")).strip()
        output_mode = str(node.get("output_mode", "none")).strip() or "none"

        out_sequence.append(
            {
                "id": node_id,
                "candidate_type": map_candidate_type(content_form),
                "content_form": content_form,
                "learning_role": node.get("learning_role", "controlled_output"),
                "skill_focus": map_skill_focus(content_form),
                "output_mode": output_mode,
                "duration_min": map_duration_min(suffix),
                "title_zh_tw": node.get("title_zh_tw") or f"{suffix} 節點任務",
                "summary_zh_tw": node.get("summary_zh_tw") or "完成本節點任務。",
                "expected_output_zh_tw": node.get("expected_output_zh_tw") or "達成本節點輸出目標。",
                "payload": ensure_minimal_payload(node),
                "adapter_hints": {
                    "content_renderer_key": content_form,
                    "interaction_renderer_key": None if output_mode == "none" else output_mode,
                },
            }
        )

    return {
        "version": "unit_blueprint_v0.1",
        "adapter_contract": {
            "adapter_version": "frontend_unit_adapter_v0",
            "stability": "preview_v1_compat",
            "fallback_locale_order": ["zh_tw", "en"],
            "notes": "Converted from unit_blueprint_v1 with node-contract-first copy.",
        },
        "unit": {
            "unit_id": unit.get("unit_id", ""),
            "title_zh_tw": title_zh_tw,
            "target_language": unit.get("target_lang", "ko"),
            "learner_locale_source": unit.get("default_support_lang", "zh_tw"),
            "level": unit.get("level", "A1"),
            "theme_zh_tw": theme_zh_tw,
            "output_ratio_target": 0.5,
            "can_do_zh_tw": unit.get("can_do", []),
        },
        "sequence": out_sequence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert unit_blueprint_v1 to modular viewer fixture")
    parser.add_argument("--input", required=True, help="Path to unit_blueprint_v1 JSON")
    parser.add_argument("--output", required=True, help="Output fixture path")
    parser.add_argument("--title-zh-tw", required=True, help="Unit title for viewer")
    parser.add_argument("--theme-zh-tw", required=True, help="Unit theme for viewer")
    args = parser.parse_args()

    source = load_json(Path(args.input))
    output = convert(source, args.title_zh_tw, args.theme_zh_tw)
    save_json(Path(args.output), output)
    print(f"Wrote modular preview fixture: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
