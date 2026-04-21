---
description: control-tower startup shim — 開工協議入口
---
# /start — 開工 (Startup Shim)

> **本檔案僅為跳轉入口。** Agent 開工時必須前往 Aggregator 讀取完整協議。

## 執行步驟

// turbo
1. 讀取開工協議：
   ```
   view_file docs/runbooks/gemini_startup_protocol.md
   ```

// turbo
2. 讀取控制塔首頁：
   ```
   view_file docs/index.md
   ```

3. 按照開工協議的 Step 1~3 向使用者確認目標。
4. 若 `/` 清單看不到 `/gsd:*`，改用本地入口 `/gsd`（`.agent/workflows/gsd.md`）。

## 硬規則
- 協議唯一來源：`docs/runbooks/`。
- **Worklog 唯一存放處**：`docs/worklogs/YYYY-MM-DD.md`。
- 不得使用各 Repo 本地的 legacy workflow 作為執行依據。
