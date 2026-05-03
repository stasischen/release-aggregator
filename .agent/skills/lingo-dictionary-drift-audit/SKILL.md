---
name: lingo-dictionary-drift-audit
description: Use when auditing Korean dictionary entry drift, homonym/polysemy metadata, Hanja/source metadata, mapping_v2 entry_refs readiness, or dictionary-to-grammar link integrity.
---

# Lingo Dictionary Drift Audit

Use this skill for Korean dictionary drift reviews and metadata readiness checks.

## Load First

1. `AGENTS.md`
2. `docs/tasks/TASK_INDEX.md`
3. `docs/tasks/DICTIONARY_ENTRY_DRIFT_REVIEW_PLAN.md`
4. Relevant dictionary, mapping, grammar, or report files named by the task

## Review Focus

- homonym and polysemy drift
- missing or inconsistent Hanja/source metadata
- stale or invalid `mapping_v2.entry_refs`
- dictionary-to-grammar link integrity
- readiness for downstream frontend or release use

## Model Routing

Default to `pro` for final findings because this work affects dictionary integrity and downstream release behavior.
Use `flash` only for preliminary inventory or bulk candidate extraction.

## Output Contract

Produce findings first, ordered by severity, with evidence and file references. Separate:

- must-fix issues
- safe patch candidates
- needs-human-review cases
- deferred cleanup

Do not rewrite dictionary data unless the task brief explicitly asks for implementation.

