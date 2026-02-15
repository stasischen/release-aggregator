---
description: 核心技能：Phase 3 映射 (Mapping)。負責將原子化內容 (Atoms) 轉換為去重後的詞塊映射表 (Chunk Mapping)，並檢測同音異義詞衝突。
---

# Phase 3: Mapping (映射)

本階段將 Phase 2 的原子內容 (Atoms) 聚合與去重，建立 Chunk Mapping。
This phase aggregates and deduplicates atoms from Phase 2 to build the Chunk Mapping.

## 🎯 Goal

- **Extraction**: Extract unique chunks from atoms.
- **Deduplication**: Assign unique IDs to unique chunks.
- **Handling Homophones**: Detect and resolve ID collisions for same-text/different-meaning terms.

## 🛑 Gatekeeper Protocol (嚴格把關協議)

**Warning**: This phase requires a mandatory "Gate 3 Pass" before proceeding to Phase 4.
**警告**：此階段必須通過「Gate 3 檢核」才能進入 Phase 4。

### Gate 3 Requirements:

1.  **Automated Check (自動檢查)**:
    - **Collisions**: No duplicate mappings for the same ID.
    - **Structure**: All required columns must exist.
2.  **Manual Verification (人工驗證)**:
    - Review `chunk_mapping.csv`.
    - Confirm logical consistency of IDs (e.g., `ko_N_apple` maps to `apple`).
3.  **Sign-off (簽核)**:
    - Create artifact `verified_p3.txt`.

## 🛠 Tools

- `python -m tools.v5.core.extract {lang}`

## 📚 Resources

- [[3_mapping/3_mapping_sop.md]]
- [[3_mapping/resources/checklists.md]]
