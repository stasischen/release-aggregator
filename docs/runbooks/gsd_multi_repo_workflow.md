# GSD Multi-Repo Workflow (Aggregator Control Tower)

## Goal
在 `release-aggregator` 作為控制台時，使用 GSD + Gemini CLI 穩定協調多個 Repo，避免跨 Repo context 汙染與錯誤提交。

## Scope
- 控制台 Repo: `release-aggregator`
- 執行目標 Repo: `content-ko`, `content-pipeline`, `core-schema`, `lingo-frontend-web`, `lllo`

## Runtime Model
- GSD 是 workflow/orchestration 層。
- Gemini CLI 是執行模型與命令載體。
- 建議在控制台安裝 GSD（global），在各目標 Repo 執行 phase 指令。

## Directory and State Layout

### Portfolio Layer (Aggregator)
- `release-aggregator/docs/tasks/TASK_INDEX.md`: 全域任務入口。
- `release-aggregator/docs/tasks/`: 跨 Repo phase/里程碑任務檔。
- `release-aggregator/docs/worklogs/YYYY-MM-DD.md`: 跨 Repo session 收工記錄。

### Repo Layer (Per Repository)
每個執行 Repo 自行維護：
- `SPEC.md`: 目標與需求邊界。
- `PLAN.md`: phase 任務拆解與 Task IDs。
- `STATE.md`: 實作進度、已決策架構、blockers。

## Setup

### 1) Install GSD for Gemini
在 aggregator 或任一終端：

```bash
npx get-shit-done-cc --gemini --global
```

驗證：

```bash
/gsd:help
```

### 2) Pre-flight Checks
- 已完成 Gemini CLI 登入。
- 在預期提交的 Repo 內執行指令（避免 commit 到錯誤倉庫）。
- 每個 Repo 的 `SPEC.md`/`PLAN.md`/`STATE.md` 已存在（若缺失先補齊）。

## Standard Operating Flow

### Stage A: Portfolio Planning (in aggregator)
1. 開新 session，先讀 `docs/tasks/TASK_INDEX.md`。
2. 選定本次里程碑與目標 Repo。
3. 在 aggregator 記錄 phase 依賴與順序（A -> B -> C）。

### Stage B: Repo-specific Execution (in target repo)
在目標 Repo 開新 session，執行：
1. `/gsd:map-codebase`（brownfield 建圖，首次或重大變更時）
2. `/gsd:new-project`（補強/校準該 Repo 規格）
3. `/gsd:discuss-phase <N>`
4. `/gsd:plan-phase <N>`
5. `/gsd:execute-phase <N>`
6. `/gsd:verify-work <N>`

### Stage C: Closeout and Sync
1. 目標 Repo 完成原子 commit。
2. 回寫該 Repo `STATE.md`。
3. 回到 aggregator 更新任務狀態與 `docs/worklogs/YYYY-MM-DD.md`。

## Commit and Boundary Rules
- 一個 phase 只允許一個 Repo。
- 跨 Repo需求必須拆成兩個以上 Task，不可單 task 同改多 repo。
- 每個 Task 使用原子 commit（可回滾、可審核）。
- 未經使用者要求，不得跨 repo 自動改檔。

## Session Policy
- 新 phase 一律新 session（手動重開）。
- 新 session 啟動時，僅載入：
  - 目標 Repo 的 `SPEC.md`、`PLAN.md`、`STATE.md`
  - 這次 Task 需要的少量程式碼檔案
- 禁止延續舊 session 直接做下一個 phase。

## Prompt Template (Target Repo)
```text
請先讀：
- <repo>/SPEC.md
- <repo>/PLAN.md
- <repo>/STATE.md

只執行 PLAN.md 中 Task ID: <TASK_ID>
限制：
- 不要做其他任務
- 完成後更新 STATE.md
- 提供建議 commit message 與驗證結果
```

## Failure Handling
- 若 phase 驗證失敗：停止進入下一 phase，先在當前 Repo 修復並更新 `STATE.md`。
- 若發現跨 Repo blocker：回 aggregator 新增 dependency task，重新排 phase。
- 若命令名稱與文件不一致：以 `/gsd:help` 輸出為準。

## Minimal Pilot Plan (1 Week)
1. Pilot-1 (`content-ko`): 建立/校準 `SPEC.md` + `PLAN.md` + `STATE.md`。
2. Pilot-2 (`content-pipeline`): 執行一個可驗證的小型 phase，輸出原子 commit。
3. Pilot-3 (`core-schema`): 跑一次 schema 變更到 consumer repo 的完整依賴流程。
4. 在 aggregator 回顧：記錄 cycle time、回滾次數、跨 repo blockers。
