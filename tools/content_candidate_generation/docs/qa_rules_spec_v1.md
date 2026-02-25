# QA Rules Specification (v1)

本文定義 `CONTENT_CANDIDATE_GENERATION_FRAMEWORK` 中 QA Stage 執行的自動化檢查規則。

## 規則列表

| Rule ID | Severity | 名稱 | 檢查邏輯 |
| :--- | :--- | :--- | :--- |
| `REQ_FIELD_MISSING` | ERROR | 缺失必要欄位 | 檢查 `candidate_schema_v1.json` 中標記為 required 的欄位是否存在。 |
| `FIELD_EMPTY` | ERROR | 欄位內容為空 | 欄位存在但內容為空字串或 null。 |
| `ARRAY_EMPTY` | ERROR | 列表內容為空 | 指定為非空列表的欄位（如 `can_do_zh_tw`）長度為 0。 |
| `ZH_SUMMARY_MISSING` | ERROR | 缺失中文摘要 | `review_summary_zh_tw` 缺失或不包含中文字元。 |
| `TARGET_POSITION_INVALID` | ERROR | 無效的位置資訊 | `target_position` 格式不正確，或同時缺失 `slot`/`after_lesson_id`/`before_lesson_id`。 |
| `DUPLICATE_ID` | ERROR | ID 重複 | 批次內存在相同的 `candidate_id`。 |
| `DUPLICATE_CONTENT` | WARNING | 內容重複 | 不同 ID 的候選項目其 `foreign_preview` 內容完全一致。 |
| `DUP_TITLE_SIMILAR_HIGH` | WARNING | 標題重複性高 | `title_zh_tw` 相似度過高（超過 80%）。 |
| `LEVEL_MISMATCH` | ERROR | 等級不符 | `target_level` 不在 `generation_brief` 的 `target_levels` 清單中。 |
| `UNIT_MISMATCH` | WARNING | 單元不符 | `target_unit_id` 不在 `generation_brief` 的 `target_units` 清單中。 |
| `A1_COMPLEXITY_RISK` | WARNING | A1 難度風險 | 若 `target_level` 為 A1，但標題或摘要長度異常（例如超過 30 字）。 |

## 嚴重程度說明

- **ERROR**: 阻塞性錯誤。必須修復才能進審核台（或在審核台會被標記為不可用）。
- **WARNING**: 注意事項。審核人員應知曉此風險，但不影響基本匯入。
