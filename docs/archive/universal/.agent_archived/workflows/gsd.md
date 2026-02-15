---
description: Get Shit Done (GSD) Workflow - Context-Driven Development
---

# 🚀 Get Shit Done (GSD) Protocol

This workflow implements the **GSD Framework** in Antigravity. It ensures maximum AI focus by moving state from chat history to persistent Markdown files, allowing for "clean-wipe" context resets without losing progress.

## 🌀 The GSD Cycle

1. **Plan** (`/gsd:plan`): Define what to do.
2. **Execute** (`/gsd:run`): Do it in a fresh context.
3. **Archive** (`/gsd:done`): Log it and clear for the next task.

---

## 🛠️ Phase 1: Planning (`/gsd:plan`)
*Run this in your current (perhaps cluttered) session.*

1. **Read State**:
   - `docs/project/ROADMAP.md` (Big picture)
   - `docs/project/TASK.md` (Detailed history)
2. **Identify Objective**: Confirm with the user what high-level milestone we are hitting.
3. **Draft Plan**: Create/Update `IMPLEMENTATION_PLAN.md`.
4. **Export Context**: Run the exporter to isolate signal from noise.
   ```bash
   python3 scripts/export_gsd_context.py [task_id]
   ```
   - This generates `docs/project/GSD_CONTEXT.md`.
   - **Instruction for the next Agent**: "You are in GSD Execution Mode. Read `docs/project/GSD_CONTEXT.md` immediately. Do NOT scan the entire repo."

---

## ⚡ Phase 2: Execution (`/gsd:run`)
*Call this AFTER refreshing the page or opening a NEW conversation.*

1. **Hydrate Memory**:
   - **ONLY** Read `docs/project/GSD_CONTEXT.md` (The "Clean Context").
   - Do NOT read `AGENT_TASKS.json` or `ROADMAP.md` unless explicitly linked.
2. **Setup Work Environment**:
   - Run necessary diagnostic commands (e.g., `flutter pub get`, `git status`).
3. **Execute**: Start coding the features defined in the plan.
4. **Stay Pure**: Do not chat about unrelated topics. Focus 100% on implementing the plan.

---

## ✅ Phase 3: Completion (`/gsd:done`)
*Run this when the task is finished/tested.*

1. **Verify**: Run tests and linting.
2. **Archive**:
   - Move completed items in `ROADMAP.md` to `Done`.
   - Update `docs/project/TASK.md` with detailed logs.
   - Update `work_log/YYYY-MM-DD_session.md`.
3. **Clear Context**:
   - Delete `docs/project/GSD_CONTEXT.md`.
   - Remove/Wipe `IMPLEMENTATION_PLAN.md`.
4. **Commit**: Standard git commit and push.

---

## 🛑 Rules for GSD Mode

- **No Vibe Coding**: If it's not in the `IMPLEMENTATION_PLAN.md`, don't do it.
- **Context is King**: If the chat gets longer than 15-20 messages, run `/gsd:save` and start a new window.
- **Single Source of Truth**: The files (`ROADMAP.md`, `TASK.md`) are the only memory you should trust.

---

**Last Updated**: 2026-01-26
