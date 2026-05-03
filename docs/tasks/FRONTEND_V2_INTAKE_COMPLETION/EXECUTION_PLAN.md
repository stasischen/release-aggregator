# FRONTEND_V2_INTAKE_COMPLETION Execution Plan

## Objective

Complete frontend intake of `content_v2`-derived study, dictionary, grammar, and learning-library runtime data without binding UI-facing repositories to raw production package layout.

## Work Split

| Order | Slice | Owner | Model Routing | Output | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Data-flow and path-coupling inventory | Codex local | Codex / DeepSeek flash if expanded | `DEEPSEEK_INVENTORY.md` | done |
| 2 | Frontend v2 resolver contract decision | GPT 5.5 | DeepSeek pro optional, GPT final | `GPT_DECISION.md` | next |
| 3 | Study discovery/loading implementation | Codex | Codex, GPT diff review | frontend commit | pending |
| 4 | Dictionary runtime contract completion | Codex | completed first slice; GPT review if widened | frontend commit / notes | partial |
| 5 | Real Korean v2 production validation | Codex | Codex | frontend tests | pending |
| 6 | PRG/frontend artifact handoff verification | Codex + GPT decision | DeepSeek pro / GPT | release-aggregator tests/docs | pending |

## Current Sequence

1. Inventory first.
2. GPT 5.5 decides the minimal resolver/adapter contract.
3. Codex implements only the accepted study resolver slice.
4. GPT 5.5 reviews the diff before broader migration.
5. Codex adds real Korean v2 validation.
6. PRG/frontend handoff is verified only after frontend expected contract is stable.

## Parallel Work Boundaries

Dictionary review thread:

- Owns dictionary truth, entry quality, homonym/polysemy decisions, ID changes, `content-ko/content_v2/inventory/dictionary/**`.
- Must hand off contract changes that affect frontend lookup.
- Must not edit frontend runtime code.

Frontend v2 intake thread:

- Owns frontend adapter/resolver, runtime loading, UI-facing compatibility, and tests.
- Must not rewrite dictionary inventory quality or content source truth.
- May update release-aggregator task docs and frontend code within accepted slices.

PRG/release thread:

- Owns release manifest, `global_manifest.json`, production artifact promotion, and rollback gates.
- Should not define frontend UI data model without GPT 5.5 contract decision.

## Immediate Next Step

Prepare `GPT_DECISION.md` from `DEEPSEEK_INVENTORY.md` and decide:

1. The minimal `FrontendContentContractResolver` shape.
2. Whether study lesson body paths must come only from `manifest.lessons[].path`.
3. Whether `modular_lessons.json` remains as compatibility input or becomes manifest-listed only.
4. Which real Korean v2 fixture should become the stable validation target.

## Do Not Do Yet

- Do not refactor `StudyContentLocator` before GPT accepts the resolver boundary.
- Do not remove legacy fallback loaders in the first implementation slice.
- Do not couple Flutter runtime directly to `content-ko/content_v2` raw inventory paths.
- Do not include Stitch UI/design work in this task.
