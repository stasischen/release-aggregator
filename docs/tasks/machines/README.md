# Machine Claims

This directory holds local, gitignored JSON files that identify which machine is working on which task.

## Purpose

- Let each computer self-identify.
- Make current task ownership explicit.
- Avoid two machines working the same main task by accident.

## File Naming

Default file:

- `local.json`

Optional alternate file names are allowed if a machine needs multiple profiles, but `local.json` should be the default so every session knows where to read and write its own claim.

## Recommended JSON Shape

```json
{
  "machine_id": "m5pro",
  "label": "m5pro",
  "host": "ywchen-macbook",
  "repo": "release-aggregator",
  "owner": "ywchen",
  "current_task": "kg-normalize-001B",
  "task_status": "in_progress",
  "updated_at": "2026-04-17T10:30:00+08:00",
  "notes": "Doing bounded normalization batch only."
}
```

## Suggested Fields

- `machine_id`: short stable identifier, e.g. `A`, `B`, `C`
- `label`: human-friendly role, e.g. `Normalization Box`
- `host`: hostname or desktop label
- `repo`: repository name
- `owner`: person or account using the machine
- `current_task`: active task ID
- `task_status`: `in_progress`, `blocked`, `idle`, `done`
- `updated_at`: ISO-8601 timestamp
- `notes`: optional short note about scope or blockers

## Operating Rule

Each computer should have one stable local claim file at `docs/tasks/machines/local.json`.
The file name stays the same; the contents identify the machine.

Before starting work:

1. Write or update `docs/tasks/machines/local.json`.
2. Check the current claim in `docs/tasks/TASK_INDEX.md`.
3. Do not pick up a task already claimed by another machine unless the claim is released.

After changing task scope:

1. Update `docs/tasks/machines/local.json`.
2. Update the shared `docs/tasks/MACHINE_STATUS.md`.
3. If the task needs a durable handoff, update the relevant handoff file.
4. Commit and push the shared status change so other machines can see the new ownership.

## Claim Flow

Recommended sequence:

1. Pick the task.
2. Update `docs/tasks/machines/local.json`.
3. Update `docs/tasks/MACHINE_STATUS.md` with the same claim.
4. Commit and push the shared status update.
5. Start work only after the shared state is visible.

## Release Flow

When you finish or pause a task:

1. Set `docs/tasks/machines/local.json` to `done`, `blocked`, or `idle`.
2. Update `docs/tasks/MACHINE_STATUS.md`.
3. Commit and push the shared status update.
4. If needed, leave a handoff note in `docs/handoffs/`.
