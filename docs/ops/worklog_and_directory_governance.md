# Worklog and Directory Governance

## Purpose
Define one stable place for daily logs and a clean rule for multi-repo WIP.

## Single Source of Daily Worklog
- Canonical daily log location: `release-aggregator/docs/worklogs/YYYY-MM-DD.md`
- One file per day across the whole Lingo system.
- Do not create full daily logs in each repo.

## What Stays in Each Repo
- `CHANGELOG.md`: only approved and merged changes.
- `docs/handoffs/*.md`: task handoff records.
- No duplicated daily timeline in feature repos.

## Directory Plan (Control Tower)
- `docs/index.md`: entry point
- `docs/repo_map.md`: repo boundaries
- `docs/workflow_map.md`: pipeline phases
- `docs/owners.md`: ownership and handoff boundaries
- `docs/tasks/*.json`: active mission boards
- `docs/worklogs/_template.md`: daily template
- `docs/worklogs/YYYY-MM-DD.md`: actual daily records
- `docs/ops/*.md`: policies and governance
- `docs/runbooks/*.md`: executable procedures
- `docs/handoffs/*.md`: completion reports

## Branch and WIP Rule
- Use repo-local `wip/*` branches for undecided work.
- If a task is not finalized, log it in daily worklog only.
- Move to repo changelog/handoff only after decision and merge path is clear.

## Daily Closeout Minimum
Each day log must include:
- `Summary`
- `Changed Repos`
- `Pending Decisions`
- `Blockers`
- `Next Actions`

## Pending Decisions Format
- `repo`: repo name
- `branch`: branch name
- `scope`: one-line change summary
- `risk`: what can break
- `decision_needed`: what must be decided
- `owner`: who decides
