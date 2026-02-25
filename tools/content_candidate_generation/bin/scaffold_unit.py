
import os
import json
import argparse
import datetime

def create_scaffold(unit_id, level, title):
    blueprint = {
        "version": "unit_blueprint_v0",
        "adapter_contract": {
            "adapter_version": "frontend_unit_adapter_v0",
            "stability": "proposed",
            "fallback_locale_order": ["zh-TW", "en"],
            "notes": f"Scaffolded unit blueprint for {unit_id}."
        },
        "unit": {
            "unit_id": unit_id,
            "title_zh_tw": title,
            "target_language": "ko",
            "learner_locale_source": "zh-TW",
            "level": level,
            "theme_zh_tw": "待補充主題",
            "output_ratio_target": 0.5,
            "can_do_zh_tw": [
                "能使用本單元核心句型進行基本溝通"
            ]
        },
        "sequence": [
            {
                "id": f"{unit_id}-L1",
                "candidate_type": "lesson",
                "content_form": "dialogue",
                "learning_role": "immersion_input",
                "skill_focus": ["listening", "reading"],
                "output_mode": "none",
                "duration_min": 5,
                "title_zh_tw": "初步沉浸對話",
                "summary_zh_tw": "展示本單元核心場景的自然對話。",
                "sample_lines": ["안녕하세요."],
                "expected_output_zh_tw": "學生能聽懂並辨識核心詞彙。",
                "payload": {
                    "dialogue_turns": [
                        {
                            "speaker": "A",
                            "text": "안녕하세요.",
                            "zh_tw": "你好。"
                        },
                        {
                            "speaker": "B",
                            "text": "반갑습니다.",
                            "zh_tw": "很高興見到你。"
                        }
                    ]
                },
                "adapter_hints": {
                    "content_renderer_key": "dialogue"
                }
            },
            {
                "id": f"{unit_id}-G1",
                "candidate_type": "grammar_note",
                "content_form": "pattern_card",
                "learning_role": "structure_pattern",
                "skill_focus": ["writing"],
                "output_mode": "frame_fill",
                "duration_min": 3,
                "title_zh_tw": "核心句型練習",
                "summary_zh_tw": "練習本單元的核心語法框架。",
                "sample_lines": [],
                "expected_output_zh_tw": "能正確填充句型槽位。",
                "payload": {
                    "frames": [
                        {
                            "frame": "___ 주세요.",
                            "use_zh_tw": "請求某物",
                            "slots_zh_tw": ["物品名稱"]
                        }
                    ]
                },
                "adapter_hints": {
                    "content_renderer_key": "pattern_card",
                    "interaction_renderer_key": "frame_fill"
                }
            },
             {
                "id": f"{unit_id}-R1",
                "candidate_type": "path_node",
                "content_form": "review_card",
                "learning_role": "review_retrieval",
                "skill_focus": ["integrated"],
                "output_mode": "review_retrieval",
                "duration_min": 3,
                "title_zh_tw": "單元總結回想",
                "summary_zh_tw": "回想本單元學到的重點句型。",
                "sample_lines": [],
                "expected_output_zh_tw": "學生能不靠提示說出核心句子。",
                "payload": {
                    "prompts_zh_tw": [
                        "如何用韓文說『請給我水』？"
                    ],
                    "reference_answers_ko": [
                        "물 주세요."
                    ]
                },
                "adapter_hints": {
                    "content_renderer_key": "review_card",
                    "interaction_renderer_key": "review_retrieval"
                }
            }
        ],
        "scheduled_followups": []
    }
    return blueprint

def main():
    parser = argparse.ArgumentParser(description="Unit Blueprint Scaffolding Tool")
    parser.add_argument("--id", required=True, help="Unit ID (e.g., A1-U05)")
    parser.add_argument("--level", default="A1", help="Target Level (e.g., A1, A2)")
    parser.add_argument("--title", required=True, help="Unit Title in Chinese")
    parser.add_argument("--output", help="Output JSON path")
    
    args = parser.parse_args()
    
    blueprint = create_scaffold(args.id, args.level, args.title)
    
    output_path = args.output or f"{args.id.lower().replace('-', '_')}_unit_blueprint_v0.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, indent=2)
        
    print(f"Scaffolded unit blueprint created at: {output_path}")

if __name__ == "__main__":
    main()
