# PEDOPT-010 — Pilot Application & Review Report

## 1. Overview
本文件記錄 `COURSE_PEDAGOGY_OPTIMIZATION` 第一階段 Pilot 執行結果。透過在 `A1-U04` 與 `A1-U05` 兩個量產級單元中實做 `PEDOPT-001~009` 所定義的教育元數據，驗證規格的可操作性與檢查工具的有效性。

---

## 2. Pilot Summary

| Pilot Unit | Theme | Migration Action | Status |
| :--- | :--- | :--- | :--- |
| **A1-U04** | Coffee Ordering | Upgraded to `v0.1`, patched CC/Review types, added followup pattern refs. | **PASSED** |
| **A1-U05** | Pharmacy | Patched CC/Transform/Repair/Review types, added followup types. | **PASSED** |

---

## 3. Checker Results (Evidence)

### 3.1 Initial Run (Before Patching)
使用了更新後的 `mockup_check.py`（包含 PED_ 規則）執行初始掃描：

- **A1-U04**: 3 Warnings
  - `PED_MISSING_TYPE` (Comprehension Check)
  - `PED_MISSING_TYPE` (Review Card)
  - `PED_MISSING_RETRIEVAL_FOCUS` (Review Card)
- **A1-U05**: 1 Blocker Error, 5 Warnings
  - `ERR_VERSION_MISMATCH` (Blocker, version 0.1 was unrecognized)
  - `PED_MISSING_TYPE` (CC, Review, Followups)
  - `PED_MISSING_RETRIEVAL_FOCUS` (Review)

### 3.2 Final Run (After Patching)
在補全元數據並升級 Checker 穩定性後執行最終驗證：

- **A1-U04**: **0 Errors, 0 Warnings**
- **A1-U05**: **0 Errors, 0 Warnings**

---

## 4. Integration Evidence (Patches Applied)

### 4.1 Metadata Field Wiring
以下欄位已成功對接至 Pilot JSON：
- `payload.question_type`: `info_extract`
- `payload.transform_type`: `slot`
- `payload.trigger_type`: `semantic_gap`
- `payload.repair_goal`: `repeat`
- `payload.target_type`: `mixed`
- `payload.retrieval_focus`: zh-TW focus description
- `scheduled_followups[].followup_type`: `transfer`
- `scheduled_followups[].transfer_pattern_refs`: Explicit pattern IDs (e.g., `["주세요"]`)

---

## 5. Findings & Recommendations

### 5.1 Findings
1. **Low Authoring Friction**: 新增的欄位（如 `question_type`）對作者負擔極小，但能大幅提升 PM 審核時的意圖辨識速度。
2. **Followup Clarity**: 透過 `transfer_pattern_refs` 強制引用，能有效防止 Followup 變成隨機練習，確保教學閉環。
3. **Checker Effectiveness**: `mockup_check.py` 的警告能精確定位遺漏的教育屬性，適合納入 PR Lint 流程。

### 5.2 Freeze-Readiness Recommendation
- **穩定度評估**: 核心教育欄位及其 Enums 表現穩定，無顯著 schema 衝突。
- **後續步驟**:
  - `PEDOPT-011`: 將上述檢核點轉化為 PM 教學 QA Checklist。
  - `PEDOPT-012`: 建議將 `v0.1` 作為 Production-Ready 的基準版本，正式凍結相關教育欄位。

---

## 6. Files Changed in Pilot
- `docs/tasks/mockups/a1_u04_unit_blueprint_v0.json` (Upgraded to v0.1)
- `docs/tasks/mockups/a1_u05_unit_blueprint_v0.json` (Patched)
- `scripts/mockup_check.py` (Updated with Pedagogy Rules)
