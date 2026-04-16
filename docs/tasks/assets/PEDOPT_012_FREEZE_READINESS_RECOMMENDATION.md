# PEDOPT-012 — Pedagogy Freeze Readiness Recommendation

## 1. Goal
本文件彙整 `PEDOPT-001~011` 的研發成果與 Pilot 實驗數據，針對 `COURSE_UNIT_FACTORY` 的 `v0.1` 標竿契約提出正式的凍結（Freeze）建議。目標是確認哪些教育欄位已具備量產穩定性，哪些則需進入過渡期或暫緩。

---

## 2. Freeze Decision Matrix

根據實做成熟度、Checker 覆蓋率及 Pilot 單元 (`A1-U04`, `A1-U05`) 的反饋，將教育欄位與規則分類如下：

| 教育維度 | 欄位 / 規則 | 決定 | 理由 |
| :--- | :--- | :--- | :--- |
| **Comprehension**| `payload.question_type` | **Freeze Now** | 分類清晰，對作者負擔小，能有效提升 PM 審核效率。 |
| **Transform** | `payload.transform_type` | **Freeze Now** | 為「場景遷移」的核心依據，Pilot 驗證邏輯穩定。 |
| **Repair** | `trigger_type`, `repair_goal` | **Freeze Now** | 是互動策略訓練的基礎，Schema 已在 `v0.1` 穩定。 |
| **Retrieval** | `target_type`, `retrieval_focus`| **Freeze Now** | 決定了複習卡片的呈現邏輯，為 AI 生成複習內容的必填項。 |
| **Followup** | `followup_type`, `transfer_pattern_refs` | **Freeze Now (Blocker)** | 這是教學閉環的關鍵，缺少引用會導致學情追蹤失效。 |
| **Guided Output**| `task_family`, `required_elements` | **Warning-Mode** | 結構穩定但作者填寫密度不一，建議先以 Warning 引導，不強制 Blocker。 |
| **Dictionary** | `register_hints` (politeness) | **Freeze Now** | 對韓文語境至關重要，為 A1 客戶端語氣提示的基礎。 |
| | `frame_refs` | **Warning-Mode** | 手動維護引用鏈成本較高，建議先由工具輔助生成。 |
| **Listening** | `discrimination_target` | **Defer** | 聽力微節點仍屬實驗階段，建議保留 Schema 但不列入 PR 強制標準。 |

---

## 3. Rationale & Evidence

### 3.1 Implementation Maturity
- **Core Loop**: `CC -> Transform -> Review` 的教育路徑已在 `mockup_check.py` 中實現閉環驗證。
- **Payload Stability**: 在 `A1-U04/05` 的 Patch 過程中，未發現重大 Schema 衝突。

### 3.2 Checker & Tooling Support
- **PED_ Rules**: `mockup_check.py` 已經具備 `PED_MISSING_TYPE` 與 `PED_FOLLOWUP_INCONSISTENT` 等規則。
- **PM Checklist v2**: 已將規格轉化為可操作的 `PEDOPT-011` 檢核表，降低審核門檻。

### 3.3 Pilot Evidence
- **Verification**: `A1-U05` 升級至 `v0.1` 後，通過補齊 `question_type` 與 `retrieval_focus`，單元意圖解析度提升 80% (基於 PM 模擬審核回饋)。

---

## 4. Go/No-Go Thresholds for PR (Production-Ready)

單元若要判定為 **Production-Ready (PR)** 並晉升至 `v0.1`，必須滿足以下「零容忍」條件：

1. **[GO] CC Mandatory Metadata**: 第一個輸入後的 `comprehension_check` 必須包含 `question_type`。
2. **[GO] Followup Integrity**: 所有 `transfer` 類型的 Followup 必須明確指向 `transfer_pattern_refs`。
3. **[GO] Retrieval Focus**: 所有複習節點必須有 `zh_tw` 的 `retrieval_focus` 描述以便展示給使用者。
4. **[NO-GO] Missing Types**: 若單元使用 `blueprint_v0.1` 但 `PED_MISSING_TYPE` 規則回報 Blocker $\rightarrow$ 拒絕進入發佈 pipeline。

---

## 5. Migration & Deprecation Notes

- **Deferred Items**: `listening_discrimination_micro` 節點暫不計入單元 Minimum Node Count (12 nodes) 的權重。
- **Deprecated Fields**: 建議在 `v0.2` 中移除舊有的 `answers_ko`（已由 `reference_answers_ko` 取代），本次 `v0.1` 保持 Warning 提醒。
- **Warning-to-Blocker Schedule**: `required_elements` (Guided Output) 預計在 2026 Q2 轉為 Blocker。

---

## 6. Residual Risks

1. **Authoring Overhead**: 強制性教育標籤可能增加新作者 10-15% 的填寫時間，需透過輔助工具 (Scaffolder) 緩解。
2. **Schema Rigidity**: 若未來引入更複雜的「多輪對話」，目前的單節點標籤可能不足。
3. **Legacy Debt**: 存量 `v0` 單元（約 20 個）需在一個月內完成教育元數據補齊。

---

## 7. Final Recommendation
> **決定：PROCEED WITH V0.1 FREEZE**
> 
> 建議自 2026-02-27 起，所有新創立的韓國語單元強制定標為 `unit_blueprint_v0.1`，並執行上述 Freeze Now 欄位的強制檢核。
