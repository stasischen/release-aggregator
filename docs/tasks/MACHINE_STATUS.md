# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | kg-ui-019 | in_progress | 2026-04-17 | Frontend priority: dictionary grammar detail overlay and link UI |
| home | home | CMOD-001~010 | in_progress | 2026-04-17 | Course module composition architecture work |
| 888 | 888 | yt-video-atomization | in_progress | 2026-04-17 | YouTube video atomization |
| gamer | gamer | Ingestion Batch (L127-131) | done | 2026-04-17 | Systematic ingestion of Beginner Grammar L127-131 |
| mac | mac | idle | idle | 2026-04-17 | Docs/content-only machine; keep frontend tasks off this machine |

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
