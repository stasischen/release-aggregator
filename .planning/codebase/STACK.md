# Codebase Stack Map

## Runtime and Languages
- Primary scripting: Bash (`scripts/*.sh`, `scripts/ops/*.sh`).
- Primary automation language: Python 3 (`scripts/release.py`).
- Documentation-first orchestration via Markdown (`docs/**`, root planning files).
- JSON assets for schema/contracts and task metadata (`docs/ops/*.json`, `docs/tasks/*.json`).

## Dependency Surface
- Python dependency declared in `requirements.txt`:
  - `jsonschema>=4.0.0`
- External runtime requirements (not vendored):
  - `python3`
  - `zellij` for control tower layout launcher.

## Tooling and Workflow Layer
- GSD/Gemini command scaffolding stored in:
  - `.gemini/commands/gsd/*.toml`
  - `.gemini/get-shit-done/workflows/*.toml`
- Startup/closeout wrappers stored in `.agent/workflows/start.md` and `.agent/workflows/wrap.md`.

## Data and Artifact Paths
- Release output target pattern: `staging/vX.Y.Z/**`.
- Manifest output: `staging/*/global_manifest.json`.
- Operational records and runbooks: `docs/runbooks/**`, `docs/worklogs/**`.

## Observations
- Repo acts as orchestration + documentation control tower, not application runtime.
- No package manager lockfile in this repo; tooling is mostly shell/Python and external CLIs.
