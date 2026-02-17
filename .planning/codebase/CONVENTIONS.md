# Codebase Conventions Map

## Process Conventions
- Startup must read `docs/tasks/TASK_INDEX.md` first.
- Execution mode must be explicit: `classic_stage` or `gsd_phase`.
- One phase should map to one repo for atomicity and rollback clarity.
- Worklogs are centralized under `docs/worklogs/YYYY-MM-DD.md`.

## Documentation Conventions
- Active protocols live only in `docs/**`.
- Archive docs are read-only and cannot be used as current execution source.
- Task plans and task JSON stay under `docs/tasks/` with index synchronization.

## Git/Change Conventions
- Prefer atomic commit units aligned to task or phase boundaries.
- Avoid cross-repo edits unless explicitly scoped.
- Preserve evidence-oriented closeout fields (test results, pending decisions).

## Script Conventions
- Shell scripts use `set -e` or `set -euo pipefail`.
- Python script keeps functions small and explicit (hashing, validation, release orchestration).
- CLI args are explicit and required for release inputs.

## Practical Enforcement Level
- Most conventions are documented and manually enforced.
- Automated checks for convention drift are limited in current state.
