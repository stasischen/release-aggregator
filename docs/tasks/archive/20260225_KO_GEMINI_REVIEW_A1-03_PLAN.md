# KO Segmentation Review: Lesson A1-03 Implementation Plan

This plan outlines the steps to perform a complete automated segmentation review for Lesson A1-03 using the Gemini API review bot.

## Proposed Changes

### [content-ko]

#### [MODIFY] [.codex_review/REMEDIATION_LOG.md](file:///Users/ywchen/Dev/lingo/content-ko/.codex_review/REMEDIATION_LOG.md)
*   Record all rule changes and rationale discovered during Phase 2.

#### [MODIFY] [engine/rules/*.json](file:///Users/ywchen/Dev/lingo/content-ko/engine/rules/)
*   Update individual rule files (e.g., `10_irregulars.json`, `60_particles.json`) based on `RULE_CANDIDATE` findings from the LLM audit.

## Execution Workflow

### Phase 1: Detection
1.  **Cache Setup**: Run `review_bot.py --create-cache` to ensure a valid context cache exists.
2.  **Audit Run**: Run `review_bot.py --process-lesson A1-03`. This will generate `manual_findings_A1-03.jsonl`.

### Phase 2: Systemic Resolution
1.  **Analysis**: Inspect `manual_findings_A1-03.jsonl` for `RULE_CANDIDATE` entries.
2.  **Engine Update**: Modify relevant files in `engine/rules/`.
3.  **Verification**: Run `scripts/ops/stage2_executor.py` for A1-03 to confirm findings are resolved.

### Phase 3: Verification & Gold Baseline
1.  **Gold Baseline**: Run `review_bot.py --process-lesson A1-03 --build-gold`.
2.  **Regression**: Run `stage2_executor.py` for `A1-01`, `A1-02`, and `A1-03`.
3.  **Handoff**: Commit all changes and update the task index.

## Verification Plan

### Automated Tests
*   `python3 scripts/ops/stage2_executor.py --lesson A1-01,A1-02,A1-03`: Ensures zero mismatches across the current and preceding lessons.
*   The review bot itself verifies that the engine output matches the newly created gold standard.

### Manual Verification
*   Spot check `manual_findings_A1-03.jsonl` to ensure all high-confidence errors are addressed.
