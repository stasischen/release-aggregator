# Lingo Release Aggregator Control Tower

## What This Is
A documentation and release orchestration control tower for the Lingo multi-repo ecosystem. It standardizes startup, planning, execution, and closeout behavior across repos, while staging and validating release artifacts for downstream intake.

## Core Value
Cross-repo delivery must stay predictable, auditable, and reversible.

## Requirements

### Validated
- ✓ Central task index and control-tower documentation hub exists — existing
- ✓ Startup and closeout dispatcher protocols exist — existing
- ✓ Release aggregation script with manifest validation exists — existing

### Active
- [ ] Make GSD phase workflow the default operating model for multi-repo work.
- [ ] Add checkable execution evidence for each phase (context, plan, summary, verification).
- [ ] Reduce drift between documented protocol and actual repo operations.

### Out of Scope
- Product feature development in non-aggregator repos — owned by their repo plans.
- Replacing repository-specific pipelines with a monolithic aggregator pipeline — violates ownership boundaries.

## Context
- Repository is process-heavy and code-light; correctness depends on protocol discipline.
- Existing docs already define boundaries, but operational artifacts are split between root files and task docs.
- GSD command definitions are present in `.gemini/commands/gsd/` and `.gemini/get-shit-done/workflows/`.

## Constraints
- **Boundary**: One phase one repo — required for atomic rollback.
- **Evidence**: Session outcomes must be persisted to files, not chat-only memory.
- **Compatibility**: Must preserve current docs navigation and runbook references.

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use `.planning/` as GSD artifact root | Align with GSD workflows and phase files | — Pending |
| Keep root `PROJECT/REQUIREMENTS/ROADMAP/STATE` for human summary | Preserve existing team visibility while bootstrapping | — Pending |
| Start with Phase 1 focused on workflow hardening docs/scripts | Fastest path to verifiable operational improvement | — Pending |

---
*Last updated: 2026-02-17 after re-initialization*
