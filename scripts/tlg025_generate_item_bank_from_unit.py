#!/usr/bin/env python3
"""Generate a simple item bank from a modular viewer unit fixture."""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def has_hangul(text: str) -> bool:
    return bool(re.search(r"[\uac00-\ud7a3]", text))


def has_han(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def normalize_md(text: str) -> str:
    s = re.sub(r"[*`_#>\[\]\(\)]", "", text)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def collect_dialogue_turns(unit_data: dict):
    turns = []
    for node in unit_data.get("sequence", []):
        if node.get("content_form") != "dialogue":
            continue
        for turn in node.get("payload", {}).get("dialogue_turns", []):
            ko = str(turn.get("text", "")).strip()
            zh = str(turn.get("zh_tw", "")).strip()
            if ko:
                turns.append({"node_id": node.get("id", "node"), "ko": ko, "zh": zh})
    return turns


def collect_grammar_sections(unit_data: dict):
    node = next((n for n in unit_data.get("sequence", []) if n.get("content_form") == "grammar_note"), None)
    if not node:
        return None, []
    sections = node.get("payload", {}).get("sections", []) or []
    return node, sections


def extract_ko_zh_pairs_from_sections(sections: list[dict]) -> list[tuple[str, str]]:
    pairs = []
    seen = set()
    for section in sections:
        for point in section.get("points_zh_tw", []) or []:
            line = normalize_md(str(point))
            if not line:
                continue

            # Pattern: 한국어 / 中文 / ...
            if "/" in line:
                chunks = [c.strip() for c in line.split("/") if c.strip()]
                if len(chunks) >= 2 and has_hangul(chunks[0]):
                    ko = chunks[0]
                    zh = chunks[1]
                    if has_han(ko) or has_hangul(zh):
                        continue
                    key = (ko, zh)
                    if key not in seen:
                        pairs.append(key)
                        seen.add(key)

            # Pattern: 한국어 (中文)
            m = re.search(r"([\uac00-\ud7a3][^()]{0,40})\(([^()]{1,40})\)", line)
            if m:
                ko = m.group(1).strip()
                zh = m.group(2).strip()
                if ko and zh and has_hangul(ko) and (not has_han(ko)) and (not has_hangul(zh)):
                    key = (ko, zh)
                    if key not in seen:
                        pairs.append(key)
                        seen.add(key)
    return pairs


def choose_cloze_token(sentence: str, vocab_pool: list[str]) -> tuple[str, list[str]] | None:
    tokens = [t for t in sentence.split() if has_hangul(t) and len(t) >= 2]
    if not tokens:
        return None
    answer = max(tokens, key=len)
    distractors = [w for w in vocab_pool if w != answer]
    random.shuffle(distractors)
    choices = [answer] + distractors[:2]
    random.shuffle(choices)
    return answer, choices


def base_linked_refs(lesson_id: str, node_id: str):
    return {
        "lesson_id": lesson_id,
        "node_id": node_id,
        "grammar_ids": [],
        "pattern_ids": [],
        "function_ids": []
    }


def build_items(unit_data: dict, seed: int = 42, max_items: int = 24):
    random.seed(seed)
    lesson_id = unit_data.get("unit", {}).get("unit_id", "UNKNOWN")
    items = []
    counter = 1

    dialogue_turns = collect_dialogue_turns(unit_data)
    grammar_node, grammar_sections = collect_grammar_sections(unit_data)
    ko_zh_pairs = extract_ko_zh_pairs_from_sections(grammar_sections)
    vocab_pool = []
    for t in dialogue_turns:
        vocab_pool.extend([w for w in t["ko"].split() if has_hangul(w) and len(w) >= 2])
    vocab_pool = list(dict.fromkeys(vocab_pool))
    item_type_counts = {"mcq_meaning": 0, "cloze": 0, "transform": 0, "retrieval": 0}
    mcq_cap = max(4, min(8, max_items // 3))
    cloze_cap = max(8, min(12, max_items // 2))
    transform_cap = max(4, max_items // 6)
    retrieval_cap = max(2, max_items // 8)

    # 1) Meaning MCQ from grammar glossary-like pairs (works even when dialogue zh is empty)
    zh_pool = [zh for _, zh in ko_zh_pairs]
    for ko, zh in ko_zh_pairs:
        if len(items) >= max_items:
            break
        distract = [z for z in zh_pool if z != zh and z]
        random.shuffle(distract)
        if len(distract) < 2:
            continue
        choices = [zh] + distract[:3]
        random.shuffle(choices)

        items.append(
            {
                "item_id": f"{lesson_id}-IB-{counter:03d}",
                "item_type": "mcq_meaning",
                "skill": "reading",
                "difficulty_tier": "L1",
                "prompt_zh_tw": "選出最接近這句韓文的中文意思。",
                "prompt_ko": ko,
                "choices": choices,
                "answer_key": {"type": "single_choice", "value": zh},
                "explanation_zh_tw": "先抓句尾語氣與關鍵名詞，再判斷語意。",
                "linked_refs": base_linked_refs(lesson_id, grammar_node.get("id", "grammar_note") if grammar_node else "grammar_note"),
                "tags": ["grammar_note", "meaning_check"],
                "review_policy": {
                    "initial_interval_days": 2,
                    "wrong_interval_days": 1,
                    "correct_fast_interval_days": 7
                }
            }
        )
        item_type_counts["mcq_meaning"] += 1
        counter += 1
        if item_type_counts["mcq_meaning"] >= mcq_cap:
            break

    # 2) Cloze from dialogue lines
    for turn in dialogue_turns:
        if len(items) >= max_items:
            break
        if item_type_counts["cloze"] >= cloze_cap:
            break
        cloze = choose_cloze_token(turn["ko"], vocab_pool)
        if not cloze:
            continue
        answer, choices = cloze
        prompt_ko = turn["ko"].replace(answer, "____", 1)
        if prompt_ko == turn["ko"]:
            continue
        items.append(
            {
                "item_id": f"{lesson_id}-IB-{counter:03d}",
                "item_type": "cloze",
                "skill": "grammar",
                "difficulty_tier": "L1",
                "prompt_zh_tw": "填入最適合的詞，完成句子。",
                "prompt_ko": prompt_ko,
                "choices": choices,
                "answer_key": {"type": "single_choice", "value": answer},
                "explanation_zh_tw": "先看句尾語氣，再選符合語境的詞。",
                "linked_refs": base_linked_refs(lesson_id, turn["node_id"]),
                "tags": ["dialogue", "cloze"],
                "review_policy": {
                    "initial_interval_days": 2,
                    "wrong_interval_days": 1,
                    "correct_fast_interval_days": 7
                }
            }
        )
        item_type_counts["cloze"] += 1
        counter += 1

    # 3) Transform from dialogue lines
    for turn in dialogue_turns:
        if len(items) >= max_items:
            break
        if item_type_counts["transform"] >= transform_cap:
            break
        sentence = turn["ko"].strip()
        if sentence.endswith("?"):
            continue
        answer = sentence if sentence.endswith("?") else f"{sentence}?"
        items.append(
            {
                "item_id": f"{lesson_id}-IB-{counter:03d}",
                "item_type": "transform",
                "skill": "speaking",
                "difficulty_tier": "L1",
                "prompt_zh_tw": "把下面韓文改成疑問語氣（句尾上揚）。",
                "prompt_ko": sentence,
                "choices": [],
                "answer_key": {"type": "short_text", "value": answer},
                "explanation_zh_tw": "初級先掌握語調問句，形態可先維持不變。",
                "linked_refs": base_linked_refs(lesson_id, turn["node_id"]),
                "tags": ["dialogue", "question_intonation"],
                "review_policy": {
                    "initial_interval_days": 2,
                    "wrong_interval_days": 1,
                    "correct_fast_interval_days": 7
                }
            }
        )
        item_type_counts["transform"] += 1
        counter += 1

    # 4) Retrieval from grammar notes
    if grammar_node:
        for section in grammar_sections:
            if len(items) >= max_items:
                break
            if item_type_counts["retrieval"] >= retrieval_cap:
                break
            title = section.get("title_zh_tw", "文法重點")
            points = section.get("points_zh_tw", [])
            if not points:
                continue
            first = normalize_md(str(points[0]))
            if not first:
                continue
            items.append(
                {
                    "item_id": f"{lesson_id}-IB-{counter:03d}",
                    "item_type": "retrieval",
                    "skill": "grammar",
                    "difficulty_tier": "L1",
                    "prompt_zh_tw": f"請口頭說明「{title}」的一個重點。",
                    "prompt_ko": "",
                    "choices": [],
                    "answer_key": {"type": "short_text", "value": first},
                    "explanation_zh_tw": "用自己的話重述規則即可，不必逐字背誦。",
                    "linked_refs": base_linked_refs(lesson_id, grammar_node.get("id", "grammar_note")),
                    "tags": ["grammar_retrieval"],
                    "review_policy": {
                        "initial_interval_days": 2,
                        "wrong_interval_days": 1,
                        "correct_fast_interval_days": 7
                    }
                }
            )
            item_type_counts["retrieval"] += 1
            counter += 1

    return items[:max_items]


def main():
    parser = argparse.ArgumentParser(description="Generate TLG-025 item bank from a unit fixture")
    parser.add_argument("--input", required=True, help="Unit fixture JSON path")
    parser.add_argument("--output", required=True, help="Output item bank JSON path")
    parser.add_argument("--max-items", type=int, default=24)
    args = parser.parse_args()

    unit_data = load_json(Path(args.input))
    unit = unit_data.get("unit", {})
    items = build_items(unit_data, max_items=args.max_items)

    bank = {
        "bank_id": f"KO-IBANK-{unit.get('unit_id', 'UNKNOWN')}-V1",
        "version": "v1",
        "target_lang": unit.get("target_language", "ko"),
        "support_langs": [unit.get("learner_locale_source", "zh_tw"), "en"],
        "level": unit.get("level", "A1"),
        "generated_at": "2026-03-04",
        "source_unit_id": unit.get("unit_id", "UNKNOWN"),
        "items": items
    }
    save_json(Path(args.output), bank)
    print(f"generated items={len(items)} -> {args.output}")


if __name__ == "__main__":
    main()
