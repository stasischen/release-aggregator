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

Do not keep task state only in chat. For persistent work, create or update artifacts
under `docs/tasks/`, `docs/handoffs/`, or `docs/worklogs/`.

## Scope Rule

For implementation tasks, work only inside the repo and file scope stated in the task
brief or implementation packet. Do not expand into sibling repos unless the brief
explicitly approves it.

