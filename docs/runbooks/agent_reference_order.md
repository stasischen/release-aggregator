# Agent Reference Order

## Goal
Prevent agent confusion between active protocol and archived historical docs.

## Mandatory Read Order (Active Protocol)
1. `docs/index.md`
2. `docs/workflow_map.md`
3. `docs/runbooks/gemini_startup_protocol.md`
4. `docs/runbooks/gsd_multi_repo_workflow.md` (跨 Repo 或 phase-based 任務必讀)
5. `docs/runbooks/multi_model_task_orchestration.md` (多模型協作、跨 thread、跨電腦任務必讀)
6. `docs/runbooks/gemini_stage_execution_protocol.md`
7. `docs/runbooks/gemini_closeout_protocol.md`
8. `docs/ops/stage_contract_matrix_ko.md`

## Optional Read (When Comparing Legacy Process)
- `docs/archive/universal/INDEX.md`
- `docs/archive/universal/.agent/workflows/**`

## Hard Rule
- `docs/archive/universal/**` is reference-only.
- Archived docs must never override active protocol.

## Session Start Prompt (Recommended)
```text
只使用 /Users/ywchen/Dev/lingo/release-aggregator/docs/** 作為現行協議。
若要比較舊流程，只可讀 /Users/ywchen/Dev/lingo/release-aggregator/docs/archive/universal/**，不得把封存內容當現行規範。
先列出本次依據的文件路徑，再執行。
```

## Compliance Check
Before execution, agent must output:
- `active_docs_used`
- `archive_docs_used` (if any)
- `decision_source` (`active` or `comparison_only`)
- `execution_mode` (`classic_stage` or `gsd_phase`)
