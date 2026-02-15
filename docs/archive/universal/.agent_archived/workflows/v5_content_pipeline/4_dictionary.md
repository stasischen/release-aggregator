---
description: Phase 4 Dictionary (Dictionary Build & Enrichment)
---

# Phase 4: Dictionary (字典構建)

本階段負責將映射表 (Chunk Mapping) 與多語言翻譯進行同步與豐富化。
This phase syncs and enriches the Chunk Mapping with multilingual translations.

## 🎯 Goal

- **Synchronization**: Sync translations from Phase 1 to dictionary entries.
- **Enrichment**: Fill in missing definitions for all target languages.
- **Consistency**: Ensure terminology is consistent across the project.

## 🛑 Gatekeeper Protocol (嚴格把關協議)

**Warning**: This phase requires a mandatory "Gate 4 Pass" before proceeding to Phase 5.
**警告**：此階段必須通過「Gate 4 檢核」才能進入 Phase 5。

### Gate 4 Requirements:

1.  **Automated Check (自動檢查)**:
    - **Coverage**: All chunks must have definitions in **ALL Configured Languages**.
    - (Config Source: `tools.v4.utils.constants.EXTENDED_LANGUAGES`)
2.  **Manual Verification (人工驗證)**:
    - **Review EVERY ATOM TRANSLATION** in `ko_lingoblocks_*.csv`.
    - **Verify semantic correctness** for ALL Configured Languages.
    - **Strictly No 'Hallucinations'**: Verify against source context if needed.
3.  **Sign-off (簽核)**:
    - Create artifact `verified_p4.txt`.

## 🛠 Tools

- `python -m tools.v5.core.sync {lang}`

## 📚 Resources

- [[4_dictionary/4_dictionary_sop.md]]
- [[4_dictionary/resources/checklists.md]]
