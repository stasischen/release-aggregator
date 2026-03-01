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
BASE_REGISTERS = {"spoken_casual", "spoken_polite", "formal_written", "neutral_written"}

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

CONTENT_FORM_TO_GENRE = {
    "dialogue": "dialogue",
    "comprehension_check": "dialogue",
    "notice": "notice",
    "message_thread": "message",
    "functional_phrase_pack": "dialogue",
    "pattern_card": "dialogue",
    "grammar_note": "article",
    "practice_card": "dialogue",
    "roleplay_prompt": "dialogue",
    "message_prompt": "message",
    "review_card": "dialogue",
}

NODE_COPY_BOOK = {
    "L1": ("沉浸輸入", "建立第一輪情境聽讀理解", "能辨識該情境的核心開場與任務語句"),
    "L2": ("理解檢核", "確認是否讀懂關鍵資訊", "能針對輸入做正確判斷與回應"),
    "L3": ("閱讀輸入", "補足非對話文本的資訊抓取", "能從文本提取場景關鍵資訊"),
    "D1": ("功能詞塊", "把句型拆成可替換詞塊", "能替換關鍵 slot 組出新句"),
    "G1": ("句型框", "固定核心句型框架", "能套用框架產出多個同功能句"),
    "G2": ("文法重點", "說清楚規則與常見錯誤", "能在提問與回應中保持語法穩定"),
    "P1": ("組裝練習", "把詞塊組成可用句", "能在提示下產出完整句子"),
    "P2": ("情境應答", "在場景中快速選擇回應", "能依語境回覆正確功能句"),
    "P3": ("變換練習", "做肯定/否定或語體轉換", "能在限制條件下完成句型變換"),
    "P4": ("修復練習", "遇到卡關時主動修復溝通", "能使用修復句維持互動"),
    "P5": ("角色扮演", "整合多句完成任務對話", "能在模擬情境完成多輪互動"),
    "P6": ("訊息任務", "把功能句遷移到文字溝通", "能用短訊息完成同任務"),
    "R1": ("回想複習", "不看提示回想核心句型", "能獨立提取本課關鍵表達"),
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


def resolve_lang_profile_path(target_lang: str, explicit_path: str | None) -> Path:
    if explicit_path:
        return Path(explicit_path)
    return Path(f"docs/tasks/lang_profiles/{target_lang}_generation_profile_v1.json")


def normalize_register_id(register_id: str) -> str:
    return register_id.strip()


def build_lang_indexes(lang_profile: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    registers = {}
    for rp in lang_profile.get("register_profiles", []):
        rid = normalize_register_id(str(rp.get("register_id", "")))
        if rid:
            registers[rid] = rp
    genres = {}
    for gp in lang_profile.get("genre_style_profiles", []):
        genre = str(gp.get("genre", "")).strip()
        if genre:
            genres[genre] = gp
    return registers, genres


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


def build_node_copy(
    node_id: str,
    can_do: str,
    frame: str,
    unit_theme_zh_tw: str,
    storyline_step_zh_tw: str,
) -> tuple[str, str, str, str]:
    suffix = suffix_of(node_id)
    stage, desc, expected = NODE_COPY_BOOK.get(suffix, ("節點", "完成本節點任務", "能達成該節點輸出"))
    focus = (can_do or "完成本課核心溝通任務").strip()
    if focus.endswith(("。", ".", "!", "?")):
        focus = focus[:-1]
    theme = unit_theme_zh_tw or "本單元主題"
    storyline = storyline_step_zh_tw.strip()

    title_zh = f"{suffix} {stage}：{storyline if storyline else focus}"
    if storyline:
        summary_zh = f"{desc}。主題情境：{theme}。劇情步驟：{storyline}。本節點語言目標：{focus}。"
    else:
        summary_zh = f"{desc}。主題情境：{theme}。本節點聚焦：{focus}。"
    expected_zh = f"{expected}。對應功能：{focus}。"
    summary_en = f"{suffix} focuses on: {focus}"
    if frame:
        summary_en = f"{summary_en} | frame: {frame}"
    return title_zh, summary_zh, expected_zh, summary_en


def build_node_contract(
    node_id: str,
    can_do: str,
) -> dict[str, str]:
    suffix = suffix_of(node_id)
    chain = {
        "L1": ("unit_intent", "L2"),
        "L2": ("L1", "L3"),
        "L3": ("L2", "D1"),
        "D1": ("L1~L3", "G1"),
        "G1": ("D1", "G2"),
        "G2": ("G1", "P1"),
        "P1": ("G1/G2", "P2"),
        "P2": ("P1", "P3"),
        "P3": ("P2", "P4"),
        "P4": ("P1~P3", "P5"),
        "P5": ("P1~P4", "P6"),
        "P6": ("P5", "R1"),
        "R1": ("P1~P6", "followups"),
    }
    incoming, outgoing = chain.get(suffix, ("previous_node", "next_node"))
    return {
        "node_goal_zh_tw": can_do or "完成節點任務",
        "input_from_prev": incoming,
        "output_to_next": outgoing,
    }


def attach_reading_overlay(sequence: list[dict[str, Any]], reading_overlay: dict[str, Any] | None) -> None:
    if not reading_overlay:
        return
    by_node = {n.get("node_id"): n for n in reading_overlay.get("reading_nodes", []) if isinstance(n, dict)}
    for node in sequence:
        node_id = node.get("node_id")
        if node_id in by_node:
            node.setdefault("payload", {})["reading_overlay"] = by_node[node_id]


def build_node_generation_constraints(
    target_lang: str,
    content_form: str,
    unit_content_genre: str,
    register_target: str | None,
    lang_profile: dict[str, Any],
    register_map: dict[str, dict[str, Any]],
    genre_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    resolved_genre = CONTENT_FORM_TO_GENRE.get(content_form, unit_content_genre)
    genre_profile = genre_map.get(resolved_genre) or {}
    resolved_register = normalize_register_id(register_target or str(genre_profile.get("default_register", "")))

    if resolved_register and resolved_register not in register_map:
        raise ValueError(f"Unknown register_target '{resolved_register}' for target_lang={target_lang}")
    if resolved_genre not in set(lang_profile.get("supported_genres", [])):
        raise ValueError(f"Unsupported genre '{resolved_genre}' for target_lang={target_lang}")

    register_profile = register_map.get(resolved_register, {})
    prompt_policy = lang_profile.get("prompt_policy", {})
    return {
        "target_lang": target_lang,
        "genre": resolved_genre,
        "register_target": resolved_register,
        "style_requirements": genre_profile.get("style_requirements", []),
        "style_anti_patterns": genre_profile.get("style_anti_patterns", []),
        "required_markers": register_profile.get("required_markers", []),
        "forbidden_markers": register_profile.get("forbidden_markers", []),
        "length_guidelines": genre_profile.get("length_guidelines", {}),
        "prompt_policy": {
            "must_use_target_lang_only": bool(prompt_policy.get("must_use_target_lang_only", True)),
            "must_follow_genre_style": bool(prompt_policy.get("must_follow_genre_style", True)),
            "must_follow_register_constraints": bool(prompt_policy.get("must_follow_register_constraints", True)),
        },
    }


def build_blueprint(
    base_input: dict[str, Any],
    pattern_library: dict[str, Any],
    default_support_lang: str,
    reading_overlay: dict[str, Any] | None,
    lang_profile: dict[str, Any],
    content_genre: str,
    register_target: str | None,
) -> dict[str, Any]:
    pattern_map = build_pattern_map(pattern_library)
    register_map, genre_map = build_lang_indexes(lang_profile)
    sequence: list[dict[str, Any]] = []
    unit_intent = base_input.get("unit_intent") or {}
    unit_theme_zh_tw = str(unit_intent.get("theme_zh_tw", "")).strip()
    node_storyline = unit_intent.get("node_storyline") or {}

    for node in base_input.get("nodes", []):
        node_id = str(node.get("node_id", ""))
        suffix = suffix_of(node_id)
        profile = NODE_PROFILES.get(suffix, {"learning_role": "controlled_output", "content_form": "practice_card"})
        content_form = profile["content_form"]

        pattern_id = str(node.get("pattern_id", ""))
        pattern_entry = pattern_map.get(pattern_id)
        summary_target, summary_zh, summary_en = make_node_summary(pattern_entry)
        can_do = str((pattern_entry or {}).get("can_do", "")).strip()
        title_zh, generated_summary_zh, expected_zh, generated_summary_en = build_node_copy(
            node_id=node_id,
            can_do=can_do,
            frame=summary_target,
            unit_theme_zh_tw=unit_theme_zh_tw,
            storyline_step_zh_tw=str(node_storyline.get(node_id, "")).strip(),
        )

        payload = dict(node.get("payload") or {})
        payload["node_contract"] = build_node_contract(node_id=node_id, can_do=can_do)
        payload["generation_constraints"] = build_node_generation_constraints(
            target_lang=str(base_input.get("target_lang", "ko")),
            content_form=content_form,
            unit_content_genre=content_genre,
            register_target=register_target,
            lang_profile=lang_profile,
            register_map=register_map,
            genre_map=genre_map,
        )
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
                "content_form": content_form,
                "output_mode": node.get("output_mode", "none"),
                "title_zh_tw": title_zh,
                "summary_target_lang": summary_target,
                "summary_zh_tw": generated_summary_zh if generated_summary_zh else summary_zh,
                "summary_en": generated_summary_en if generated_summary_en else summary_en,
                "expected_output_zh_tw": expected_zh,
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
            "content_genre": content_genre,
            "register_target": normalize_register_id(register_target or ""),
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
    parser.add_argument("--lang-profile", help="Optional path to lang_generation_profile_v1 JSON; defaults to target_lang profile")
    parser.add_argument("--content-genre", default="dialogue", choices=["dialogue", "article", "notice", "email", "message", "report", "story"])
    parser.add_argument("--register-target", help="Optional register target; if omitted, per-genre default is used from lang profile")
    args = parser.parse_args()

    base_input = load_json(Path(args.input))
    pattern_library = load_json(Path(args.pattern_library))
    reading_overlay = load_json(Path(args.reading_overlay)) if args.reading_overlay else None
    target_lang = str(base_input.get("target_lang", "")).strip()
    if not target_lang:
        raise ValueError("Input JSON missing target_lang")
    lang_profile_path = resolve_lang_profile_path(target_lang, args.lang_profile)
    if not lang_profile_path.exists():
        raise FileNotFoundError(f"Language profile not found: {lang_profile_path}")
    lang_profile = load_json(lang_profile_path)
    if str(lang_profile.get("target_lang", "")).strip() != target_lang:
        raise ValueError(f"Language profile target_lang mismatch: input={target_lang}, profile={lang_profile.get('target_lang')}")

    blueprint = build_blueprint(
        base_input,
        pattern_library,
        args.default_support_lang,
        reading_overlay,
        lang_profile,
        args.content_genre,
        args.register_target,
    )
    blueprint["lang_profile_ref"] = str(lang_profile_path)

    suffixes = {suffix_of(n.get("node_id", "")) for n in blueprint.get("sequence", [])}
    missing = [s for s in MANDATORY_SUFFIXES if s not in suffixes]
    if missing:
        print(f"Warning: missing mandatory node suffixes in generated sequence: {missing}")

    save_json(Path(args.output), blueprint)
    print(f"Wrote unit blueprint: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
