# Multi-Model Project Review Workflow

This workflow keeps full-repo scanning separate from architecture decisions.
Use it for large refactors, cross-repo migrations, architecture audits, or any change where the blast radius is larger than one bounded module.

## Core Roles

| Role | Owner | Primary Work | Output | Must Not Own |
| :--- | :--- | :--- | :--- | :--- |
| Repo mapper | Gemini | Scan full repo, map modules, describe data flow, identify dependency paths | Architecture map, risk hotspots, relevant files | Final refactor decision |
| Cleanup analyst | DeepSeek | Batch-find duplication, stale files, naming drift, dead code, TODOs, old flows | Pain-point inventory, cleanup candidates, suspicious files | Architecture direction |
| Architecture judge | GPT | Review condensed packet, decide boundaries, migration order, risk controls | Decision memo, migration plan, review verdict | Raw full-repo mining by default |
| Implementer | Codex / DeepSeek | Apply small scoped patches, update tests, run validation | Patch, test result, implementation note | Unapproved architecture expansion |

## Standard Flow

1. Gemini performs the full-repo scan.
2. DeepSeek performs cleanup and consistency inventory.
3. Codex assembles the review packet from both outputs.
4. GPT reviews only the packet, key file summaries, and current diff.
5. Codex converts GPT's decision into small implementation tasks.
6. GPT reviews critical PRs, migration diffs, and final architecture audit.

## When GPT Should See More Context

Use expanded context only when one of these is true:

- Gemini and DeepSeek outputs contradict each other.
- Domain logic is too subtle to summarize safely.
- A migration crosses repo ownership boundaries.
- A final architecture audit is required before merge.
- A production-risking regression cannot be localized.

Avoid expanded context for simple file discovery, dependency listing, cleanup-only changes, or narrow patches.

## Review Gates

Before implementation starts:

- The project goal is explicit.
- Current architecture is summarized in 20-50 lines.
- Pain points are ranked by severity.
- Relevant files are capped to the smallest useful set.
- Cross-repo ownership boundaries are identified.
- Acceptance criteria and rollback criteria are written.

Before merge:

- All changed files are inside approved scope.
- Tests or validation commands have run, or missing coverage is explicitly recorded.
- Migration compatibility is addressed.
- GPT has reviewed P0/P1 risks and critical diff.
- Cleanup-only items are separated from behavior changes.

## Severity Model

| Level | Meaning | Required Action |
| :--- | :--- | :--- |
| P0 | Data loss, broken release, broken runtime, schema incompatibility | Stop and fix before proceeding |
| P1 | Migration failure risk, cross-repo contract break, hidden dependency | Fix or add explicit mitigation |
| P2 | Maintainability debt, duplication, unclear ownership | Track and schedule |
| P3 | Cosmetic cleanup, naming polish, optional simplification | Batch when convenient |

## Operating Rule

GPT acts as the architecture reviewer and decision maker.
Gemini and DeepSeek produce evidence.
Codex turns decisions into scoped patches and verification.
