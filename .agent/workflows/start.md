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
- **Context hygiene**：若同一 thread 已跨多個 milestone、同時牽涉多個 agent/repo dirty state、或新任務已從資料 intake 轉到 UI/產品 QA/架構 review，Agent 必須主動提醒使用者考慮開新 thread。
- 建議開新 thread 前，Agent 必須先輸出並落盤 `Handoff Summary`，至少包含：已完成、目前決策、重要上下文、相關檔案、未解問題、下一步、不要重做/不要改的東西。
