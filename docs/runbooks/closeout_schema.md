# Closeout Protocol - Core Schema

## Scope
Use this protocol only when `core-schema` is touched.

## Required Checks
1. Validate all modified schema JSON files are syntactically valid.
2. Run schema validator against required examples (dictionary core/i18n, grammar core/i18n, manifest if changed).
3. If contract docs changed, confirm examples and docs are consistent with schema fields.

## Required Report Fields
- `repo`: core-schema
- `branch`
- `commit_hashes`
- `commands_run`
- `test_results`
- `schema_coverage` (which schemas/examples were validated)
- `breaking_change` (`yes|no`) with rationale
- `pending_decisions`
- `blockers`

## Exit Rule
- Do not mark done if any required example validation fails.
- If breaking change is `yes`, include migration note and affected repos.
