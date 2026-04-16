# Tasks Workspace

這個目錄是 release-aggregator 的任務工作區。

## Layout

- `docs/tasks/` 根層：active working set
- `docs/tasks/assets/`：可重用參考文件、spec、schema、contract、mockup
- `docs/tasks/archive/`：已完成或封存的歷史任務

## Rule

- 新任務先放根層 active working set
- completed / historical task artifacts 移到 `archive/`
- reference-only material 放 `assets/`
- `TASK_INDEX.md` 是進入點，新增或完成任務時要同步更新
