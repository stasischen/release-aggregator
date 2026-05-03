# AGENTS.md

## Project Role

This repository is the control tower for the Lingourmet / Lingo multi-repo system.
When working from this repo, treat `release-aggregator` as the source of truth for task
planning, cross-repo coordination, handoffs, and release governance.

## Startup Rule

At the start of a new session, read these files before planning or editing:

1. `GEMINI.md`
2. `docs/index.md`
3. `docs/runbooks/agent_reference_order.md`
4. `docs/runbooks/multi_model_task_orchestration.md`
5. `docs/tasks/TASK_INDEX.md`

If the user names a specific task, also read that task's `TASK_BRIEF.md` and latest
`HANDOFF_SUMMARY.md` when present.

## Multi-Model Operating Rule

Use `docs/runbooks/multi_model_task_orchestration.md` as the default workflow for
non-trivial tasks:

- Gemini scans broad repo or cross-repo context.
- DeepSeek drafts inventory, cleanup notes, or bulk analysis.
- GPT 5.5 makes architecture decisions and reviews critical diffs.
- Codex implements narrow scoped changes and runs validation.
- Local Qwen may draft private, low-cost, or bulk text work.

## DeepSeek Default

When Claude Code is routed to DeepSeek in this workspace, default to `deepseek-v4-flash`
for drafting, scanning, and bulk text work. Escalate to `deepseek-v4-pro` for review,
architecture judgment, root-cause analysis, or any task where the output will drive a
release or code change decision.

Do not keep task state only in chat. For persistent work, create or update artifacts
under `docs/tasks/`, `docs/handoffs/`, or `docs/worklogs/`.

## Routine Skills

Use repo-local skills in `.agent/skills/` for repeated workflows:

- `lingo-task-brief`: task brief, task directory, implementation packet, model routing.
- `lingo-diff-review`: diff review against a brief, completion candidate, or PR-like change.
- `lingo-release-closeout`: session closeout, worklog, handoff, next-phase prompt.
- `lingo-content-batch-handoff`: content batch, lesson/video/grammar migration handoff.
- `lingo-dictionary-drift-audit`: Korean dictionary drift and metadata readiness audit.

Create a new skill only when a routine has a clear trigger, repeated steps, stable inputs,
and fixed outputs. Keep general coding behavior in this file or the relevant runbook.

## Coding Guardrails

- Think before editing: state assumptions, uncertainty, tradeoffs, and blockers.
- Prefer simple changes over new abstractions unless the repo already has that pattern.
- Edit only files required by the task; do not opportunistically refactor nearby code.
- Preserve existing style, public APIs, and ownership boundaries unless the brief approves changes.
- Define validation before implementation and report commands run or why they could not run.
- Remove only dead code introduced by the current change; do not delete unrelated legacy code.

## Scope Rule

For implementation tasks, work only inside the repo and file scope stated in the task
brief or implementation packet. Do not expand into sibling repos unless the brief
explicitly approves it.
