# PEDOPT-009 — Pedagogy Metadata Integration Spec

## 1. Goal
本文件定義如何將 `PEDOPT-001~008` 的教育優化規格整合至 `COURSE_UNIT_FACTORY` 的生產體系（Contract, Templates, Checkers）。目標是將文檔化的教育標準轉化為可執行、可檢驗的資料架構。

---

## 2. Integration Matrix (整合矩陣)

### 2.1 Unit Blueprint Contract (UNITFAC-001) Extensions
以下欄位將納入 `v0.1` 契約，作為 Production-Ready (PR) 單元的必填或選填項。

| 節點類型 | 欄位 (Path in Payload) | 類型 | 狀態 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **Comprehension Check** | `question_type` | Enum | **Required** | `info_extract`, `intent`, `next_response`, `sequence` |
| **Pattern Transform** | `transform_type` | Enum | **Required** | `slot`, `scenario`, `function`, `politeness`, `correction` |
| **Repair Practice** | `trigger_type` | Enum | **Required** | `muffled_audio`, `semantic_gap`, `info_conflict`, `uncertain_intent` |
| | `repair_goal` | Enum | **Required** | `repeat`, `slow_down`, `rephrase`, `confirm`, `reject_replace` |
| **Review Retrieval** | `target_type` | Enum | **Required** | `form`, `function`, `mixed` |
| | `retrieval_focus` | String | **Required** | 描述本次檢索的教學重點（zh-TW） |
| **Guided Output** | `task_family` | Enum | Optional | `sentence_completion`, `constrained_response`, `guided_rewrite`, `role_based_output` |
| | `required_elements` | List | Optional | 必須包含的韓文關鍵詞或句型 |
| **Dictionary Pack** | `readiness_tag` | Enum | Optional | `production_ready`, `input_only` (Default: `input_only`) |
| | `frame_refs` | List | Optional | 引用該詞項的單元或語法 ID |
| **Followup** | `followup_type` | Enum | **Required** | `review`, `transfer` |
| | `transfer_pattern_refs`| List | **Cond. Req**| 當 `followup_type` 為 `transfer` 時必填 |
| **Listening Micro** | `discrimination_target`| Enum | Optional | `minimal_pair`, `formality`, `numeral`, `particle` |

---

## 3. Checker Warning Rules (UNITFAC-004)
`mockup_check.py` 將新增以下規則。在 `v0.1` 過渡期，多數規則預設為 **Warning**，僅核心結構為 **Blocker**。

| 規則 ID | 嚴重程度 | 觸發條件 |
| :--- | :--- | :--- |
| **PED_MISSING_TYPE** | Warning | `comprehension_check` / `pattern_transform` 缺少 type 標籤。 |
| **PED_FOLLOWUP_INCONSISTENT**| **Blocker** | `followup_type: transfer` 但 `transfer_pattern_refs` 為空。 |
| **PED_MISSING_RETRIEVAL_FOCUS**| Warning | `review_card` 缺少 `retrieval_focus` 描述。 |
| **PED_LISTENING_NO_RATIONALE** | Warning | `listening_discrimination` 缺少 `distractor_rationale` 或 `feedback_zh_tw`。 |
| **PED_LOW_CC_DIVERSITY** | Warning | 單元內所有 CC 節點的 `question_type` 皆相同。 |
| **PED_LEGACY_DICTIONARY** | Warning | `dictionary_pack` 中存在 `readiness_tag: input_only` 卻被生產節點引用。 |

---

## 4. Authoring Template Updates (UNITFAC-005)
模板將更新 JSON 片段與 QA Checklist，引導作者填寫教育元數據。

### 4.1 JSON Snippet Expansion
例如，`comprehension_check` 的模板將強制要求 `question_type`。

### 4.2 QA Checklist Expansion
新增「教學品質維度」：
- [ ] CC 題型是否多樣化？
- [ ] Transform 是否包含 `scenario` 或 `function` 遷移？
- [ ] Followup 遷移目標是否明確引用了 Pattern ID？

---

## 5. Backward Compatibility & Migration
- **v0 Compatibility**: 既有單元（未標註 `v0.1`）在執行檢查時，以上 PED 規則將僅作為 **Info/Soft Warning**，不阻礙 CI 流程。
- **v0.1 Promotion**: 若單元要宣告為 Production-Ready，必須將 `version` 改為 `unit_blueprint_v0.1` 並修正所有 PED 相關警告。
- **Fixture Strategy**: 
    - `A1-U04` (Legacy): 保持 v0，容忍警告。
    - `A1-U05` (Pilot): 升級至 v0.1，作為首個完全符合教育元數據規範的單元。

---

## 6. Implementation Status
- [x] Mapping Table defined (this doc)
- [ ] UNITFAC-001 Contract Updated
- [ ] UNITFAC-005 Templates Updated
- [ ] UNITFAC-004 Checker Logic Spec Updated
- [ ] Task index sync
