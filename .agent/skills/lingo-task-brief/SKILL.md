---
name: lingo-task-brief
description: Use when creating, updating, or reviewing a Lingourmet task brief, implementation packet, model routing note, or task directory under release-aggregator/docs/tasks.
---

# Lingo Task Brief

Use this skill when a task needs to become a durable repo artifact instead of staying in chat.

## Load First

1. `AGENTS.md`
2. `docs/runbooks/multi_model_task_orchestration.md`
3. `docs/tasks/TASK_INDEX.md`
4. `docs/tasks/templates/TASK_BRIEF_TEMPLATE.md`
5. `docs/tasks/templates/CODEX_TASK_TEMPLATE.md` if implementation will follow

## Workflow

1. Create or update the task brief using `TASK_BRIEF_TEMPLATE.md`.
2. Fill `Model Routing` with `flash`, `flash -> pro`, or `pro`.
3. Keep the target repo and scope explicit.
4. Add acceptance criteria before implementation starts.
5. If the task is active or changes status, update `docs/tasks/TASK_INDEX.md`.

## Routing Defaults

- `flash`: drafting, scan, inventory, bulk text cleanup.
- `flash -> pro`: first-pass inventory followed by decision or review.
- `pro`: root-cause analysis, architecture review, release risk, schema/API/data-flow decisions.

## Output

Return the task path, model routing, scope, acceptance criteria, and any missing blockers.

