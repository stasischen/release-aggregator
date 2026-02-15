---
description: How to setup and run Antigravity on multiple machines (Distributed Workflow)
---

# 🌍 Distributed Workflow & Agent Manager Guide

This guide explains how to scale Antigravity across multiple computers (e.g., specific machines for Content vs. Coding) and how the "Agent Manager" protocol works.

## 1. Multi-Computer Setup (The Setup)

Each computer is treated as a distinct "Agent" with its own identity.

### A. Clone & Prepare
On the **new computer**:
1. Clone the repository.
2. Create/Update `.agent_identity.json` in the root (do NOT commit this file):

```json
{
    "agent_id": "Agent-MacBook-Pro",  // Unique Name
    "default_role": "builder",
    "machine_name": "Pro-M3-Max",
    "capabilities": ["flutter", "ios-build"]
}
```

### B. Environment Lock
Run the environment setup to lock the model context for this specific machine:
```bash
./scripts/set_model.sh "Pro"  # or "Flash" for weaker machines
```

---

## 2. The "Agent Manager" (The Brain) 🧠

"Agent Manager" is not a separate app; it is a **Protocol** that runs on top of Git. The "Database" is `AGENT_TASKS.json`.

### How to Distribute Work (Manager Mode)
When you want to split work across machines:

1. **Plan**: Open a "Planning" session on your main machine.
2. **Dispatch**: Ask the Agent: "Create tasks for fixing the UI and writing tests."
   - The Agent will write multiple entries into `AGENT_TASKS.json` with `status: "TODO"`.
3. **Sync**: The Agent commits and pushes `AGENT_TASKS.json`.

### How to Claim Work (Worker Mode)
On the **worker machines**:

1. **Start**: Open a session (or run the heartbeat daemon).
2. **Claim**: The Agent looks at `AGENT_TASKS.json`, finds a `TODO` item, and marks it:
   - `status`: "IN_PROGRESS"
   - `assignee`: "Agent-MacBook-Pro"
   - `heartbeat`: [Current Timestamp]
3. **Lock**: It commits and pushes this change. Now other machines know this task is taken.

---

## 3. The Heartbeat Daemon 💓

To ensure agents don't step on each other, you should run the heartbeat script in the background on active machines.

```bash
# Keeps your lock active and syncs status every 30 mins
python3 scripts/agent_heartbeat.py
```

- **If you crash**: The heartbeat stops.
- **Recovery**: After 60 mins (STUCK timeout), another Agent (Manager) can "Steal" the task back to `TODO`.

---

## 4. Practical Example: "GSD" across 2 Machines

**Goal**: PC-1 does coding, PC-2 does content generation.

1. **PC-1 (Manager)**:
   - Protocol: `/gsd:plan`
   - Output: Creates 2 tasks in `AGENT_TASKS.json`.
     - Task A: "Refactor Widget" (Role: Builder)
     - Task B: "Generate Thai Audio" (Role: Content)

2. **PC-1 (Worker)**:
   - Claims "Task A".
   - Updates `docs/project/GSD_CONTEXT.md` with coding context.
   - Codes...

3. **PC-2 (Worker)**:
   - Claims "Task B".
   - Updates `docs/project/GSD_CONTEXT.md` with content context.
   - Runs generation scripts...

4. **Merge**:
   - Both push changes.
   - Git handles the code merge.
   - `AGENT_TASKS.json` shows both as "DONE".

---

**Last Updated**: 2026-01-26
