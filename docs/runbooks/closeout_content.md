# Closeout Protocol - Content

## Scope
Use this protocol only when `content-ko` is touched.

## Required Checks
1. Run token/mapping steps used in this session.
2. Run validation script(s) and capture unresolved/conflict counts.
3. If dictionary changed, report core/i18n coverage and missing fields.

## Required Report Fields
- `repo`: content-ko
- `branch`
- `commit_hashes`
- `commands_run`
- `test_results`
- `mapping_summary` (accepted/conflicts/unresolved ratio)
- `dictionary_summary` (core/i18n coverage)
- `pending_decisions`
- `blockers`

## Exit Rule
- Do not claim complete if unresolved ratio or schema checks fail policy threshold.
