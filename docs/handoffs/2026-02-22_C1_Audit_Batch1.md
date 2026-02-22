# Handoff - 2026-02-22 - Wave-3-C1-Audit Batch 1

## Context
- **Task**: [KO-INGEST-01] V5 Pipeline Ingestion / Wave-3-C1-Audit.
- **Goal**: Perform atomic audit and POS standardization for C1 (Cultural Critics) Korean content.
- **Current Position**: Completed Batch 1 (C1-01 to C1-05).

## Accomplishments
- **Audit Completion**: C1-01 to C1-05 are fully audited and synchronized to `content/gold_standards/dialogue/C1/`.
- **Commit Hash**: `014812e` (content-ko).
- **Tooling Enhancement**: 
    - Created/Refined `d:\Githubs\lingo\content-ko\scripts\review\fix_c1_patterns.py`.
    - Integrated academic Hanja/Copula splitting rules into the heuristic flow.
    - Specifically handled: `-이라는`, `-이더군요`, `-었었-`, and noun+particle splits tailored for high-level Hanja.
- **State Updates**:
    - Updated `d:\Githubs\lingo\content-ko\STATE.md`.
    - Updated `d:\Githubs\lingo\release-aggregator\docs\tasks\KO_B2_C1_OPTIMIZATION_TASKS.json`.

## Infrastructure
- **Script**: `python scripts/review/orchestrator.py` (Main driver).
- **Helper**: `python scripts/review/fix_c1_patterns.py` (C1 Specific Heuristics).
- **Repo**: `content-ko` (Primary workspace).

## Remaining
- **Next Batch**: C1-06 to C1-10.
- **Protocol**:
    1. Run `python scripts/review/orchestrator.py draft --lesson C1-0X` (06-10).
    2. Apply C1 patterns: `python scripts/review/fix_c1_patterns.py data/reviews/runs/C1-0X/surgery_C1-0X.json`.
    3. Manual Review of `surgery_C1-0X.json`.
    4. Apply: `python scripts/review/orchestrator.py apply --lesson C1-0X`.
    5. Sync to `content/gold_standards/dialogue/C1/`.

## Boundary Rules / Notes
- **Hanja Sensitivity**: Monitor C1 Hanja words mistagged as nouns when they should be `ko:v` or `ko:adj` (e.g., `동감하다`).
- **Copula Decomposition**: Ensure `-이다` is always separated from the noun and ending.
