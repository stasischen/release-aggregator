# Closeout Protocol - Release Aggregator

## Scope
Use this protocol only when `release-aggregator` is touched.

## Required Checks
1. Run release/manifest generation command if logic changed.
2. Verify manifest path and provenance fields.
3. Confirm docs links and task-board status updates if documentation changed.

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
