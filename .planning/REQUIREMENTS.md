# Requirements: Release Aggregator GSD Re-Initialization

**Defined:** 2026-02-17
**Core Value:** Cross-repo delivery must stay predictable, auditable, and reversible.

## v1 Requirements

### Workflow
- [ ] **WF-01**: Operator can run a documented sequence: map-codebase -> new-project -> discuss -> plan -> execute -> verify.
- [ ] **WF-02**: Every phase has persisted artifacts (`CONTEXT`, `PLAN`, `SUMMARY`, `VERIFICATION`, optional `UAT`).
- [ ] **WF-03**: Execution mode (`classic_stage` or `gsd_phase`) is explicit in planning state.

### Governance
- [ ] **GOV-01**: Active protocols are sourced only from `docs/**` (archive read-only).
- [ ] **GOV-02**: Cross-repo tasks are decomposed into repo-scoped phases.
- [ ] **GOV-03**: Session closeout writes to `docs/worklogs/YYYY-MM-DD.md`.

### Release Operations
- [ ] **REL-01**: Release aggregation can stage JSON artifacts and generate manifest.
- [ ] **REL-02**: Manifest validates against `core-schema` validator.
- [ ] **REL-03**: Release command interface is documented and runnable with required inputs.

## v2 Requirements

### Automation
- **AUTO-01**: Add CI checks for docs links and required protocol fields.
- **AUTO-02**: Add fixture-based tests for `scripts/release.py`.
- **AUTO-03**: Produce weekly dashboard summary from task/worklog data.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Implementing downstream frontend/content features | Out of release-aggregator ownership scope |
| Full replacement of per-repo runbooks | Violates local repo autonomy |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| WF-01 | Phase 1 | In Progress |
| WF-02 | Phase 1 | In Progress |
| WF-03 | Phase 1 | In Progress |
| GOV-01 | Phase 1 | In Progress |
| GOV-02 | Phase 2 | Verified in Phase 2 |
| GOV-03 | Phase 2 | Verified in Phase 2 |
| REL-01 | Phase 3 | Pending |
| REL-02 | Phase 3 | Pending |
| REL-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 9 total
- Mapped to phases: 9
- Unmapped: 0

---
*Requirements defined: 2026-02-17*
*Last updated: 2026-02-17 after Phase 2 execution*
