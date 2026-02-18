---
description: gsd workflow shim — GSD protocol 入口
---
# /gsd — GSD Workflow Entry

> 本檔案是本地入口，讓 `/` 指令清單可直接看到 GSD。
> 實際規範以 control tower runbook 為準。

## 執行步驟


1. 讀取 GSD 主協議：

   ```text
   view_file /Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/gsd_multi_repo_workflow.md
   ```

2. 讀取開工協議（確認 execution_mode 與 decomposition check）：

   ```text
   view_file /Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/gemini_startup_protocol.md
   ```

3. 依模式執行：

   - `classic_stage`：走 stage protocol，不進 `/gsd:*`。
   - `gsd_phase`：依 runbook 執行 discuss/plan/execute/verify。

## 指令可見性說明

- 若你的執行器不支援 Gemini 外掛斜線指令，`/gsd:*` 可能不會顯示在 `/` 清單。
- 這種情況下，仍以 runbook 步驟執行即可（先 `/start`，中段照 GSD，最後 `/wrap`）。
