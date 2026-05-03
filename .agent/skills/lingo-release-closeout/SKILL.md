---
name: lingo-release-closeout
description: Use when closing a Lingourmet session, milestone, phase, or cross-repo task; writing handoff summaries, worklogs, final validation notes, or next-phase prompts.
---

# Lingo Release Closeout

Use this skill whenever work is ending and must be made durable for the next thread or machine.

## Load First

1. `AGENTS.md`
2. `docs/runbooks/gemini_closeout_protocol.md`
3. `docs/handoffs/HANDOFF_SUMMARY_TEMPLATE.md`
4. `docs/tasks/TASK_INDEX.md`
5. Relevant task brief, plan, or state files

## Required Closeout Checks

1. Confirm changed files and touched repos.
2. Confirm validation commands run, or record why not.
3. Update task state when status changed.
4. Write or update the handoff summary with DeepSeek model routing.
5. Include the three closeout outputs required by the closeout protocol:
   - `commit_reminder`
   - `next_phase_prompt`
   - `handoff_summary`

## Output

Return commits, changed repos, validation, blockers, next actions, and the handoff path.

Do not claim completion without commit hashes when the protocol requires committed work.

