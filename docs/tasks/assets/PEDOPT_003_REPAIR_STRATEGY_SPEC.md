# PEDOPT-003 — Repair Strategy Practice Spec

## 1. Goal
將「修復策略（Repair Strategy）」由單純的對話腳本提升為**互動策略訓練**。學習者不僅要背誦修復句子，更要學會「辨識溝通障礙點（Trigger Recognition）」並選擇「合適的修復手段（Repair Response）」。

本規格與 `PEDOPT-001` (理解檢查) 及 `PEDOPT-002` (變體練習) 互補，共同構成 `controlled_output` 的教學核心。

---

## 2. Trigger Taxonomy (為何需要修復？)

在練習中，系統（或虛擬對手）應模擬以下溝通障礙：

| 觸發類型 (trigger_type) | 定義 | 學習者反應目標 |
| :--- | :--- | :--- |
| **`muffled_audio`** | **聽不清/雜訊**：音檔帶有環境音或故意壓低音量。 | 要求重說或大聲點。 |
| **`semantic_gap`** | **語義不懂**：對方使用了學習者尚未學過的生詞。 | 要求解釋或換個說法。 |
| **`info_conflict`** | **資訊衝突**：對方說出的事實與前情提要不符（例如：訂房日期錯了）。 | 糾正資訊或確認事實。 |
| **`uncertain_intent`** | **意圖不明**：對方語氣模糊，不確定是同意還是反對。 | 進一步確認意圖。 |

---

## 3. Response Categories (如何修復？)

學習者應根據觸發條件選擇合適的回應類型：

| 回應類別 (repair_category) | 手段 | Dos | Don'ts |
| :--- | :--- | :--- | :--- |
| **`repeat`** | 要求重說 | 「다시 한번 말씀해 주세요.」 | 不要只發出「Eh?」或「Huh?」。 |
| **`slow_down`** | 要求放慢 | 「천천히 말씀해 주세요.」 | 適用於語速過快時。 |
| **`rephrase`** | 要求換個說法 | 「무슨 뜻이에요?」(這是什麼意思？) | 適用於單字不懂時。 |
| **`confirm`** | 確認資訊 | 「___(日期/價格) 맞아요?」 | 針對特定資訊點進行核實。 |
| **`reject_replace`** | 拒絕並更正 | 「아니요, __예요.」 | 用於修正明顯的資訊衝突。 |

---

## 4. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-RS",
  "candidate_type": "path_node",
  "content_form": "practice_card",
  "learning_role": "interaction_strategy",
  "payload": {
    "trigger_type": "muffled_audio | semantic_gap | info_conflict | uncertain_intent",
    "repair_goal": "repeat | slow_down | rephrase | confirm | reject_replace",
    "context_zh_tw": "情境描述 (例如：店員說得太快，你沒聽清楚金額。)",
    "audio_trigger_path": "path/to/distorted_audio.mp3",
    "expected_response_type": "speaking | selection",
    "tasks": [
      {
        "prompt_zh_tw": "請要求對方說慢一點",
        "target_examples": ["천천히 말해 주세요."],
        "acceptable_variants": ["천천히 해주세요", "조금만 천천히요"],
        "feedback_zh_tw": "當聽不懂長句子時，要求放慢速度是很好的策略。"
      }
    ]
  }
}
```

---

## 5. A1/A2 範例

### 範例 1：A1 - Information Conflict (旅館櫃檯)
- **Trigger**: 櫃檯人員說：「302號房，這是您的鑰匙。」(但你預定的是 305)
- **Repair Goal**: `reject_replace` (更正資訊)
- **Task**: 「아니요, 305호예요.」
- **練習點**: 數字聽辨 + 糾正勇氣。

### 範例 2：A1 - Muffled/Fast Audio (便利商店)
- **Trigger**: 店員咕噥了一串（語速快 + 背景音）。
- **Repair Goal**: `slow_down` (要求放慢)
- **Task**: 「죄송하지만 천천히 말씀해 주세요.」
- **練習點**: 掌握生存必備的「求援」句型。

### 範例 3：A2 - Semantic Gap (餐廳點餐)
- **Trigger**: 店員推薦：「저희 **시그니처** 메뉴 어떠세요?」(使用了外來語 signature，學生可能不懂)
- **Repair Goal**: `rephrase` (要求解釋)
- **Task**: 「'시그니처'가 무슨 뜻이에요?」(Signature 是什麼意思？)
- **練習點**: 訓練學生主動詢問不認識的單字，而非放棄對話。

---

## 6. PM 檢核清單 (PM Checklist)
- [ ] **真實性**：觸發條件是否在現實中常見？（如：車站廣播、吵雜的市場）
- [ ] **策略性**：是否明確標示了 `repair_goal`？學生是否知道自己為何而說？
- [ ] **多樣性**：單元內不可重複使用同一種 `repair_category` 超過兩次。
- [ ] **容錯度**：`acceptable_variants` 是否包含了口語化的對應表達？
- [ ] **關聯性**：是否與 `PEDOPT-002` 的 `correction` 題型做了區分？（RS 重點在於「主動發起修復」，TP 重點在於「語法變換」）

---

## 7. 與 PEDOPT-001/002 的關係說明
- `PEDOPT-001 (CC)`：確認「聽懂了沒」。
- `PEDOPT-002 (TP)`：確認「會不會換句話說」。
- `PEDOPT-003 (RS)`：確認「聽不懂時知不知道怎麼辦」。
- **三者結合**：形成從「被動理解」到「主動互動」的教學閉環。
