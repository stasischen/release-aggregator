---
description: Phase 5 Build (Course Pack Compilation & QA)
---

# Phase 5: Build (全視圖構建)

本階段將原子 (Structure) 與翻譯 (Content) 合併，生成用於最終審核的 Full View CSV。
This phase merges Atoms (Structure) and Translations (Content) to generate the Full View CSV for final audit.

## 🎯 Goal

- **Merger**: Combine `atoms.csv` and `trans.csv` into `full.csv`.
- **Final Audit**: Verify the complete dataset before compilation.

## 🛑 Gatekeeper Protocol (嚴格把關協議)

**Warning**: This phase requires a mandatory "Gate 5 Pass" before release.
**警告**：此階段必須通過「Gate 5 檢核」才能發布。

### Gate 5 Requirements

1. **Automated Check (自動檢查)**:
    - **Zero Error Tolerance**: `audit_view.py` scan must return 0 errors for **ALL Configured Languages** (defined in `constants.py`).
2. **Manual Verification (人工驗證)**:
    - Review Full View CSVs.
    - **Verify EVERY LANGUAGE column** (dynamic based on config) is correct and visible.
    - Confirm `trans_id` matches Phase 1 source.
3. **Sign-off (簽核)**:
    - Create artifact `verified_p5.txt`.

## 🛠 Tools

- `python -m tools.v5.core.merger {lang}`
- `python tools/v5/5_build/audit_view.py`

## 📚 Resources

- [[5_full_view/5_full_view_sop.md]]
- [[5_full_view/resources/checklists.md]]
