# [COMPLETED] Implementation Plan - Video Atomization: Daily Routines (eF65dUUDcEQ)

> [!NOTE]
> **Completion Date**: 2026-04-19
> **Status**: Full video (220 turns) atomized, validated, and promoted to production.

This plan outlines the continuation of the V5 morphological atomization for the video **"Talking About Daily Routines" (eF65dUUDcEQ)**. The video has 220 turns total, with turns v_001-v_063 already completed and promoted.

## User Review Required

> [!IMPORTANT]
> **Task Handover**: Machine 888 is transitioning from `goPwS4aL4Lk` to `eF65dUUDcEQ`.
> **Strategy**: We will continue using the **Small Chunk Workflow** (approx. 20-25 turns per batch) to ensure high-precision Level 3 matching and POS normalization.

## Proposed Changes

### [content-ko](file:///f:/Githubs/lingo/content-ko)

#### [MODIFY] [local.json](file:///f:/Githubs/lingo/release-aggregator/docs/tasks/machines/local.json)
- Update machine claim to video `eF65dUUDcEQ` and start from batch `v_064_v_085`.

#### [NEW] [checkpoints/eF65dUUDcEQ_atoms_064_085.json](file:///f:/Githubs/lingo/content-ko/runs/video_atomization/checkpoints/eF65dUUDcEQ_atoms_064_085.json)
- Generate the next batch of V5 atomized data.

#### [MODIFY] [eF65dUUDcEQ_atoms.json](file:///f:/Githubs/lingo/content-ko/content/core/video_atoms/eF65dUUDcEQ_atoms.json)
- Append and consolidate the new validated batches into the master artifact.

---

## Execution Plan

1. **Machine Claim**: Update `release-aggregator/docs/tasks/machines/local.json` and `MACHINE_STATUS.md`.
2. **Chunk Generation (Batch 1: v_064 - v_085)**:
   - Perform Level 3 canonical decomposition.
   - Apply strict V5 POS tagging (e.g., auxiliary verbs -> `vx`, honorifics mapping).
   - Ensure 100% surface alignment with the source text.
3. **Validation**:
   - Run `v5_standardize_video_atoms.py` on the batch.
   - Verify alignment using `validate_video_atoms.py`.
   - Pass the V5 QA gate (`qa_v5_gate.py`).
4. **Promotion**:
   - Update `pending_queue.json` status.
   - Consolidate into the master JSON in `content/core/video_atoms/`.

## Open Questions

- None at this stage.

## Verification Plan

### Automated Tests
- `python scripts/ops/validate_video_atoms.py --video eF65dUUDcEQ`
- `python scripts/ops/qa_v5_gate.py --video eF65dUUDcEQ --dry-run`

### Manual Verification
- Visual check of the generated JSON for atom-to-eojeol mapping accuracy.
