# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | KG-UI-019 | in_progress | 2026-04-17 | Frontend dictionary-to-grammar deep linking UI |
| home | home | none | idle | 2026-04-17 | Batch 1.1 Ingestion completed (50 sentences, 5 KIs). |
| 888 | 888 | yt-video-atomization (goPwS4aL4Lk) | done | 2026-04-18 | v_001 - v_439 processed and promoted. |
| gamer | gamer | Ingestion Batch (L137-142) - FINAL | done | 2026-04-17 | Beginner series officially complete. |
| mac | mac | LEARNING_LIBRARY_CONTENTKO_MIGRATION | done | 2026-04-18 | Frontend intake aligned to core/i18n packs |

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
