# Zellij Control Tower Setup

## Goal
Use `release-aggregator` as the CLI entry point while keeping fast access to all Lingo repos in one Zellij workspace.

## Layout
- Layout file: `/Users/ywchen/Dev/lingo/release-aggregator/tools/zellij/lingo_control_tower.kdl`
- Launcher script: `/Users/ywchen/Dev/lingo/release-aggregator/scripts/ops/start_lingo_control_tower.sh`

Tabs and panes:
- `control-tower`: `release-aggregator`, `content-ko`, `content-pipeline`
- `schema-frontend`: `core-schema`, `lingo-frontend-web`, `lllo`

## Start Command
From any terminal:

```bash
/Users/ywchen/Dev/lingo/release-aggregator/scripts/ops/start_lingo_control_tower.sh
```

Optional custom session name:

```bash
/Users/ywchen/Dev/lingo/release-aggregator/scripts/ops/start_lingo_control_tower.sh lingo-main
```

## Can Aggregator Entry Edit `content-ko`?
Yes, with boundary rules:
- If your workspace root is `/Users/ywchen/Dev/lingo`, CLI can operate across sibling repos.
- Run commands in the target repo pane or use explicit repo path (for example `git -C /Users/ywchen/Dev/lingo/content-ko ...`).
- Keep one task per repo per phase; do not mix cross-repo edits in one atomic commit.

## Recommended Session Flow
1. Open Zellij via launcher.
2. In `release-aggregator` pane, choose task from `docs/tasks/TASK_INDEX.md`.
3. Execute task in target repo pane (`content-ko`, `content-pipeline`, etc.).
4. Commit in target repo, then sync status back to aggregator task files.
