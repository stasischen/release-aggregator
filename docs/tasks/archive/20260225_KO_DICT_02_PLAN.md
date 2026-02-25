# KO-DICT-02 Implementation Plan: Active Lemma zh_tw Filling

## Goal
Fill the **zh_tw** (Traditional Chinese) translations for all Korean lemmas currently used in active courses.

> [!IMPORTANT]
> **Constraint**: Do NOT translate the entire TOPIK 3000 base. Only translate lemmas (Atoms) that are extracted from the actual course dialogue.

## Proposed Changes

### content-ko

#### [NEW] [zh_tw dictionary structure]
- Create `content/source/ko/i18n/zh_tw/` directory.
- Files should match `base/` structure: `mapping_nouns.json`, `mapping_verbs.json`, etc.

#### Extraction Process
1.  **Extract Active Atoms**:
    - Run `stage2_executor.py`.
    - Read `artifacts/stage2/handoff.stage-02.json` or `data/staging/mapping_accepted.jsonl`.
    - Collect all `final_atom_id` values (e.g., `ko:n:친구`, `ko:v:가다`).
2.  **Generate Skeleton**:
    - Create a script `scripts/ops/generate_i18n_skeleton.py` to:
        - Input: List of active Atom IDs.
        - Output: JSON templates in `zh_tw/` containing only those IDs.
3.  **Translate**:
    - Fill the `zh_tw` gloss for the identified IDs.

## Verification Plan

### Automated Tests
- Run `stage2_executor.py`.
- Verify `handoff.stage-02.json` contains non-null `zh_tw` values for all course tokens.
- Add a CI gate (e.g., `scripts/qa/check_i18n_coverage.py`) that fails if active tokens are missing translations.

### Manual Verification
- View updated lessons in LLO Viewer.
- Confirm dictionary popups show Traditional Chinese definitions.
