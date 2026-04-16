# PEDOPT-001 — Comprehension Check Taxonomy + Payload Spec

## 1. Goal
將 `comprehension_check` 從廣義的「理解題」細分為可工程化驗證、可教學設計的題型分類（Taxonomy）。目標是確保理解檢查不只是簡單的「中文對照」，而是能真正檢測學習者是否掌握了韓文語境、意圖或互動邏輯。

---

## 2. Taxonomy (題型分類)

| 類型 (question_type) | 教學目標 | 題目範例 (中文描述) |
| :--- | :--- | :--- |
| **`info_extract`** | **資訊提取**：找關鍵時間、地點、物品、價格。 | 「他明天幾點要去超市？」 |
| **`intent`** | **意圖辨識**：判斷說話者的態度或目的（如：拒絕、邀請、抱怨）。 | 「說話者為什麼說這句話？(A) 邀請 (B) 拒絕」 |
| **`next_response`** | **語境銜接**：根據上文判斷最自然的下一句回應。 | 「聽到『謝謝』後，哪句回應最合適？」 |
| **`sequence`** | **邏輯排序**：根據對話判斷事情發生的先後順序。 | 「請排列出他們的行程順序。」 |

---

## 3. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-CC",
  "candidate_type": "path_node",
  "content_form": "practice_card",
  "learning_role": "controlled_output",
  "title_zh_tw": "理解檢查",
  "payload": {
    "question_type": "info_extract | intent | next_response | sequence",
    "prompt_zh_tw": "題目描述 (例如：這句話的意思是？)",
    "context_ko": "（選填）輔助理解的韓文短文或前情提要",
    "options": [
      {
        "text": "選項內容",
        "is_correct": true,
        "feedback_zh_tw": "答對時的解析（選填）"
      },
      {
        "text": "選項內容",
        "is_correct": false,
        "feedback_zh_tw": "答錯時的提示（選填）"
      }
    ]
  }
}
```

---

## 4. Dos & Don'ts (作者指引)

### ✅ Do
- **多樣化題型**：一個單元若有 3 個 CC 節點，建議至少包含兩種不同 `question_type`。
- **干擾項設計**：錯誤選項應包含「聽起來很像但意思不對」的詞，或「單元中出現過但在此語境不通」的詞。
- **意圖優先**：在 A2 級別，增加 `intent` 題型，訓練學生聽出語氣（如：是想買東西還是只是問問）。

### ❌ Don't
- **翻譯依賴**：題目如果「不看韓文原文，只看中文翻譯也能選對」，這就是無效題目。
- **過度細節**：避免考過於偏門的生詞，重點應放在本節課的核心教學目標。

---

## 5. A1/A2 範例

### 範例 1：A1 - Info Extract (咖啡廳點餐)
```json
{
  "id": "A1-U04-CC1",
  "question_type": "info_extract",
  "prompt_zh_tw": "主角最後點了幾杯咖啡？",
  "options": [
    { "text": "한 잔 (一杯)", "is_correct": false },
    { "text": "두 잔 (兩杯)", "is_correct": true },
    { "text": "세 잔 (三杯)", "is_correct": false }
  ]
}
```

### 範例 2：A2 - Intent辨識 (約定時間)
```json
{
  "id": "A2-U02-CC2",
  "question_type": "intent",
  "prompt_zh_tw": "對方為什麼說「좀 바빠요 (有點忙)」？",
  "options": [
    { "text": "想約在別的時間", "is_correct": true, "feedback_zh_tw": "正確！這是委婉拒絕當前提議的方式。" },
    { "text": "他真的很討厭主角", "is_correct": false, "feedback_zh_tw": "韓文語境中，這通常只是在討論行程。" }
  ]
}
```

---

## 6. PM 評估準則 (Evaluation Rules)
- **覆蓋率**：單元內第一個 `immersion_input` 之後是否緊接 CC 節點？
- **有效性**：遮住原文翻譯，題目是否仍具備挑戰性？
- **反饋品質**：對於 `intent` 或 `next_response` 類題目，是否有具備解釋性的 `feedback_zh_tw`？
