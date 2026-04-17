# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | MODULAR_VIEWER_REFACTOR | in_progress | 2026-04-17 | Step 3 (Renderer Split) done. Ready for Step 4 (i18n-first cleanup) |
| home | home | idle | idle | 2026-04-17 | Completed CMOD-012 |
| 888 | 888 | CMOD-013 | done | 2026-04-17 | Sentence Practice Action Contract completed. |
| gamer | gamer | Ingestion Batch (L137-142) - FINAL | done | 2026-04-17 | Beginner series officially complete. |
| mac | mac | repo-org / docs maintenance | in_progress | 2026-04-17 | Repo organization, doc cleanup, and spec stabilization |

## Usage Rule

- Update the local JSON first.
- Then update this shared summary.
- Commit and push the summary change so other machines can see the new ownership.
- If a task is released, set the machine row back to `idle`.
- Keep the summary short and current; do not use it as a long log.

## Recommended Claim Sequence

1. Decide the task.
2. Write the machine-local JSON claim.
3. Update this shared summary in the same commit if possible.
4. Push the commit before starting substantive work.

This keeps the shared status consistent across machines without relying on oral coordination.
