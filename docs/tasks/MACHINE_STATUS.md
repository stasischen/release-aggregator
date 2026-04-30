# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | STITCH_UI_PROTOTYPING | idle | 2026-04-20 | ULV Core & PatternLab restored |
| home | home | YT_ATOM_TO_V2_CONTENT | pending_plan | 2026-04-21 | Ready for worker pickup from batch handoff |
| 888 | 888 | - | idle | 2026-04-21 | Released from YT_ATOM_TO_V2_CONTENT |
| gamer | gamer | - | idle | 2026-04-27 | Migration of sentences 001051 to 001100. |
| atg | atg | - | idle | 2026-04-25 | NyCrQ-NZMbg atomization (109 turns) completed and promoted. |
| mac | mac | - | idle | 2026-04-30 | Round 2 re-atomization sweep completed |


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
