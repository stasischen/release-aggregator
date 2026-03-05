# KO Segmentation Repair Plan (SEG-C1-001)

Repair 25 specific `source_ref` items in the C1 dialogue batch where Korean segmentation is incorrect (e.g., swallowed particles/endings).

## Proposed Changes

### [content-ko]

#### [MODIFY] `content/gold_standards/dialogue/C1/*.jsonl`
- Update `gold_final_atom_id` with canonical atom decomposition.
- Set `review_applied: true`.
- Set `gsd_action: "MANUAL_BATCH_FIX_SEG-C1-001"`.

#### [NEW] `content/core/dictionary/atoms/<POS>/<fs_safe_id>.json` (Optional)
- Create if a required atom is missing from the dictionary.

#### [NEW] `content/i18n/zh_tw/dictionary/<fs_safe_id>.json` (Optional)
- Create Traditional Chinese definition for the new atom.

## Verification Plan

### Automated Tests
- Run `python3 scripts/ko_data_pipeline.py` on the modified files if available.
- Verify `surface` reconstruction matches the original text.

### Manual Verification
- Review the fixed `gold_final_atom_id` against the original sentence in `content/core/dialogue/C1/*.json`.
