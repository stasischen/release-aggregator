# Closeout Protocol - Pipeline

## Scope
Use this protocol only when `content-pipeline` is touched.

## Required Checks
1. Run build script.
2. Run smoke test.
3. If QA gates changed, run one negative sample to confirm fail-fast behavior.

## Required Report Fields
- `repo`: content-pipeline
- `branch`
- `commit_hashes`
- `commands_run`
- `test_results`
- `qa_gate_results`
- `artifacts_generated`
- `pending_decisions`
- `blockers`

## Exit Rule
- Build + smoke must pass for completion claim.
