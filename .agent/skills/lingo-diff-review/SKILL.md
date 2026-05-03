---
name: lingo-diff-review
description: Use when reviewing a Lingourmet diff, implementation packet, task completion candidate, or PR-like change against a task brief and acceptance criteria.
---

# Lingo Diff Review

Use this skill for review-first work. Findings are the primary output.

## Load First

1. `AGENTS.md`
2. `docs/runbooks/multi_model_task_orchestration.md`
3. `docs/tasks/templates/GPT_DIFF_REVIEW_TEMPLATE.md`
4. The relevant `TASK_BRIEF.md`, plan, or task file
5. The current diff or commit range

## Review Focus

- Scope creep or unrelated edits
- Architecture, schema, release path, public API, or data-flow regressions
- Missing tests or weak validation
- Mismatch with task brief acceptance criteria
- Unsafe assumptions or unrecorded tradeoffs

## Output Contract

Report findings first, ordered by severity. If there are no findings, say so and list residual risks or testing gaps.

Each finding should include:

- severity
- file path and tight line reference
- issue
- required fix

After findings, include only concise open questions and next fix instructions.

