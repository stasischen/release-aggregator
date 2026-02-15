# Asset Tracking Policy and Migration Tasks

Date: 2026-02-14  
Owner: Architecture / Release  
Scope: `lingo-frontend-web`, `content-pipeline`, `release-aggregator`

## Decision

Current policy: **A-mode (tracked assets)**.

Reason:
1. Pipeline and intake workflows are still stabilizing.
2. B-mode (untracked assets) adds extra operational risk in CI and local dev.
3. We prioritize deterministic test execution first.

## Definitions

### A-mode (Tracked Assets)

1. `assets/content/**` remains tracked in `lingo-frontend-web`.
2. CI can run tests directly after checkout.
3. Sync scripts may update assets, but final artifacts are committed.

### B-mode (Untracked Assets)

1. `assets/content/**` is ignored in git.
2. CI/local must fetch/sync artifacts before running tests.
3. Requires reliable artifact availability and version pinning.

## Migration Rule

Do not switch to B-mode until all entry criteria are green.

## Entry Criteria for B-mode

All must pass for 2 consecutive release cycles:

1. `release-aggregator` publish success rate = 100%.
2. `content-pipeline` schema validation pass rate = 100%.
3. Frontend intake sync success in CI = 100%.
4. Rollback runbook tested at least once.
5. Artifact version pin + provenance manifest verified in CI.

## Task Plan (Gemini Execution)

### Task ASSET-POLICY-01: Lock A-mode and Remove Ambiguous Ignores

Repo: `lingo-frontend-web`

Actions:
1. Update `.gitignore` to avoid broad/ambiguous content rules.
2. Keep tracked assets behavior explicit in docs.
3. Add `docs/operations/asset_tracking_policy.md` with A-mode rationale.

Acceptance:
1. Existing tracked `assets/content/**` remains intact.
2. `.gitignore` has no contradictory content rules.

### Task ASSET-POLICY-02: Add B-mode Readiness Checks (No Switch Yet)

Repo: `lingo-frontend-web`

Actions:
1. Add CI preflight step to verify artifact version metadata exists.
2. Add non-blocking dry-run step for `scripts/sync_content.sh`.
3. Emit clear logs for sync source/version.

Acceptance:
1. CI still passes in A-mode.
2. Dry-run output is visible in CI logs.

### Task ASSET-POLICY-03: Define B-mode Cutover Runbook

Repo: `release-aggregator`

Actions:
1. Add `docs/runbooks/frontend_asset_untrack_cutover.md`.
2. Include cutover, rollback, and verification commands.
3. Include required approvals and rollback trigger conditions.

Acceptance:
1. Runbook covers full path: prepare -> cutover -> verify -> rollback.

### Task ASSET-POLICY-04: Create Status Board for Criteria

Repo: `release-aggregator`

Actions:
1. Add `docs/ops/asset_mode_readiness.md`.
2. Track each B-mode entry criterion with status/date/evidence.

Acceptance:
1. Team can decide go/no-go from one page.

## Out of Scope (Now)

1. Do not untrack `assets/content/**` yet.
2. Do not remove currently tracked artifact files.
3. Do not change frontend tests to depend on remote fetch only.

## Mandatory Report Format

Gemini must return:

1. `task_id`
2. `commit_hash`
3. `changed_files`
4. `commands_run`
5. `test_results`
6. `blockers`
7. `handoff_file_path`

## Ready-to-Use Prompt

```text
請讀取 docs/planning/ASSET_TRACKING_POLICY_AND_MIGRATION_TASKS.md。
先執行 ASSET-POLICY-01（A-mode lock），不要切換到 B-mode。
完成後用固定格式回報：
task_id / commit_hash / changed_files / commands_run / test_results / blockers / handoff_file_path
```
