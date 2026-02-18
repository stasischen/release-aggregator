# AI Handoff Protocol (交接協議)

## Goal
在任務尚未完全結束（未達到 `/wrap` 條件）但需要中斷 Session 時，確保進度被完整記錄，讓下一個 Agent 能無縫接手。

## Handoff Sequence

### Step 1: 整理進度狀態
Agent 必須讀取以下檔案以彙整現況：
- `release-aggregator/docs/tasks/TASK_INDEX.md`
- 各 Repo 的 `STATE.md` (若存在)
- 當前的 `worklog`

### Step 2: 建立交接文件
建立檔案 `release-aggregator/docs/handoffs/YYYY-MM-DD_{TASK_ID|Topic}.md`。內容包含：
- **Context**: 目前處理到哪個任務、哪個步驟。
- **Accomplishments**: 本 Session 完成了什麼（含 Commit Hash）。
- **Infrastructure**: 使用了哪些腳本、產出了哪些臨時檔案。
- **Remaining**: 接下來要做的具體動作（帶入具體 ID 或檔案路徑）。

### Step 3: 更新工作日誌
在當天的 Worklog 中增加一個 Session 區塊，標註為 `(Handoff: Continued in next session)`。

### Step 4: 輸出接力 Prompt
向使用者輸出一個清楚的 Markdown 區塊，包含「給下個 Agent 的啟動命令」，確保下一個 Agent 啟動後能直接進入狀態。

## Boundary Rules
- **不要提交未完成的破壞性變更**：如果程式碼目前無法編譯，應在交接文件中特別註明，或暫存在 `data/staging/`。
- **路徑明確化**：交接文件中的路徑必須使用絕對路徑或 Repo 相對路徑。
