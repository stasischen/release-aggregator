# PEDOPT-004 — Review Retrieval Target Spec

## 1. Goal
定義 **檢索複習 (Retrieval/Review)** 的目標分類與規格，確保複習環節不只是單純的「看到句子後翻譯」，而是能針對「語言形式 (Form)」或「溝通功能 (Function)」進行有意識的提取練習。目標是提升學習者在不同時間點（當天/隔天/一週後）的記憶回收精度。

---

## 2. Taxonomy (檢索分類)

| 類型 (target_type) | 定義 | 教學目標 (Retrieval Focus) |
| :--- | :--- | :--- |
| **`form`** | **形式檢索**：側重於特定語法結構或詞綴。 | 確保能否正確拼裝句子（如：敬語尾綴、時態標記）。 |
| **`function`** | **功能檢索**：側重於在特定情境下的直覺反應。 | 確保在情境出現時，能第一時間提取出合適的社交語句。 |
| **`mixed`** | **混合檢索**：要求在維持功能反應的同時，滿足特定形式限制。 | 訓練「在正確情境下使用正確語體」的綜合能力。 |

---

## 3. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-RV",
  "candidate_type": "path_node",
  "content_form": "practice_card",
  "learning_role": "retrieval_review",
  "payload": {
    "target_type": "form | function | mixed",
    "retrieval_focus": "本次檢索的核心重點 (例如：時態變化 / 點餐反應)",
    "context_zh_tw": "情境描述 (例如：你在餐廳，想要點咖啡)",
    "prompt_zh_tw": "提示文字 (例如：請用韓文說「請給我咖啡」)",
    "expected_signal": "預期觸發的語言特徵 (例如：-아요/어요 ending, 주세요 suffix)",
    "target_examples": ["커피 주세요."],
    "acceptable_variants": ["커費 한 잔 주세요", "아메리카노 주세요"],
    "feedback_zh_tw": "針對該檢索點的教學解析"
  }
}
```

---

## 4. Placement Guidelines (單元位置與放置指引)

### 放置點建議：
1. **Near-Transfer (當旬複習)**：
   - 位於單元末尾的 `controlled_output` 區段。
   - 目的：驗證剛學完的內容是否能在情境提示下直接提取，而非看著範例抄。
2. **Periodic Retrieval (延時複習)**：
   - 位於 `+1` (隔日) 或 `+3` (三日後) 的 Followup 節點。
   - 目的：對抗遺忘曲線，測試脫離單元上下文後的提取能力。

### 與其他節點的關係：
- **Comprehension Check (CC)** 驗證「有沒有入大腦」。
- **Transform Practice (TP)** 驗證「能不能換著說」。
- **Retrieval Target (RV)** 驗證「在沒看到提示時，能不能從腦中找出來」。

---

## 5. A1/A2 範例

### 範例 1：A1 - Function Retrieval (日常問候)
- **Target Type**: `function`
- **Retrieval Focus**: 社交初次見面的直覺反應。
- **Context**: 遇見新朋友，想用韓文打招呼。
- **Prompt**: 「初次見面，請多指教」
- **Expected Signal**: `처음 뵙겠습니다`
- **Placement**: A1-U01 單元末尾。

### 範例 2：A1 - Form Retrieval (數字與量詞)
- **Target Type**: `form`
- **Retrieval Focus**: 固有詞數字與量詞 `병` (瓶) 的結合。
- **Context**: 在便利商店買水。
- **Prompt**: 「請給我兩瓶水」
- **Expected Signal**: `두` (不是 둘) + `병`
- **Placement**: A1-U05 Followup (+1)。

### 範例 3：A2 - Mixed Retrieval (邀約與婉拒)
- **Target Type**: `mixed`
- **Retrieval Focus**: 邀約情境 + 委婉語氣 (-고 싶다 + -는데)。
- **Context**: 朋友邀你去唱歌，但你今天很累。
- **Prompt**: 「雖然我也想去，但今天有點累...」
- **Expected Signal**: `가고 싶은데` (反折語氣)
- **Placement**: A2-U03 單元中段回顧區。

### 範例 4：A2 - Function Retrieval (求助修復)
- **Target Type**: `function`
- **Retrieval Focus**: 溝通卡住時的求助策略。
- **Context**: 當對方說太快你聽不懂時，你會說？
- **Prompt**: 「請再說一次」
- **Expected Signal**: `다시 한번 말해 주세요`
- **Placement**: A2-U10 Followup (+3)。

---

## 6. PM Checklist (檢核清單)

PM 在測試或審核時應確認：
- [ ] **檢索價值**：題目是否真的需要「從腦中搜尋」？（如果背景已經貼著正確答案的例句，就失去檢索意義，變成單純重複）
- [ ] **情境關聯**：`context_zh_tw` 是否足以誘發正確的 `target_type`？
- [ ] **提示顆粒度**：`prompt_zh_tw` 不應包含太多「單對單翻譯提示」，例如：不要寫「請說：茶 (차) 給我」，應寫「請說想喝茶」。
- [ ] **容錯餘裕**：`acceptable_variants` 是否涵蓋了符合溝通功能但形式略異的正確句子？

---

## 7. Common Failure Cases (常見失敗案例)

1. **Only-Translation Clue**：
   - 錯誤：提示寫「請翻譯：커피 주세요 → 請給我咖啡」。
   - 原因：這是在考翻譯，不是在考情境下的檢索。
2. **Zero-Recall Burden**：
   - 錯誤：在同一個畫面上方顯示範例，下方要求複習。
   - 原因：大腦不需要「提取」，只需「複製」。
3. **Over-Ambiguous Prompts**：
   - 錯誤：情境寫「在外面」，提示寫「說一句話」。
   - 原因：範圍太廣，學習者無法判斷要提取哪一個知識點。
4. **Incorrect Form Focus**：
   - 錯誤：要求 A1 學生檢索 A2 才會學到的語體變換。
   - 原因：超出能力的複習會導致挫折感而非鞏固。
