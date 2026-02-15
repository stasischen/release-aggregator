---
description: 核心技能：Phase 1 翻譯與校對 (Translation & Review)。處理 `1_translation` 階段的內容確保。
---

# Skill: Phase 1 Translation (翻譯與校對)

這是管線的第二步。在結構 (Yarn) 確定後，確保翻譯內容的準確性與一致性。
This is the second step. After structure (Yarn) is set, ensure translation accuracy and consistency.

## 🎯 Objective

審查、修復並驗證 `1_translation/` 目錄下的 CSV 檔案，確保通過 QA 檢查。
Review, repair, and validate CSV files in `1_translation/` to ensure they pass QA checks.

## 🛑 Gatekeeper Protocol (嚴格把關協議)

**Warning**: This phase requires a mandatory "Gate 1 Pass" before proceeding to Phase 2.
**警告**：此階段必須通過「Gate 1 檢核」才能進入 Phase 2。

### Gate 1 Requirements:

1.  **Automated Check (自動檢查)**:
    - **Columns**: MUST verify existence of `trans_{lang}` for ALL languages in `EXTENDED_LANGUAGES` (defined in `constants.py`).
    - **Consistency**: No empty cells or `[TODO]` markers in these column.
2.  **Manual Verification (人工驗證)**:
    - **MUST review ALL Configured Languages**.
    - Confirm alignment across all columns.
3.  **Sign-off (簽核)**:
    - Create artifact `verified_p1.txt`.

## 📍 Resources

- **執行手冊 (SOP)**: [[1_translation/1_translation_sop.md]]
- **審查檢查表**: [[1_translation/resources/checklists.md]]
- **審查表格範本**: [[1_translation/resources/audit_template.md]]
- **驗證工具**: `python -m tools.v5.1_translation.validation {lang}`
