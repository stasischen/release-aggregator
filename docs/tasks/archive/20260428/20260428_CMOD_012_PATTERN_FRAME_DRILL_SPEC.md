# CMOD-012 — Controlled Substitution Drills (Pattern Frame & Slot Bank)

## Goal

定義 `controlled_output` 類型節點（組句、填空、轉換）的標準資料契約，確保其與 `EXAMPLE_SENTENCE_BANK_SCHEMA_V1` 中的 `frame_projection` 概念對齊。

目標是讓練習不再只是「死板的字串替換」，而是基於語法框（Pattern Frame）與詞庫（Slot Bank）的動態組合。

## Core Concepts

### 1. Pattern Frame
- 定義句子的骨架與變動點。
- 例如：`[body_part]가/이 아파요.`
- 對應 `pattern_frame_ref` 鏈接到知識庫中的 GID。

### 2. Slot Bank
- 定義填充變動點的候選詞。
- 每個 Slot 都有一個 `slot_id`。
- 提供 `candidates` 清單，包含韓文表面形、中文翻譯、音檔路徑等。

### 3. Task Projection
- 指定單一練習任務要使用的 Slot 組合。
- 對應 `slot_projection` 概念。

---

## Proposed Schema: `pattern_frame_drill`

當 `payload.mode` 為 `pattern_frame_drill` 時，適用以下結構。

### Payload Level

| Field | Type | Description |
| :--- | :--- | :--- |
| `pattern_frame_ref` | string | 引用 `core-schema` 或 `content-ko` 中的 Pattern GID |
| `frame_template` | string | (Optional) 離線渲染使用的模板，如 `[body_part]가/이 아파요.` |
| `slot_bank` | array | 定義多個 Slot 的候選庫 |
| `tasks` | array | 具體的練習題目 |

### `slot_bank` Item

```json
{
  "slot_id": "body_part",
  "candidates": [
    {
      "surface": "머리",
      "zh_tw": "頭",
      "audio_ref": "audio/vocab/head.mp3"
    },
    {
      "surface": "배",
      "zh_tw": "肚子"
    }
  ]
}
```

### `tasks` Item

```json
{
  "prompt_zh_tw": "說出「我頭痛」",
  "target_projection": {
    "slot_values": {
      "body_part": "머리"
    }
  },
  "distractor_slots": ["body_part"] 
}
```

---

## Node Type Mapping

### 1. `chunk_assembly` (組句)
- **Modality**: 將 `slot_bank` 中的正確候選詞與 `frame_template` 的固定部分（Static chunks）拆解為干擾項供選擇。
- **Interaction Mode**: `chunk_assembly`

### 2. `frame_fill` (填空)
- **Modality**: 保留 `frame_template` 的固定部分，僅將 `slot_id` 對應位置留白。
- **Interaction Mode**: `frame_fill`

### 3. `pattern_transform` (轉換)
- **Modality**: 提供一個 `source_projection` (A) 與 `target_projection` (B)，要求學生進行轉換。
- **Interaction Mode**: `pattern_transform`

---

## Migration Strategy (Warning-first)

1. **Phase 1**: 支援 Legacy Shape (目前的 `tasks` 內含 `chunks` 或 `target_frame`)。
2. **Phase 2**: 引入 `pattern_frame_drill` 作為推薦規格，`mockup_check.py` 對於沒有 `pattern_frame_ref` 的新單元發出警告。
3. **Phase 3**: 全面模組化，由 `adapter` 根據 `pattern_frame_drill` 動態生成 UI 所需的 chunks 或填空位。

## Example: A1-U05-P3 (Refactored)

```json
{
  "id": "A1-U05-P3-V1",
  "content_form": "practice_card",
  "learning_role": "controlled_output",
  "output_mode": "frame_fill",
  "interaction_modes": ["frame_fill", "chunk_assembly"],
  "payload": {
    "mode": "pattern_frame_drill",
    "pattern_frame_ref": "P-KO-SYMPTOM-PAIN",
    "frame_template": "[body_part]가/이 아파요.",
    "slot_bank": [
      {
        "slot_id": "body_part",
        "candidates": [
          { "surface": "머리", "zh_tw": "頭" },
          { "surface": "목", "zh_tw": "喉嚨" },
          { "surface": "배", "zh_tw": "肚子" }
        ]
      }
    ],
    "tasks": [
      {
        "prompt_zh_tw": "將『我頭痛』改為『我喉嚨痛』",
        "source_projection": { "slot_values": { "body_part": "머리" } },
        "target_projection": { "slot_values": { "body_part": "목" } }
      }
    ]
  }
}
```
