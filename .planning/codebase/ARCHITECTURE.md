# Codebase Architecture Map

## High-Level Pattern
- Control-tower architecture: this repo coordinates process, policy, and release aggregation.
- Separation of concerns:
  - `docs/**` for protocol and decision memory.
  - `scripts/**` for operational execution.
  - Root planning files for current project state.

## Primary Flows
1. Task and protocol discovery via `docs/index.md` and `docs/tasks/TASK_INDEX.md`.
2. Stage execution policy selection (`classic_stage` vs `gsd_phase`).
3. Release aggregation script copies pipeline artifacts into staging.
4. Manifest generated and validated against `core-schema` validator.
5. Closeout routed through runbook dispatcher and worklog append.

## Entry Points
- Human/agent workflow entry: `.agent/workflows/start.md`.
- Operational script entry: `scripts/release.py`.
- Multi-repo layout launcher: `scripts/ops/start_lingo_control_tower.sh`.

## Architecture Characteristics
- Documentation-driven orchestration with thin executable core.
- Explicit repo boundary rules reduce cross-repo mutation risk.
- State intentionally persisted in files rather than ephemeral chat context.

## Gaps
- No centralized CI in this repo validating docs links or protocol consistency.
- Release script hardcodes some metadata values (version/schema/pipeline version).
