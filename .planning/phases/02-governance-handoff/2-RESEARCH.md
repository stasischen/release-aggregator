# Phase 2 Research

## Objective
Define executable governance work for GOV-02 and GOV-03 using active protocol docs only, without cross-repo edits.

## Findings
1. `docs/runbooks/gsd_multi_repo_workflow.md` already states one-phase-one-repo and cross-repo decomposition, but lacks an explicit pre-execution checklist artifact that operators must fill before `execute-phase`.
2. `docs/runbooks/gemini_startup_protocol.md` includes mode selection and worklog rule, but the startup output template does not force decomposition proof (repo-scoped phase list / dependency order).
3. `docs/runbooks/gemini_closeout_protocol.md` strongly defines worklog target and anti-overwrite behavior, but governance consistency depends on operators manually remembering closeout dispatch and state-sync requirements.
4. `docs/ops/worklog_and_directory_governance.md` defines canonical daily log fields, while closeout protocol's sample format omits `Blockers` in one section; this can weaken GOV-03 evidence consistency.
5. `.planning/STATE.md` and `.planning/REQUIREMENTS.md` still mark GOV-02/GOV-03 as pending, so Phase 2 needs a doc hardening wave plus a verification wave to move requirement status forward.

## Targeted Gaps
- Missing mandatory decomposition template for cross-repo requests before execution.
- Missing uniform closeout evidence contract spanning runbook + governance policy + planning state.
- Missing phase-level verification artifact plan for GOV-02/GOV-03 completion criteria.

## Implications for Plan
- Wave 1: Codify decomposition/handoff guardrails in active runbooks used at startup and execution.
- Wave 2: Align closeout/worklog protocol fields and add explicit state-sync checks.
- Wave 3: Verify via phase artifacts and update requirements/state traceability.

## Constraints Confirmed
- Only modify `release-aggregator` in this phase.
- `docs/**` is the only active protocol source.
- `docs/archive/**` can be referenced only for comparison, not execution.
