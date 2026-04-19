# Machine Status

This file is the shared, tracked summary of which machine is currently working on which task.

Each machine should maintain its own local, gitignored claim JSON under `docs/tasks/machines/*.json`, then reflect the active state here for cross-machine visibility.

## Current Template

| Machine ID | Label | Current Task | Status | Updated At | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| m5pro | m5pro | FRONTEND_CONTENT_V2_REALIGNMENT | in_progress | 2026-04-19 | Frontend contract alignment & adapter refactor |
| home | home | MDICT_KO_ZH_DICTIONARY_INGEST | pending_plan | 2026-04-19 | MDict 韓中字典清洗與導入；建 skill 後 pilot |
| 888 | 888 | YT_ATOM_TO_V2_CONTENT | pending_plan | 2026-04-19 | YT atom 轉 V2 content 格式；建 skill 後 pilot |
| gamer | gamer | SENTENCE_BANK_ATOMIZATION | in_progress | 2026-04-19 | 批次 sentence bank atom 化導入中 |
| mac | mac | SCHEMA_DOCS_AUDIT | pending_plan | 2026-04-19 | 盤點最新 schema 與文件同步狀態 |

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
