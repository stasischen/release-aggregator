#!/usr/bin/env python3
import argparse
import json
import os
import sys

def create_scaffold(args):
    unit_id = args.unit_id
    title = args.title_zh_tw
    lang = args.target_language
    locale = args.learner_locale_source
    level = args.level
    theme = args.theme_zh_tw

    # Top-level structure
    blueprint = {
        "version": "unit_blueprint_v0",
        "adapter_contract": {
            "adapter_version": "frontend_unit_adapter_v0",
            "stability": "proposed",
            "fallback_locale_order": [locale, "en"],
            "notes": f"Scaffolded production-ready unit blueprint for {unit_id}."
        },
        "unit": {
            "unit_id": unit_id,
            "title_zh_tw": title,
            "target_language": lang,
            "learner_locale_source": locale,
            "level": level,
            "theme_zh_tw": theme,
            "output_ratio_target": 0.5,
            "can_do_zh_tw": [
                f"TODO: Add can-do statement for {title} (e.g. 能使用...進行...)"
            ]
        },
        "sequence": [],
        "scheduled_followups": []
    }

    # Helper for node IDs
    def node_id(suffix):
        return f"{unit_id}-{suffix}"

    # 1. Immersion: Dialogue
    blueprint["sequence"].append({
        "id": node_id("L1"),
        "candidate_type": "lesson",
        "content_form": "dialogue",
        "learning_role": "immersion_input",
        "skill_focus": ["listening", "integrated"],
        "output_mode": "none",
        "duration_min": 5,
        "title_zh_tw": f"{title}：核心對話",
        "summary_zh_tw": "TODO: 描述主要的對話場景與情境。",
        "sample_lines": ["TODO: 第一句韓文對話", "TODO: 第二句韓文對話"],
        "expected_output_zh_tw": "藉由聽與讀初步沉浸在真實場景中。",
        "payload": {
            "dialogue_turns": [
                {"speaker": "A", "text": "TODO: KO", "zh_tw": "TODO: TW"},
                {"speaker": "B", "text": "TODO: KO", "zh_tw": "TODO: TW"}
            ]
        },
        "adapter_hints": {"content_renderer_key": "dialogue"}
    })

    # 2. Comprehension: Check
    blueprint["sequence"].append({
        "id": node_id("L2"),
        "candidate_type": "lesson",
        "content_form": "comprehension_check",
        "learning_role": "immersion_input",
        "skill_focus": ["reading"],
        "output_mode": "none",
        "duration_min": 3,
        "title_zh_tw": "理解度抽查",
        "summary_zh_tw": "針對 L1 對話內容進行非評分式理解檢查。",
        "sample_lines": ["TODO: 問題內容"],
        "expected_output_zh_tw": "確認學習者抓到 L1 的核心資訊。",
        "payload": {
            "tasks": [
                {
                    "prompt_zh_tw": "TODO: 關於對話內容的問題？",
                    "options": [
                        {"id": "1", "label_zh_tw": "TODO: 正確選項", "is_correct": True},
                        {"id": "2", "label_zh_tw": "TODO: 錯誤選項", "is_correct": False}
                    ]
                }
            ]
        },
        "adapter_hints": {"content_renderer_key": "comprehension_check"}
    })

    # 3. Immersion: Non-Dialogue (Notice)
    blueprint["sequence"].append({
        "id": node_id("L3"),
        "candidate_type": "lesson",
        "content_form": "notice",
        "learning_role": "immersion_input",
        "skill_focus": ["reading"],
        "output_mode": "none",
        "duration_min": 4,
        "title_zh_tw": f"{title}相關公告/文件",
        "summary_zh_tw": "TODO: 描述文檔類型（如公告、價目表、地圖等）。",
        "sample_lines": ["TODO: 公告中的韓文標題"],
        "expected_output_zh_tw": "閱讀非對話式的真實語言輸入。",
        "payload": {
            "notice_items": ["TODO: KO Item 1", "TODO: KO Item 2"],
            "notice_items_zh_tw": ["TODO: TW Item 1", "TODO: TW Item 2"]
        },
        "adapter_hints": {"content_renderer_key": "notice"}
    })

    # 4. Structure: Dictionary Chunks
    blueprint["sequence"].append({
        "id": node_id("D1"),
        "candidate_type": "dictionary_pack",
        "content_form": "functional_phrase_pack",
        "learning_role": "structure_pattern",
        "skill_focus": ["integrated"],
        "output_mode": "chunk_assembly",
        "duration_min": 5,
        "title_zh_tw": "生存詞塊：關鍵表達",
        "summary_zh_tw": "整理本單元必備的高頻詞塊（Collocations）。",
        "sample_lines": ["TODO: 核心詞塊 1", "TODO: 核心詞塊 2"],
        "expected_output_zh_tw": "掌握組裝句子所需的最小功能單元。",
        "payload": {
            "sections": [
                {
                    "title_zh_tw": "核心名詞/動作",
                    "items": ["TODO: KO 1", "TODO: KO 2"],
                    "item_gloss_by_ko": {"TODO: KO 1": "TODO: TW 1", "TODO: KO 2": "TODO: TW 2"}
                }
            ]
        },
        "adapter_hints": {
            "content_renderer_key": "functional_phrase_pack",
            "interaction_renderer_key": "chunk_assembly"
        }
    })

    # 5. Structure: Pattern Card
    blueprint["sequence"].append({
        "id": node_id("G1"),
        "candidate_type": "grammar_note",
        "content_form": "pattern_card",
        "learning_role": "structure_pattern",
        "skill_focus": ["writing", "speaking"],
        "output_mode": "frame_fill",
        "duration_min": 5,
        "title_zh_tw": "核心句型框",
        "summary_zh_tw": "定義本單元的語法公式。",
        "sample_lines": ["TODO: ___ 주세요."],
        "expected_output_zh_tw": "能在公式中替換詞塊產出新句子。",
        "payload": {
            "frames": [
                {
                    "frame": "TODO: ___ (slot) ...",
                    "use_zh_tw": "TODO: 句型用途描述",
                    "slots_zh_tw": ["TODO: 槽位說明"]
                }
            ]
        },
        "adapter_hints": {
            "content_renderer_key": "pattern_card",
            "interaction_renderer_key": "frame_fill"
        }
    })

    # 6. Structure: Grammar Note
    blueprint["sequence"].append({
        "id": node_id("G2"),
        "candidate_type": "grammar_note",
        "content_form": "grammar_note",
        "learning_role": "structure_grammar",
        "skill_focus": ["reading"],
        "output_mode": "none",
        "duration_min": 4,
        "title_zh_tw": "文法重點：為什麼這樣說？",
        "summary_zh_tw": "補充必要的語法細節（如助詞、語尾、特別搭配）。",
        "sample_lines": ["TODO: 解說重點"],
        "expected_output_zh_tw": "理解語法背後的規則而非死記。",
        "payload": {
            "sections": [
                {
                    "title_zh_tw": "TODO: 重點標題",
                    "points_zh_tw": ["TODO: 解說點 1", "TODO: 解說點 2"],
                    "ko_examples": ["TODO: KO Example"]
                }
            ]
        },
        "adapter_hints": {"content_renderer_key": "grammar_note"}
    })

    # 7. Output: Controlled Assembly
    blueprint["sequence"].append({
        "id": node_id("P1"),
        "candidate_type": "path_node",
        "content_form": "practice_card",
        "learning_role": "controlled_output",
        "skill_focus": ["writing"],
        "output_mode": "chunk_assembly",
        "duration_min": 5,
        "title_zh_tw": "句型組裝練習",
        "summary_zh_tw": "利用 P1 提供的詞塊組拆解 G1 的句型。",
        "sample_lines": ["[chunk1] [chunk2]"],
        "expected_output_zh_tw": "能正確排序出目標句型。",
        "payload": {
            "tasks": [
                {
                    "prompt_zh_tw": "TODO: 請組出「...」",
                    "chunks": ["TODO: KO 1", "TODO: KO 2"],
                    "target_examples": ["TODO: KO TARGET"]
                }
            ]
        },
        "adapter_hints": {"interaction_renderer_key": "chunk_assembly"}
    })

    # 8. Output: Controlled Response
    blueprint["sequence"].append({
        "id": node_id("P2"),
        "candidate_type": "path_node",
        "content_form": "practice_card",
        "learning_role": "controlled_output",
        "skill_focus": ["speaking"],
        "output_mode": "response_builder",
        "duration_min": 4,
        "title_zh_tw": "情境反應選擇",
        "summary_zh_tw": "聽取店員/對方的提問，選擇正確的回應。",
        "sample_lines": ["Q: ??? -> A: !!!"],
        "expected_output_zh_tw": "在受控情境下快速做出正確語意反應。",
        "payload": {
            "items": [
                {
                    "prompt_ko": "TODO: KO PROMPT",
                    "prompt_zh_tw": "TODO: TW PROMPT",
                    "response_choices_ko": ["TODO: OPTION 1", "TODO: OPTION 2"],
                    "accepted_responses_ko": ["TODO: OPTION 1"]
                }
            ]
        },
        "adapter_hints": {"interaction_renderer_key": "response_builder"}
    })

    # 9. Output: Transform
    blueprint["sequence"].append({
        "id": node_id("P3"),
        "candidate_type": "path_node",
        "content_form": "practice_card",
        "learning_role": "controlled_output",
        "skill_focus": ["writing", "speaking"],
        "output_mode": "pattern_transform",
        "duration_min": 5,
        "title_zh_tw": "句型代換與變換",
        "summary_zh_tw": "給予特定限制，將原句型進行變換（如 Ice -> Hot, 1 -> 2）。",
        "sample_lines": ["A -> B (Pattern Shift)"],
        "expected_output_zh_tw": "展現對句型變數的控制力。",
        "payload": {
            "mode": "pattern_transform",
            "tasks": [
                {
                    "prompt_zh_tw": "TODO: 將「...」改為「...」",
                    "input_ko": "TODO: OLD KO",
                    "target_examples": ["TODO: NEW KO"]
                }
            ],
            "instruction_zh_tw": "請根據題目要求變換句型詞彙。"
        },
        "adapter_hints": {"interaction_renderer_key": "pattern_transform"}
    })

    # 10. Output: Repair Practice
    blueprint["sequence"].append({
        "id": node_id("P4"),
        "candidate_type": "path_node",
        "content_form": "practice_card",
        "learning_role": "controlled_output",
        "skill_focus": ["speaking"],
        "output_mode": "response_builder",
        "duration_min": 4,
        "title_zh_tw": "修復與求助練習 (Repair)",
        "summary_zh_tw": "學習在溝通中斷或聽不懂時如何求助（如：請再說一次、我要這個不是那個）。",
        "sample_lines": ["다시 말씀해 주세요."],
        "expected_output_zh_tw": "建立溝通韌性，練習常見的修復短語。",
        "payload": {
            "items": [
                {
                    "prompt_ko": "TODO: 某個聽不懂的快語段",
                    "prompt_zh_tw": "TODO: (聽不懂的情境描述)",
                    "response_choices_ko": ["다시 말씀해 주세요.", "죄송합니다."],
                    "accepted_responses_ko": ["다시 말씀해 주세요."]
                }
            ]
        },
        "adapter_hints": {"interaction_renderer_key": "response_builder"}
    })

    # 11. Output: Guided Production (Speaking)
    blueprint["sequence"].append({
        "id": node_id("P5"),
        "candidate_type": "path_node",
        "content_form": "roleplay_prompt",
        "learning_role": "immersion_output",
        "skill_focus": ["speaking"],
        "output_mode": "guided",
        "duration_min": 6,
        "title_zh_tw": "自由對話挑戰 (Roleplay)",
        "summary_zh_tw": "在設定的情境下完成多回對話任務。",
        "sample_lines": ["Scenario: At the TODO..."],
        "expected_output_zh_tw": "能整合運用本單元所有句型完成溝通任務。",
        "payload": {
            "scenery_ko": "TODO: 韓文情境描述",
            "scenery_zh_tw": "TODO: 中文情境描述",
            "constraints_zh_tw": ["TODO: 任務限制 1", "TODO: 任務限制 2"],
            "required_patterns_zh_tw": ["TODO: 必須使用的句型"],
            "prompt_card_zh_tw": "TODO: 給學習者的引導語"
        },
        "adapter_hints": {"content_renderer_key": "roleplay_prompt"}
    })

    # 12. Output: Guided Production (Writing)
    blueprint["sequence"].append({
        "id": node_id("P6"),
        "candidate_type": "path_node",
        "content_form": "message_prompt",
        "learning_role": "immersion_output",
        "skill_focus": ["writing"],
        "output_mode": "guided",
        "duration_min": 4,
        "title_zh_tw": "訊息傳遞挑戰 (Messaging)",
        "summary_zh_tw": "以訊息形式完成任務（如預約、留言、確認細節）。",
        "sample_lines": ["Task: Message TODO..."],
        "expected_output_zh_tw": "能書寫正確的訊息與朋友或服務端溝通。",
        "payload": {
            "prompt_ko": "TODO: KO TASK PROMPT",
            "prompt_zh_tw": "TODO: TW TASK PROMPT",
            "must_include_zh_tw": ["TODO: 必含元素"],
            "example_shape_ko": ["TODO: 參考答案 KO"]
        },
        "adapter_hints": {"content_renderer_key": "message_prompt"}
    })

    # 13. Review: Retrieval
    blueprint["sequence"].append({
        "id": node_id("R1"),
        "candidate_type": "path_node",
        "content_form": "review_card",
        "learning_role": "review_retrieval",
        "skill_focus": ["integrated"],
        "output_mode": "review_retrieval",
        "duration_min": 5,
        "title_zh_tw": "單元總結回想",
        "summary_zh_tw": "僅靠中文提示，回想起本單元的關鍵溝通功能句。",
        "sample_lines": ["TODO: 提示 1 -> TODO: 答案 1"],
        "expected_output_zh_tw": "不依賴提示完成核心句子的回想（Retrieval）。",
        "payload": {
            "retrieval_target": "mixed",
            "prompts_zh_tw": ["TODO: 中文提示 1", "TODO: 中文提示 2"],
            "reference_answers_ko": ["TODO: 參考答案 1", "TODO: 參考答案 2"]
        },
        "adapter_hints": {"content_renderer_key": "review_card"}
    })

    # 14. Followup 1 (+1 unit)
    blueprint["scheduled_followups"].append({
        "id": node_id("X1"),
        "candidate_type": "path_node",
        "learning_role": "cross_unit_transfer",
        "timing": "+1 unit",
        "transfer_to": "TODO: Target Unit ID",
        "goal_zh_tw": f"TODO: 描述如何將 {title} 的句型遷移至下一單元。",
        "transfer_pattern_refs": ["TODO: 遷移句型名稱"]
    })

    # 15. Followup 2 (+3 units)
    blueprint["scheduled_followups"].append({
        "id": node_id("X2"),
        "candidate_type": "path_node",
        "learning_role": "cross_unit_transfer",
        "timing": "+3 units",
        "transfer_to": "TODO: Later Unit ID",
        "goal_zh_tw": f"TODO: 進行間隔重複，遷移 {title} 的次要句型。",
        "transfer_pattern_refs": ["TODO: 修復短語或其他"]
    })

    # Save to file
    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated scaffold for {unit_id} at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a production-ready A1/A2 unit blueprint scaffold.")
    parser.add_argument("--unit_id", required=True, help="e.g. A1-U06")
    parser.add_argument("--title_zh_tw", required=True, help="e.g. 旅館入住")
    parser.add_argument("--target_language", default="ko", help="default: ko")
    parser.add_argument("--learner_locale_source", default="zh-TW", help="default: zh-TW")
    parser.add_argument("--level", required=True, choices=["A1", "A2"], help="A1 or A2")
    parser.add_argument("--theme_zh_tw", required=True, help="e.g. 預約、入住手續")
    parser.add_argument("--output", required=True, help="Path for the output JSON file")

    args = parser.parse_args()
    create_scaffold(args)

if __name__ == "__main__":
    main()
