---
name: lingo-content-batch-handoff
description: Use when handing off Lingourmet content batches, lesson/video/grammar migration work, atomization batches, or multi-session content production tasks.
---

# Lingo Content Batch Handoff

Use this skill for content work that spans multiple sessions, machines, or model passes.

## Load First

1. `AGENTS.md`
2. `docs/runbooks/multi_model_task_orchestration.md`
3. `docs/handoffs/HANDOFF_SUMMARY_TEMPLATE.md`
4. `docs/tasks/TASK_INDEX.md`
5. The relevant task plan or batch artifact

## Handoff Requirements

Record:

- exact batch scope
- completed units, rows, lessons, videos, or files
- current decisions and rejected options
- validation commands and results
- DeepSeek routing for next pass
- what not to redo
- exact next action

## Model Routing

- Use `flash` for bulk extraction, translation drafts, inventory, and summaries.
- Use `pro` for final content judgment, schema-risk decisions, unresolved ambiguity, or release-affecting recommendations.
- Use `flash -> pro` when a batch starts with inventory and ends with a recommendation.

## Output

Create or update a handoff under `docs/handoffs/` or the task directory, then summarize changed files and next action.

