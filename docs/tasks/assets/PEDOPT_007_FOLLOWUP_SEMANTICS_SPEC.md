# PEDOPT-007 — Followup Semantics Spec (Review vs Transfer)

## 1. Goal
定義 `scheduled_followups` (+1/+3/+7 天) 的語義與教學任務分類。確保後的追蹤練習不只是隨機的複習提醒，而是具有明確「鞏固現有單元（Review）」或「遷移至新情境（Transfer）」目標的教學設計項目。

---

## 2. Followup Taxonomy (任務分類)

| 類型 (followup_type) | 教學目標 | 核心任務 |
| :--- | :--- | :--- |
| **`review`** | **強化鞏固**：確保學習者對該單元核心 pattern 的持久記憶。 | 在**相同或高度相似**的情境下進行檢索（Retrieval）。 |
| **`transfer`** | **應用遷移**：將學過的 pattern 轉移到全新情境，或結合舊單元知識。 | 在**跨單元、跨情境**的任務中主動使用 pattern（Application）。 |

---

## 3. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-FW-01",
  "followup_type": "review | transfer",
  "target_scope": "same_unit | cross_unit",
  "transfer_pattern_refs": [
    "pattern_id_01",
    "U04_pattern_greeting"
  ],
  "payload": {
    "title_zh_tw": "追蹤挑戰：情境應用",
    "task_prompt_zh_tw": "任務描述（例如：試試看在不同情境使用這句話）",
    "context_zh_tw": "情境說明（例如：你在機場，想詢問洗手間位置）",
    "expected_outcome": "預期教學效果（例如：正確使用 -주세요 請求協助）",
    "success_criteria": "檢核成功指標（例如：包含目的地詞彙與結尾語體）",
    "transfer_task_hint_zh_tw": "（選填）給作者的提示，說明如何設計此遷移任務"
  }
}
```

### 欄位說明 (Field Definitions)
- **`followup_type`**: 必填。區分是「複習鞏固」還是「情境遷移」。
- **`transfer_pattern_refs`**: **當 `followup_type` 為 `transfer` 時必填**。必須引用至少一個既有單元的 Pattern ID。
- **`target_scope`**: 區分是在本單元內情境變化 (`same_unit`)，還是跨越不同單元的主題 (`cross_unit`)。
- **`expected_outcome`**: 該追蹤點希望達到的學習心理狀態。
- **`success_criteria`**: 客觀可觀察的指標，用於後續可能的 AI 或人工審核。

---

## 4. Placement & Clarity Rules (放置與清晰度規則)

### 4.1 放置時機 (When to use Review vs Transfer)
- **Review (+1 Day)**: 重點在「對抗遺忘」。建議回饋該單元最重要的 1-2 個核心句子或 Block。
- **Transfer (+3 / +7 Day)**: 重點在「活化應用」。大腦已經稍微遺忘細節時，強制將 Pattern 放入新情境（如由咖啡廳移至辦公室）最能激發深層內化。

### 4.2 跨單元任務清晰度 (Cross-unit Task Clarity Rules)
1. **明確引用源 (Explicit Source)**: 所有跨單元遷移必須在 `transfer_pattern_refs` 中列出所有依賴的舊知識點。
2. **單一核心任務 (Single Critical Task)**: 一個 Followup 應只解決一個主要遷移目標 (Main Transfer Goal)。若需要混合多個單元，應在提示中明確指出哪個是主、哪個是輔。
3. **場景區隔度 (Contextual Contrast)**: 遷移任務的情境描述必須與原單元有 50% 以上的差異（例：購物 vs 問路、對店員說 vs 對同事說）。
4. **低認知負荷 (Low Cognitive Load)**: 遷移任務應專注於「舊知識在新場景的應用」，不應在 Followup 節點中引入全新的生詞（除非該生詞為 Context 必需且有提供提示）。

### 4.3 反模式 (Anti-Patterns)
- **Ambiguous Prompts**: 提示只寫「複習昨天的內容」或「翻譯這句話」。
- **Mixed Intent**: 同一個節點既想複習單詞，又想練習文法，又要做情境遷移。
- **Disconnected Transfer**: 標註為 `transfer` 卻沒有引用任何 Pattern ID，導致無法追蹤學生的學情模型。
- **Slot-Fill as Transfer**: 只是把「蘋果」換成「香蕉」，情境不變。這算 `review` 或 `same_unit TP`，不算 `transfer`。

---

## 5. A1/A2 Examples

### 範例 1：A1 - Review (點餐鞏固)
- **Followup Type**: `review`
- **Target Scope**: `same_unit`
- **Context**: 昨天你在咖啡廳練習了點餐，現在試試看你還記得怎麼跟店員要東西嗎？
- **Task Prompt**: 「請給我一杯拿鐵」
- **Expected Outcome**: 鞏固 `[物品] + 주세요` 結構。
- **Success Criteria**: 包含 `라떼` 與 `주세요`。

### 範例 2：A1 - Transfer (從咖啡廳到藥局)
- **Followup Type**: `transfer`
- **Target Scope**: `cross_unit`
- **Transfer Pattern Refs**: `["A1-U04-P01 (주세요)"]`
- **Context**: 你現在在**藥局 (약국)**。你感冒了，需要買感冒藥。
- **Task Prompt**: 請試著用昨天學過的「拜託」、「給」的語氣買藥。
- **Expected Outcome**: 將服務請求語法遷移至不同交易場景。
- **Success Criteria**: 正確產出包含 `감기약` 與 `주세요` 的句子。

### 範例 3：A2 - Review (邀約婉拒)
- **Followup Type**: `review`
- **Target Scope**: `same_unit`
- **Context**: 還記得昨天朋友約你吃飯但你拒絕了嗎？再次練習如何委婉拒絕。
- **Task Prompt**: 「我今天有點忙，所以可能去不了...」
- **Expected Outcome**: 強化 `-아/어서` (理由) 與語氣連結。
- **Success Criteria**: 包含正確的連接詞與結尾語體。

### 範例 4：A2 - Transfer (工作任務結合生活)
- **Followup Type**: `transfer`
- **Target Scope**: `cross_unit`
- **Transfer Pattern Refs**: `["A2-U05-P02 (詢問時間)", "A2-U01-P01 (敬語基礎)"]`
- **Context**: 你在會議結束後，想跟韓國同事確認「晚上幾點吃飯」。
- **Task Prompt**: 請結合第一單元的禮貌語體與本單元的時間詢問。
- **Expected Outcome**: 跨單元知識點整合，提升溝通流暢度。
- **Success Criteria**: 語體等級正確（polite）且成功詢問時間。

---

## 6. PM & Reviewer Checklist

- [ ] **類型標註**：+1 followups 是否大多標註為 `review`？+3 以上是否包含 `transfer`？
- [ ] **連動完整**：所有 `transfer` 任務是否都有 `transfer_pattern_refs`？
- [ ] **跨單元明確**：涉及跨單元整合時，`target_scope` 是否正確設為 `cross_unit`？
- [ ] **成功標竿**：`success_criteria` 是否能量化或具體觀察？
- [ ] **區隔度評估**：`transfer` 任務與原單元的情境是否具備足夠的差異化？
