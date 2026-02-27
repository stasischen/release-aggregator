# PEDOPT-002 — Transform Practice Spec

## 1. Goal
定義 `pattern_transform` 的教育目標與題型分類，確保變體練習（Drill/Practice）不只是機械式的換字，而是具備「場景遷移」與「語言功能轉換」的教育價值。

---

## 2. Transform Types (題型分類)

| 類型 (transform_type) | 定義 | 教育價值 |
| :--- | :--- | :--- |
| **`slot`** | **槽位替換**：替換句子中的名詞或動詞。 | 鞏固基礎語法結構與核心詞彙。 |
| **`scenario`** | **場景變換**：將學到的句型套用到另一個類似場景。 | 提升跨情境的語言遷移能力。 |
| **`function`** | **功能變換**：從「詢問」轉為「陳述」，或「否定」轉為「肯定」。 | 靈活用法切換，非死背句子。 |
| **`politeness`** | **語體/敬語轉換**：切換半語、尊待語（해요體 vs. 습니다體）。 | 掌握韓文核心的社會語用邏輯。 |
| **`correction`** | **錯誤修正/矛盾轉換**：根據給予的提示（如：不對、沒有）調整句子。 | 訓練否定句、修復策略與資訊精確度。 |

---

## 3. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-TP",
  "candidate_type": "path_node",
  "content_form": "practice_card",
  "learning_role": "controlled_output",
  "payload": {
    "transform_type": "slot | scenario | function | politeness | correction",
    "base_sentence_ko": "저는 커피를 마셔요.",
    "instruction_zh_tw": "請換成「茶」來練習",
    "tasks": [
      {
        "prompt_zh_tw": "換成：茶 (차)",
        "target_examples": ["저는 차를 마셔요."],
        "hint_keywords": ["차"]
      }
    ]
  }
}
```

---

## 4. A1/A2 範例 (跨場景)

### 範例 1：A1 - Slot Transform (咖啡廳)
- **Base**: 「Americano 주세요.」
- **Transform**: 換成 Latte (라떼)。
- **目的**: 熟練 `___ 주세요` 結構。

### 範例 2：A1 - Scenario Transform (藥局)
- **Context**: 剛才在咖啡廳學會了點餐。
- **Transfer**: 現在在藥局，你要買感冒藥 (감기약)。
- **Task**: 「감기약 주세요.」
- **目的**: 讓學生理解該句型在「購買行為」中是通用的。

### 範例 3：A2 - Politeness Transform (職場 vs. 朋友)
- **Base**: 「어디에 가요?」(해요體 - 普通尊敬)
- **Transform**: 換成對長輩/上司說的尊待語。
- **Target**: 「어디에 가세요?」
- **目的**: 區分主體尊重的用法。

### 範例 4：A2 - Correction Transform (旅館)
- **Prompt**: 「房號是 302 嗎？」(提示：不是，是 305)
- **Target**: 「아니요, 305호예요.」
- **目的**: 練習否定句與修正正確資訊。

---

## 5. Progression Rules (進階規則)
1. **A1 初期**：以 `slot` 為主，確保句框穩固。
2. **A1 中後期**：引入 `scenario`，打破「場景 = 句型」的死板連結。
3. **A2**：增加 `function` 與 `politeness`，開始處理語用差異。
4. **所有等級**：在單元末尾的 `controlled_output` 應包含至少兩個不同 `transform_type` 的練習。

---

## 6. PM 評估準則 (Evaluation Rules)
- **遷移性**：練習是否只是把單元內的單字輪流換一遍？是否有嘗試帶入新單字或新場景？
- **提示清晰度**：`instruction_zh_tw` 是否能讓學生明確知道要「轉」什麼？（避免猜題）
- **連續性**：Transform 是否與前方的 `immersion_input` 邏輯掛鉤？
