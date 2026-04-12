# Implementation Plan: Incremental Video Atomization

## Goal
Atomize (segment) all 26 pending YouTube videos in `content-ko` into 100% reversible atoms. To prevent Gemini hallucinations, the process will be broken down into manageable batches (max 20 turns per session).

## User Review Required

> [!IMPORTANT]
> **Hallucination Guardrail**: We will strictly limit each Gemini session to **20 turns**. Large videos will be processed in multiple increments and merged later.

## Proposed Changes

### [Component Name] content-ko

#### [MODIFY] [build_gemini_video_atom_bundle.py](file:///d:/Githubs/lingo/content-ko/scripts/ops/build_gemini_video_atom_bundle.py)
- Support `--start-turn` and `--end-turn` arguments to slice a specific range of turns from the source JSON.
- Adjust the `PROMPT.txt` and output naming to reflect the range (e.g., `videoID_atoms_001_050.json`).

#### [NEW] [consolidate_video_atoms.py](file:///d:/Githubs/lingo/content-ko/scripts/ops/consolidate_video_atoms.py)
- A tool to merge multiple partial atom JSONs into a single canonical `videoID_atoms.json`.
- It will verify the sequence of turn IDs to ensure no gaps or overlaps.

### [Component Name] release-aggregator

#### [NEW] [VIDEO_ATOMIZATION_INCREMENTAL_PLAN.md](file:///d:/Githubs/lingo/release-aggregator/docs/tasks/VIDEO_ATOMIZATION_INCREMENTAL_PLAN.md)
- Define the roadmap for processing 26 videos.

## Execution Workflow (Step-by-Step)

1. **Refactor Tooling**: Update `build_gemini_video_atom_bundle.py`- Results are moved to `content/core/video_atoms/`
- Intermediate runs are gitignored
2. **Queue Setup**: Run `build_gemini_video_atom_queue.py --limit 5` to focus on the top 5 videos.
3. **Incremental Processing**:
- [x] **Video 1**: `9lOJxJBRj1I` (Ice Cream Shop) - 79 turns
    - [x] Chunk 1: 1-20
    - [x] Chunk 2: 21-40
    - [x] Chunk 3: 41-60
    - [x] Chunk 4: 61-79
    - [x] Consolidated and Verified.
- [x] **Video 2**: `IGEj-oDKyw8` (Convenience Store) - 104 turns
    - [x] Chunks 1-6 completed and verified.
    - [x] Consolidated and Verified.
- [ ] **Video 3**: `Q7_UmOUi1XE` (Lunar New Year Soup) - 57 turns
    - [ ] Pending processing.
     - Store output as `runs/video_atomization/checkpoints/{videoId}_atoms_{start}_{end}.json`.
     - Verify each chunk individually with `verify_video_atoms.py`.
4. **Final Consolidation**: Use `consolidate_video_atoms.py` to produce the final `_atoms.json`.
5. **Final QA Gate**: Run `verify_video_atoms.py` on the consolidated file.

## Open Questions

- **Batch Size**: Is 50 turns per call acceptable, or should we go even smaller (e.g., 25) for high-complexity vlogs?
- **Workflow**: For 26 videos, this will take multiple sessions. Do you want me to prioritize specific videos (e.g., v5 vlogs)?

## Verification Plan

### Automated Tests
- `python3 scripts/ops/verify_video_atoms.py <consolidated_file> --source-file <source_file>`
- Check for 100% pass on alignment and reversibility.

### Manual Verification
- Random sampling of 5-10 turns to check POS tagging accuracy and lemma standardization.
