# CMOD-013 — Sentence Practice Action Contract

## Goal

定義 **Sentence Practice Action Contract**，讓內容層（Content-first）能統一描述句子級別的互動行為。
確保 `listen`, `repeat`, `shadow`, `type` 等動作在不同載體（Dialogue, Video, Article）間具有一致的資料格式，並能無縫觸發 Knowledge Lab 的下鑽（Deep-dive）行為。

## Core Concepts

### 1. Atomic Actions
- **`listen`**: 播放可用的音訊來源，來源可以是預錄音檔或內建 TTS。
- **`repeat`**: 聽完後錄音，並可回放比對。若無預錄音檔，可改用 TTS 文字來源。
- **`shadow`**: 跟讀模式。在播放音訊來源的同時進行錄音，通常伴隨進度條或文字高亮。
- **`type`**: 引導式打字（Guided Typing）。

### 2. Action Registry
- 每一個句子（Sentence Item）可以宣告其支援的動作清單。
- 這些動作對應前端的原子組件（Atom Components）。

### 3. Deep-dive Links
- 整合 `CMOD-011` 的 Anchor Linking。
- 確保句子中的特定片段能關聯到 `dictionary_atom_refs` 或 `grammar_refs`。

---

## Data Schema: `sentence_action_contract`

當一個內容節點（如 `dialogue` 的 `turns` 或 `video_transcript` 的 `lines`）需要支援句子級互動時，應掛載此結構。

### Contract Structure

```json
{
  "interaction_contract": {
    "actions": ["listen", "repeat", "shadow", "type"],
    "payload": {
      "tts_text": "안녕하세요.",
      "audio_ref": "audio/path/to/sentence.mp3",
      "target_surface": "안녕하세요",
      "alignment_ref": "audio/path/to/alignment.json",
      "zh_tw": "你好"
    },
    "knowledge_dive": {
      "dictionary_atom_refs": [
        { "surface": "안녕", "ref": "n-ko-0001" }
      ],
      "grammar_refs": [
        { "surface": "하세요", "ref": "g-ko-polite-present" }
      ]
    }
  }
}
```

### Field Definitions

| Field | Type | Description |
| :--- | :--- | :--- |
| `actions` | array | 該句子支援的動作清單 (`listen`, `repeat`, `shadow`, `type`) |
| `payload` | object | 執行動作所需的資料基礎 |
| `payload.audio_ref` | string | (Optional) 句子音檔路徑 |
| `payload.tts_text` | string | (Optional) 供內建 TTS 使用的朗讀文字 |
| `payload.target_surface` | string | 韓文表面形（用於打字檢核或顯示） |
| `payload.alignment_ref` | string | (Optional) 音頻對齊資料，主要供 `shadow` 使用 |
| `knowledge_dive` | object | 知識下鑽元數據 |
| `knowledge_dive.dictionary_atom_refs` | array | 句子內部的單字引用 |
| `knowledge_dive.grammar_refs` | array | 句子內部的語法引用 |

---

## Integration with Carriers

### 1. Dialogue Carrier

```json
{
  "id": "A1-U05-D1",
  "content_form": "dialogue",
  "payload": {
    "turns": [
      {
        "speaker": "Minsu",
        "text": "머리가 아파요.",
        "interaction_contract": {
          "actions": ["listen", "repeat", "type"],
          "payload": {
            "tts_text": "머리가 아파요.",
            "target_surface": "머리가 아파요."
          },
          "knowledge_dive": {
            "dictionary_atom_refs": [{ "surface": "머리", "ref": "n-ko-head" }],
            "grammar_refs": [{ "surface": "아파요", "ref": "g-ko-pain" }]
          }
        }
      }
    ]
  }
}
```

### 2. Video Carrier (Transcript)

影片的 transcript line 亦可套用相同契約：

```json
{
  "id": "V-KO-001-L1",
  "interaction_contract": {
    "actions": ["listen", "shadow"],
    "payload": {
      "tts_text": "안녕하세요.",
      "alignment_ref": "audio/video/v001_l1_align.json"
    }
  }
}
```

---

## Action Semantics & Requirements

### Listen
- **Requirement**: `audio_ref` 或 `tts_text` 至少其一必須存在。
- **UX**: 點擊發音圖示或句子本身。

### Repeat (Recording)
- **Requirement**: `audio_ref` 或 `tts_text` 至少其一必須存在。
- **UX**: 播放一次 -> 使用者錄音 -> 系統提供簡單比對（或僅提供波形顯示）。

### Shadow (Progressive)
- **Requirement**: `audio_ref` 或 `tts_text` 至少其一必須存在；`alignment_ref` 建議存在。
- **UX**: 音檔播放時，文字隨進度變色。

### Type (Input)
- **Requirement**: `target_surface` 必須存在。
- **UX**: 提供輸入框或虛擬鍵盤，對齊 `interaction_modes: guided_typing`。

---

## Compatibility Rules

1. **Fallback**: 若 `interaction_contract` 缺失，系統應嘗試從內容頂層句子文字派生 `tts_text`，必要時再由 viewer 轉為預錄音或純文字播放模式。
2. **Knowledge Priority**: `knowledge_dive` 中的 `surface` 應與 `CMOD-011` 的 Anchor Linking 邏輯對齊。若兩者衝突，優先使用內容層明確標記的 `knowledge_dive`。
3. **Completion Tracking**: 若 `interaction_contract.actions` 包含 `shadow` 且 `completion_rules` 要求 `shadow` 完成，則需追蹤該動作的執行狀態。

---

## Next Steps

1. **Viewer Support**: 在 Modular Viewer 中實作 `interaction_contract` 解析器。
2. **Template Update**: 更新 `UNITFAC_005_AUTHORING_TEMPLATES.md` 加入句子級互動區塊。
3. **Pilot Data**: 將 `A1-U05` 的對話部分遷移至此契約格式。
