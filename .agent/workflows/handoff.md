---
description: Handoff current session to the next AI agent
---

# /handoff — 交接協議

> **本檔案為交接入口。** 當任務進行到一半需要中斷，或需要更換 Session 時使用。

## 執行步驟

// turbo
1. 讀取交接協議：
   ```text
   view_file /Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/handoff_protocol.md
   ```

2. 按照協議執行：
   - 整理當前進度與狀態 (TASK_INDEX / STATE.md / STATE_GSD.md)
   - 建立交接文件：`release-aggregator/docs/handoffs/YYYY-MM-DD_HANDOFF.md`
   - 產生給下一場 Session 的 Prompt
