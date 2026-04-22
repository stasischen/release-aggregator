# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | STITCH_UI_PROTOTYPING | idle | 2026-04-20 | ULV Core & PatternLab restored |
| home | home | YT_ATOM_TO_V2_CONTENT | pending_plan | 2026-04-21 | Ready for worker pickup from batch handoff |
| 888 | 888 | - | idle | 2026-04-21 | Released from YT_ATOM_TO_V2_CONTENT |
| gamer | gamer | SENTENCE_BANK_ATOMIZATION | in_progress | 2026-04-21 | Batch 06 ingested; Batch 07 readiness complete |
| atg | atg | BATCH_07_INGESTION | idle | 2026-04-21 | Batch 07 ingestion completed. |
| mac | mac | MDICT_KO_ZH_DICTIONARY_INGEST | idle | 2026-04-23 | Switched to dictionary ingest work. |


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
