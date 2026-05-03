# Tasks Workspace

這個目錄是 release-aggregator 的任務工作區。

## Layout

- `docs/tasks/` 根層：active working set
- `docs/tasks/assets/`：可重用參考文件、spec、schema、contract、mockup
- `docs/tasks/templates/`：Task Brief、Codex packet、GPT review、handoff 等跨模型模板
- `docs/tasks/archive/`：已完成或封存的歷史任務

## Rule

- 新任務先放根層 active working set
- 非 trivial 任務先建立 `Task Brief`，再下發給 Codex / Gemini / DeepSeek
- completed / historical task artifacts 移到 `archive/`
- reference-only material 放 `assets/`
- `TASK_INDEX.md` 是進入點，新增或完成任務時要同步更新

## Multi-Model Workflow

- 日常跨模型協作規範：`docs/runbooks/multi_model_task_orchestration.md`
- Task brief template：`docs/tasks/templates/TASK_BRIEF_TEMPLATE.md`
- Codex implementation packet：`docs/tasks/templates/CODEX_TASK_TEMPLATE.md`
- GPT diff review prompt：`docs/tasks/templates/GPT_DIFF_REVIEW_TEMPLATE.md`
- Milestone handoff：`docs/tasks/templates/HANDOFF_SUMMARY_TEMPLATE.md`
