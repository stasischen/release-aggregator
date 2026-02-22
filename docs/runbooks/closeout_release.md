# Closeout Protocol - Release Aggregator

## Scope
Use this protocol only when `release-aggregator` is touched.

## Required Checks
1. Run release/manifest generation command if logic changed.
2. Verify manifest path and provenance fields.
3. Confirm docs links and task-board status updates if documentation changed.
4. Run `python scripts/sync_task_index.py` to ensure all task progress is reflected in the index.

## Required Report Fields
- `repo`: release-aggregator
- `branch`
- `commit_hashes`
- `commands_run`
- `test_results`
- `manifest_status`
- `docs_updates`
- `pending_decisions`
- `blockers`

## Exit Rule
- No completion claim without manifest/doc verification evidence.
