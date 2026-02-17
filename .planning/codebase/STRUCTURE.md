# Codebase Structure Map

## Top-Level Layout
- `docs/`: canonical control-tower knowledge base.
- `scripts/`: executable operational scripts.
- `tools/`: environment layout helpers (e.g., Zellij layout).
- `staging/`: release artifact output area.
- `reports/`, `research/`, `todos/`: auxiliary tracking folders.
- `.agent/` and `.gemini/`: workflow command and protocol configuration.

## Documentation Structure
- `docs/index.md`: top navigation.
- `docs/runbooks/`: actionable runbooks and protocols.
- `docs/tasks/`: active task registry and plans.
- `docs/ops/`: governance and schema files.
- `docs/worklogs/`: date-based session records.
- `docs/archive/universal/`: comparison-only archived docs.

## Script Structure
- `scripts/release.py`: artifact aggregation + manifest validation.
- `scripts/release.sh`: release wrapper.
- `scripts/ops/start_lingo_control_tower.sh`: session launcher.
- `scripts/migrate_universal_docs_to_control_tower.sh`: docs migration utility.

## Planning/State Structure
- Root: `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `PLAN.md`, `STATE.md`.
- GSD-compatible workspace now under `.planning/**`.

## Naming Patterns
- Runbooks use snake_case filenames.
- Task files use task-id naming and archive date prefix conventions.
