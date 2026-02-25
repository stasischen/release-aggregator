# GSD Task: Content-Ko Structure Normalization

**Status**: Defined
**Owner**: Content-Ko Team
**Priority**: High

## Context
The current `content-ko` structure has redundant nesting (`content/source/ko`) and the `.codex_review` workflow is not fully integrated into the standard data flow. This task aims to normalize the directory structure and formalize the review pipeline.

## Objectives
1.  **Normalize Directory Structure**: Move items to standard `content/` and `data/` paths.
2.  **Integrate Review Workflow**: Move `.codex_review` artifacts to permanent locations.
3.  **Update Toolchain**: Ensure all scripts in `scripts/ops` reference the new paths.

## Execution Plan (Phase 1)

### Step 1: Migration (Git Operations)
- [ ] Move `content/source/ko/core` -> `content/core`
- [ ] Move `content/source/ko/overrides` -> `content/overrides`
- [ ] Move `.codex_review/gold_standards` -> `content/gold_standards`
- [ ] Move `content/source/ko/i18n` -> `content/mappings` (or verify content)
- [ ] Move `.codex_review/ko_gemini_review_api_v1` -> `data/review_history`

### Step 2: Script Updates
- [ ] Update `scripts/ops/stage2_executor.py`: Point to `content/overrides`
- [ ] Update `scripts/ops/build_lesson_gold.py`: Point to `content/gold_standards`
- [ ] Update `scripts/ops/gsd_window_runner.py`: Update report paths
- [ ] Scan and fix imports in `scripts/ops/*`

### Step 3: Validation
- [ ] Run `stage2_executor.py` -> Verify candidates generated
- [ ] Run `build_lesson_gold.py` (A1-04) -> Verify Gold comparison works
- [ ] Run `gsd_window_runner.py` (Window 1) -> Verify full regression suite pass

## Deliverables
- Clean `content/` root with no `source/ko` nesting.
- Functional pipeline with 0 regression.
