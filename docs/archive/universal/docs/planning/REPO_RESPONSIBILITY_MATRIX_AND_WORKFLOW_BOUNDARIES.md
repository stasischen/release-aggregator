# Repo Responsibility Matrix and Workflow Boundaries

Date: 2026-02-14  
Status: Active guardrail (must read before executing any split task)

## Purpose

Stop cross-repo drift and enforce clear execution boundaries for the split architecture.

## Canonical Repositories

1. `core-schema`
2. `content-ko` (and future `content-<target_lang>`)
3. `content-pipeline`
4. `release-aggregator`
5. `lingo-frontend-web`
6. `Lingourmet_universal` (planning/archive only)

## Responsibility Matrix

### 1) core-schema

Allowed:
1. Define JSON schemas.
2. Maintain validator tooling.
3. Maintain contract/versioning docs.

Not allowed:
1. Content ingestion logic.
2. Frontend runtime code.
3. Release deployment logic.

### 2) content-ko

Allowed:
1. Source content storage.
2. Import/normalize/review scripts for KO source.
3. Merge precedence and conflict reports.

Not allowed:
1. Pipeline build orchestration for release artifacts.
2. Frontend asset sync logic.
3. Global manifest/deploy logic.

### 3) content-pipeline

Allowed:
1. Build/transform/validate workflow.
2. CI checks for pipeline outputs.
3. Output artifact generation from source repos.

Not allowed:
1. Direct editing of source-of-truth content in content repos.
2. Release publishing/deploy steps.
3. Frontend runtime behavior changes.

### 4) release-aggregator

Allowed:
1. Collect artifacts.
2. Generate global manifest with provenance.
3. Stage/publish release outputs.

Not allowed:
1. Mutating content source data.
2. Rebuilding content logic owned by content-pipeline.
3. Frontend code changes.

### 5) lingo-frontend-web

Allowed:
1. Intake/sync released artifacts.
2. Runtime loading and feature integration.
3. Frontend tests and app behavior.

Not allowed:
1. Content production pipeline logic.
2. Schema contract source-of-truth changes.
3. Release aggregation/deploy code.

### 6) Lingourmet_universal (monorepo)

Allowed:
1. Planning documents.
2. Migration records.
3. Cross-repo coordination notes.

Not allowed:
1. Active frontend implementation.
2. Active content production implementation.
3. Active pipeline/release implementation.

## Workflow Placement (Where Pipeline Work Belongs)

1. Source ingestion and normalization:
   - `content-ko`
2. Build/validate transformation pipeline:
   - `content-pipeline`
3. Aggregation/publish workflow:
   - `release-aggregator`
4. Intake and runtime verification:
   - `lingo-frontend-web`

## Execution Guardrail for Gemini

Before starting any task, Gemini must:

1. Identify target repo and task id.
2. Check if planned file edits match repo responsibilities.
3. If scope crosses boundaries:
   - stop immediately
   - output `BLOCKED: CROSS_REPO_SCOPE_VIOLATION`
   - list violating files and expected repo owner

## Mandatory Preflight Output (Every Task)

Gemini must output this before coding:

1. `task_id`
2. `target_repo`
3. `allowed_scope_summary`
4. `planned_files`
5. `boundary_check` (`PASS` or `BLOCKED`)

If `boundary_check=BLOCKED`, no edits are allowed.

## Mandatory Completion Output (Every Task)

1. `task_id`
2. `commit_hash`
3. `changed_files`
4. `commands_run`
5. `test_results`
6. `blockers`
7. `handoff_file_path`

## Ready-to-Use Prompt

```text
先讀 docs/planning/REPO_RESPONSIBILITY_MATRIX_AND_WORKFLOW_BOUNDARIES.md。
執行任務前先輸出 preflight（task_id/target_repo/planned_files/boundary_check）。
若 boundary_check 不是 PASS，停止並回報 BLOCKED，不可修改任何檔案。
```
