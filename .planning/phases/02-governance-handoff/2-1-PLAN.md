# Plan 2-1: Repo-Scoped Decomposition Guardrails

## Goal
Make GOV-02 executable by forcing cross-repo requests to be decomposed into repo-scoped phase units before execution.

## Steps
1. Update startup/phase workflow docs to require a pre-execution decomposition checklist.
2. Add an explicit output contract for `gsd_phase`: phase id, target repo, dependency predecessor, and boundary statement.
3. Add blocker rule: if one phase needs edits in more than one repo, stop and split into separate phases.

## Done When
- Active runbooks include a mandatory decomposition checklist.
- Startup output template includes repo-scoped wave/dependency fields.
- Blocker handling for decomposition violations is documented.
