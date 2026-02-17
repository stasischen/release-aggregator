# Codebase Integrations Map

## Upstream and Downstream Repos
- Upstream artifact producer: `content-pipeline` (dist artifacts consumed by release script).
- Contract authority: `core-schema` (manifest schema + validator path).
- Downstream consumer: `lingo-frontend-web` (intake from release staging output).
- Additional ecosystem source: `content-ko`, `lllo` (described in workflow docs).

## Script-Level Integrations
- `scripts/release.py` invokes external validator:
  - `core-schema/validators/validate.py`
  - `core-schema/schemas/manifest.schema.json`
- `scripts/ops/start_lingo_control_tower.sh` integrates with local Zellij installation and layout file.

## Documentation and Governance Integrations
- `docs/workflow_map.md` defines cross-repo phase handoffs.
- `docs/owners.md` defines ownership boundaries and escalation split.
- `docs/ops/stage_contract_matrix_ko.md` links stage outputs across repositories.

## File Contract Integrations
- JSON handoff schema in `docs/ops/handoff_stage.schema.json` used by stage protocols.
- Task registry format via `docs/tasks/TASK_INDEX.md` + task JSON files.

## Risks
- Integration paths are documented strongly, but automation enforcement is light.
- `scripts/release.sh` currently delegates directly to Python without argument passthrough.
- Contract validation depends on external checkout path correctness for `core-schema`.
