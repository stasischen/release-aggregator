# STATE

## Current Position
- Workspace orchestrator: `release-aggregator`
- Execution model: `classic_stage` + `gsd_phase` (by task type)

## Decisions
- Use aggregator for portfolio planning and task routing.
- Use per-repo state files for implementation memory.
- Require manual new session at phase boundaries.

## Blockers
- None recorded yet.

## Next Checkpoint
- Create repo-level `REQUIREMENTS.md`/`STATE.md`/`PLAN.md` for active repos.
