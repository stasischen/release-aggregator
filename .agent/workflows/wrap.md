---
description: control-tower closeout shim — 收工協議入口
---

# /wrap — 收工 (Closeout Shim)

> **本檔案僅為跳轉入口。** Agent 收工時必須前往 Aggregator 讀取完整協議。

## 執行步驟

// turbo

1. 讀取收工協議：

   ```text
   view_file release-aggregator/docs/runbooks/gemini_closeout_protocol.md
   ```

2. 按照收工協議的 Step 1~4 依序執行：

   - Step 1: 提交所有變更
   - Step 2: 撰寫 Worklog（**必須寫入 Aggregator**）
   - Step 3: 輸出收工報告
   - Step 4: 執行 Repo 專用檢查

## 硬規則

- **Worklog 唯一存放處**：`release-aggregator/docs/worklogs/YYYY-MM-DD.md`。
- 如當天已有 Worklog，必須以 **追加 (append)** 方式寫入，不可覆蓋。
- 必須提供 commit hash 作為完成證據，不可空口 claim。
- **防覆蓋**：寫入 Worklog 前必須先 `git pull` 再 `view_file` 確認現有內容，禁止直接 `write_to_file` + `Overwrite: true`。
