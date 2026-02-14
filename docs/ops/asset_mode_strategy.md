# Asset Tracking Policy and Migration Strategy

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

---
**Reference**: [ASSET_TRACKING_POLICY_AND_MIGRATION_TASKS.md](../../../Lingourmet_universal/docs/planning/ASSET_TRACKING_POLICY_AND_MIGRATION_TASKS.md)
