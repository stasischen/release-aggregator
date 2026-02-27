# PEDOPT-011 — PM Educational QA Checklist v2

## 1. Overview
本文件將 `PEDOPT-001~010` 的教育優化成果轉化為 PM 審核（Trial Review）時的可操作工具。目標是確保所有量產單元（Unit Blueprint v0.1+）在進入凍結（Freeze）前，均通過一致的高品質教育檢核。

---

## 2. PM Inspection Checklist (by Domain)

### 2.1 Comprehension Checks (CC) — [PED-COMP]
*驗證「有沒有入大腦」，防止無效翻譯依賴。*

- **PM Inspection Questions**:
  - [ ] 題目是否具備「意圖」或「語境」深度，而非單純的單字翻譯？
  - [ ] 遮住原文翻譯後，題目是否仍具備挑戰性？
  - [ ] 干擾項是否包含「聽起來很像但意思不對」的詞？
- **Acceptance Criteria**:
  - 第一個 `immersion_input` 之後必須緊接 CC。
  - 單元內至少包含兩種不同 `question_type` (如 `info_extract` + `intent`)。
- **Common Failure Patterns**:
  - 題目過於簡單（如：這句話是中文什麼意思？）。
  - 所有 CC 題型皆為單一分類。
- **Escalation Threshold**: 若單元無 CC 或 CC 全數為單純翻譯題 $\rightarrow$ **Blocker**.

### 2.2 Transform Practice (TP) — [PED-TRANSFORM]
*驗證「能不能換著說」，打破死記硬背。*

- **PM Inspection Questions**:
  - [ ] 練習是否包含「場景遷移」（Scenario）或「功能轉換」（Function）？
  - [ ] 指示語 (`instruction_zh_tw`) 是否清晰，防止學生猜題？
- **Acceptance Criteria**:
  - `v0.1` 必須標註 `transform_type`。
  - A1 單元末尾應包含跨場景的 `scenario` 或 `function` 遷移。
- **Common Failure Patterns**:
  - 機械式換字（僅 `slot` 變換）。
  - 提示過於模糊導致無法作答。
- **Escalation Threshold**: 若單元末尾僅包含 `slot` 變換且無場景遷移 $\rightarrow$ **Major**.

### 2.3 Repair Strategy (RS) — [PED-REPAIR]
*驗證「聽不懂時怎麼辦」，培養對話韌性。*

- **PM Inspection Questions**:
  - [ ] 觸發情境（如聽不清、語義不懂）是否在現實中常見？
  - [ ] 學生是否清楚其 `repair_goal`（例如：是要求重說還是要求放慢）？
- **Acceptance Criteria**:
  - 必須標註 `trigger_type` 與 `repair_goal`。
  - 提供的 `acceptable_variants` 需包含口語化的正確表達。
- **Common Failure Patterns**:
  - 將「糾正錯誤資訊」與「變體練習」混淆（RS 應強調主動發起）。
- **Escalation Threshold**: 若修復練習不符合 `trigger_type` 邏輯 $\rightarrow$ **Major**.

### 2.4 Review Retrieval & Followup — [PED-RETRIEVAL / PED-FOLLOWUP]
*驗證「延時記憶提取」，確保教學閉環。*

- **PM Inspection Questions**:
  - [ ] 檢索題是否真的需要「從腦中搜尋」（畫面上方無答案）？
  - [ ] Followup 遷移任務是否與原單元情境有足夠區隔（>50% 差異）？
- **Acceptance Criteria**:
  - `followup_type: transfer` 必須填寫 `transfer_pattern_refs`。
  - 所有 `review_card` 必須有明確的 `retrieval_focus`。
- **Common Failure Patterns**:
  - Followup 淪為隨機複習，無明確遷移目標。
- **Escalation Threshold**: `transfer` 類追蹤任務未引用 Pattern ID $\rightarrow$ **Blocker (Checker Enforced)**.

### 2.5 Guided Output Rubric — [PED-OUTPUT]
*驗證「自由產出品質」，定義完成標準。*

- **PM Inspection Questions**:
  - [ ] `required_elements` 是否具備（不會判錯對的答案）？
  - [ ] 反饋微型提示 (`hint_zh_tw`) 是否能引導修正而非直接給答案？
- **Acceptance Criteria**:
  - 必須區分 `PASS`, `REVISE`, `FAIL` 三種路徑。
  - 排除 A2 對上司使用半語等嚴重語氣錯誤。
- **Common Failure Patterns**:
  - Rubric 太鬆（什麼都過）或太嚴（忽略合法拼寫變體）。
- **Escalation Threshold**: 核心語法錯誤卻被標註為 `PASS` $\rightarrow$ **Blocker**.

### 2.6 Dictionary Readiness — [PED-DICT]
*驗證「詞彙生產品質」，防止雜訊干擾。*

- **PM Inspection Questions**:
  - [ ] `production_ready` 詞項是否具備正確的 `register_hints`？
  - [ ] 是否存在無人引用 (`frame_refs` 為空) 的孤兒詞？
- **Acceptance Criteria**:
  - 非生產詞項必須標註為 `input_only`。
- **Common Failure Patterns**:
  - 專業生僻詞被標記為 A1 生產詞。
- **Escalation Threshold**: 核心詞項缺少語氣標註 $\rightarrow$ **Major**.

### 2.7 Listening Micro-node — [PED-LISTEN / PED-METADATA]
*驗證「聽覺辨識風險」，鎖定生存瓶頸。*

- **PM Inspection Questions**:
  - [ ] 辨識目標（如 ㄱ vs ㄲ）是否屬於該級別的高頻誤導點？
  - [ ] 答錯反饋是否解釋了「如何聽出差異」？
- **Acceptance Criteria**:
  - 必須包含 `distractor_rationale` (為什麼會錯)。
- **Common Failure Patterns**:
  - LD 節點數量過多（單元建議不超過 2 個）。
- **Escalation Threshold**: LD 缺少聽覺差異描述 $\rightarrow$ **Minor**.

---

## 3. Triage Label System

### 3.1 Severity Labels
| 標籤 | 定義 | 處理優先序 |
| :--- | :--- | :--- |
| **`severity:blocker`** | 違反核心教育規格，或 Checker 報錯，阻礙凍結。 | 立即修復 (Stop-the-line) |
| **`severity:major`** | 教學設計有瑕疵，影響學習效果但不阻礙流程。 | 下一版修正 (Fix before next Pilot) |
| **`severity:minor`** | 文字微調、格式美化。 | 累積處理 |

### 3.2 Type Labels (PED-*)
- `PED-COMP`: 理解檢查問題。
- `PED-TRANSFORM`: 變體遷移問題。
- `PED-REPAIR`: 修復策略問題。
- `PED-RETRIEVAL`: 檢索提取問題。
- `PED-FOLLOWUP`: 追蹤任務邏輯問題。
- `PED-OUTPUT`: Guided Rubric 問題。
- `PED-DICT`: 字典標籤/語氣問題。
- `PED-LISTEN`: 聽力辨識問題。
- `PED-METADATA`: 通用元數據缺失。

### 3.3 Action Labels
- `author-fix`: 需作者調整內容或 Payload。
- `spec-gap`: 規格本身不支援，需調整 PEDOPT 文檔。
- `checker-gap`: Checker 漏報或誤報。
- `contract-gap`: Blueprint Schema 需擴充。

---

## 4. Decision Rules (Pass/Fail/Revise)

- **PASS**: 
  - 所有 Blocker 已修正。
  - 符合單元結構多樣性（CC/TP/RS/RV 均有覆蓋）。
- **REVISE**: 
  - 存在 3 個以上 Major 缺陷。
  - 元數據填寫不完整但內容尚可。
- **FAIL**: 
  - 缺少核心教學節點。
  - 語氣標註（Register）與場景完全相反。

---

## 5. Example Issue Classifications

| 情境描述 | Triage Labels | 分類理由 |
| :--- | :--- | :--- |
| A1-U04 Followup 轉到藥局，但沒有填寫 `transfer_pattern_refs`。 | `severity:blocker`, `PED-FOLLOWUP`, `author-fix` | 極高優先級。缺少引用會導致學情追蹤斷裂。 |
| A1-U05 單元內所有理解檢查 (CC) 都是「資訊提取」，沒有「意圖辨識」。 | `severity:major`, `PED-COMP`, `author-fix` | 題型單一，違反「教學多樣性」準則。 |
| 點餐詞項 `주세요` 解析正確，但標籤標記為 `input_only` 且無語氣提示。 | `severity:major`, `PED-DICT`, `author-fix` | 核心詞未晉升生產，會導致前端無法正確顯示。 |
| 聽力微節點 (LD) 答錯反饋寫「你聽錯了」，沒解釋聲音差異。 | `severity:minor`, `PED-LISTEN`, `author-fix` | 反饋品質不佳，不阻礙功能但無教學價值。 |
| 想要標記「語速太快」觸發器，但 Schema 中沒有這個 Enum。 | `severity:minor`, `PED-REPAIR`, `spec-gap` | 規格缺口，需反饋給 Arch 組。 |

---

## 6. Checklist v2 Completion Status
- [x] Domains mapped to PEDOPT specs
- [x] PM inspection questions defined
- [x] Triage label system established
- [x] PASS/FAIL rules defined
- [x] Example classifications provided
