# Gemini Closeout Protocol (Dispatcher)

## Goal
When user says "收工", Gemini selects only the protocol(s) that match touched repositories.

## Selection Rules
- If touched repo includes `lingo-frontend-web`: include [closeout_frontend.md](closeout_frontend.md)
- If touched repo includes `content-ko`: include [closeout_content.md](closeout_content.md)
- If touched repo includes `content-pipeline`: include [closeout_pipeline.md](closeout_pipeline.md)
- If touched repo includes `release-aggregator`: include [closeout_release.md](closeout_release.md)
- If touched repo includes `core-schema`: include [closeout_schema.md](closeout_schema.md)

## Do Not Include Unrelated Protocols
- Backend/content work must not run frontend-only checks.
- Frontend-only work must not run pipeline/content gates.

## Mandatory Workflow
1. Detect touched repos from commands/changed files.
2. Select matching protocol set.
3. Execute checks per selected protocol.
4. Emit one merged closeout report.
5. Append daily worklog at `docs/worklogs/YYYY-MM-DD.md`.

## Merged Closeout Report Format
- `task_id`
- `touched_repos`
- `selected_protocols`
- `branches`
- `commit_hashes`
- `commands_run`
- `test_results`
- `artifacts_generated`
- `pending_decisions`
- `blockers`
- `next_actions`

## Output Rules
- Never claim completion without command evidence.
- If work is undecided, write it to control-tower daily worklog only.
- Do not write unrelated repo changelog entries.
