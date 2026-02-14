# Closeout Protocol - Frontend

## Scope
Use this protocol only when `lingo-frontend-web` is touched.

## Required Checks
1. Run `flutter analyze` in frontend repo.
2. Run impacted tests (minimum one integration path if content intake changed).
3. If content intake changed, run sync command and verify no broken asset path.

## Required Report Fields
- `repo`: lingo-frontend-web
- `branch`
- `commit_hashes`
- `commands_run`
- `test_results`
- `asset_intake_status`
- `pending_decisions`
- `blockers`

## Exit Rule
- Do not mark done if analyze/test fails.
