#!/usr/bin/env python3
"""Normalize unit_blueprint_v1 for viewer-readiness and goal/payload alignment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_node(node: dict[str, Any]) -> None:
    payload = node.setdefault("payload", {})
    node_contract = payload.setdefault("node_contract", {})
    form = str(node.get("content_form", "")).strip()
    mode = str(node.get("output_mode", "none")).strip()

    goal = str(node_contract.get("node_goal_zh_tw", "")).strip()
    if form == "comprehension_check":
        payload.setdefault("question_type", "detail")
        payload.setdefault("items", [])
        if any(k in goal for k in ["詢問", "回答", "表達", "說明"]):
            node_contract["node_goal_zh_tw"] = "能聽懂並判斷關鍵資訊。"
    elif form == "notice":
        payload.setdefault("notice_items", [])
        payload.setdefault("notice_items_zh_tw", [])
        if any(k in goal for k in ["詢問", "回答"]):
            node_contract["node_goal_zh_tw"] = "能從文本提取地點與規則資訊。"
    elif form == "review_card":
        payload.setdefault("target_type", "sentence_recall")
        payload.setdefault("retrieval_focus", "core_patterns")
        payload.setdefault("prompts_zh_tw", [])
        payload.setdefault("reference_answers_ko", [])
    elif form == "pattern_card":
        payload.setdefault("frames", [])
    elif form == "grammar_note":
        payload.setdefault("sections", [])
    elif form == "functional_phrase_pack":
        payload.setdefault("sections", [])
    elif form == "dialogue":
        payload.setdefault("dialogue_turns", [])
    elif form == "roleplay_prompt":
        payload.setdefault("scenery_zh_tw", "")
        payload.setdefault("constraints_zh_tw", [])
        payload.setdefault("required_patterns_zh_tw", [])
        payload.setdefault("prompt_zh_tw", payload.get("prompt_zh_tw", "依照情境完成口說任務。"))
    elif form == "message_prompt":
        payload.setdefault("prompt_zh_tw", "請依照情境完成訊息輸出。")
        payload.setdefault("must_include_zh_tw", [])
        payload.setdefault("example_shape_ko", [])

    if mode == "pattern_transform":
        payload.setdefault("transform_type", "slot_substitution")
        payload.setdefault("prompt_zh_tw", node.get("summary_zh_tw", "請完成句型變換。"))
    if mode == "guided":
        payload.setdefault("prompt_zh_tw", node.get("summary_zh_tw", "請依照任務輸出。"))
    if mode == "response_builder":
        payload.setdefault("items", payload.get("items", []))
    if mode == "chunk_assembly":
        payload.setdefault("tasks", payload.get("tasks", []))
    if mode == "frame_fill":
        if "frames" not in payload and "frame" in payload:
            payload["frames"] = [{"frame": payload.get("frame", ""), "use_zh_tw": "以 slot 替換完成句子。", "slots_zh_tw": []}]
        payload.setdefault("frames", payload.get("frames", []))


def normalize(blueprint: dict[str, Any]) -> dict[str, Any]:
    sequence = blueprint.get("sequence", [])
    for node in sequence:
        if isinstance(node, dict):
            normalize_node(node)

    # Cross-node grounding: L2 comprehension must anchor to L1 dialogue.
    l1 = next((n for n in sequence if str(n.get("node_id", "")).endswith("-L1")), None)
    l2 = next((n for n in sequence if str(n.get("node_id", "")).endswith("-L2")), None)
    if isinstance(l1, dict) and isinstance(l2, dict):
        l1_turns = ((l1.get("payload") or {}).get("dialogue_turns") or [])
        l1_lines = [str(t.get("text", "")).strip() for t in l1_turns if isinstance(t, dict) and str(t.get("text", "")).strip()]
        anchor_line = next((ln for ln in l1_lines if "?" in ln or "요?" in ln), l1_lines[0] if l1_lines else "")

        l2_payload = l2.setdefault("payload", {})
        l2_payload.setdefault("question_type", "detail_from_l1")
        l2_payload["source_anchor_node_id"] = str(l1.get("node_id", ""))
        if anchor_line:
            l2_payload["source_anchor_line"] = anchor_line

        items = l2_payload.get("items")
        if not isinstance(items, list) or not items:
            items = [{}]
            l2_payload["items"] = items

        for item in items:
            if not isinstance(item, dict):
                continue
            if "question_ko" in item and "prompt_ko" not in item:
                item["prompt_ko"] = item.get("question_ko", "")
            if "question_zh_tw" in item and "prompt_zh_tw" not in item:
                item["prompt_zh_tw"] = item.get("question_zh_tw", "")
            if "choices" in item and "response_choices_ko" not in item:
                choices = item.get("choices") or []
                if isinstance(choices, list):
                    item["response_choices_ko"] = [
                        str(c.get("text_ko", "")).strip()
                        for c in choices
                        if isinstance(c, dict) and str(c.get("text_ko", "")).strip()
                    ]

            prompt_ko = str(item.get("prompt_ko", "")).strip()
            if not prompt_ko or (anchor_line and prompt_ko not in anchor_line and anchor_line not in prompt_ko):
                item["prompt_ko"] = anchor_line or prompt_ko or "이 대화에서 핵심 질문은 무엇이에요?"
                item["prompt_zh_tw"] = "根據 L1 對話內容作答。"
            item.setdefault("response_choices_ko", ["네", "아니요"])
            item.setdefault("accepted_responses_ko", ["네"])
            for k in ["question_ko", "question_zh_tw", "choices", "explanation_ko", "explanation_zh_tw"]:
                if k in item:
                    item.pop(k, None)
    return blueprint


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize unit_blueprint_v1")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = load_json(Path(args.input))
    out = normalize(data)
    save_json(Path(args.output), out)
    print(f"Wrote normalized blueprint: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
