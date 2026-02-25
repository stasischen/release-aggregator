# Generation Brief Examples

## Lesson Batch (A1)

Targeting two units in A1 to add more dialogue-based lessons.

```json
{
  "batch_id": "20260225_A1_U04_lessons_v1",
  "goal": "增加 A1-U04 單元的對話練習，重點在於基礎問候與自我介紹的變體。",
  "target_levels": ["A1"],
  "target_units": ["A1-U04"],
  "candidate_types": ["lesson"],
  "count_targets": {
    "lesson": 5
  },
  "variant_policy": "none",
  "cost_preference": "balanced",
  "language_policy": {
    "summary_locale": "zh-TW",
    "target_language": "ko"
  },
  "input_snapshots": {
    "catalog_path": "docs/snapshots/catalog_20260225.json",
    "unit_blueprint_path": "docs/tasks/mockups/agg_gen_017_a1_u04_unit_mockup_data.json"
  }
}
```

## Mixed Grammar & Dictionary Batch (B1)

Targeting B1 grammar notes and dictionary packs.

```json
{
  "batch_id": "20260225_B1_grammar_dict_v1",
  "goal": "補齊 B1 級別關於『情緒表達』的文法與單字包。",
  "target_levels": ["B1"],
  "candidate_types": ["grammar_note", "dictionary_pack"],
  "count_targets": {
    "grammar_note": 3,
    "dictionary_pack": 2
  },
  "language_policy": {
    "summary_locale": "zh-TW",
    "target_language": "ko"
  },
  "exclusion_rules": [
    "已經存在的 A2 基本情緒單元",
    "過於專業的心理學術語"
  ]
}
```
