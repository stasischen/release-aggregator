# Multi-Model Task Orchestration

本文件是 Lingourmet 日常任務的主控協議。它把大型 review 用的
`docs/review/MULTI_MODEL_PROJECT_REVIEW.md` 下沉成每個任務都能使用的固定流程。

## Source Of Truth

- 主控 repo：`release-aggregator`
- 任務入口：`docs/tasks/TASK_INDEX.md`
- 任務模板：`docs/tasks/templates/`
- 大型 review packet：`docs/review/PROJECT_REVIEW_PACKET_TEMPLATE.md`
- 模型輸入規格：`docs/review/MODEL_INPUT_SPECS.md`
- 跨機執行協議：`docs/runbooks/codex_antigravity_orchestration.md`

所有跨 repo 任務都先在 `release-aggregator` 建立 task brief。不要只把任務留在聊天 thread。

## Model Roles

| Model | Role | Owns | Does Not Own |
| :--- | :--- | :--- | :--- |
| GPT 5.5 | 總指揮、架構師、最終 reviewer | 決策、拆任務、風險判斷、critical diff review | 長時間掃全 repo、批量整理 |
| Codex | 實作手與整合者 | 小範圍改 code、跑測試、更新任務文件、整合修正 | 未核准的大重構 |
| Gemini | 長 context 掃描者 | 全 repo / 跨 repo map、資料流、檔案關係、文件整理 | 最終架構決策 |
| DeepSeek | 低成本整理者 | 大量草稿、cleanup inventory、方案初稿、內容初稿 | production-critical 決策 |
| Local Qwen | 私有低成本草稿者 | 私有資料初篩、快速改寫、翻譯/atom 批量實驗 | 最終品質裁決 |

## DeepSeek Model Choice

DeepSeek 在本 workspace 以 `deepseek-v4-flash` 作為預設省成本模型，以 `deepseek-v4-pro` 作為高可靠模型。

### Use `flash` when

- 起草 Task Brief
- 大量整理、摘要、轉述、格式化
- repo 掃描、inventory、文件歸納
- 低風險的第一輪 bug triage
- 內容初稿、翻譯、批量改寫
- 只是要把資訊蒸餾成給 GPT 5.5 的材料

### Use `pro` when

- 需要做結論或裁決
- review diff、review architecture
- 涉及資料流、schema、release path、public API
- 跨 repo / 跨模組的高風險推理
- bug root cause 不容易定位
- 任何失誤會導致重工或破壞發布

### Switch Rule

- 先 `flash`，再 `pro`：先蒐集材料，再做決策。
- 如果任務要「產生材料」就用 `flash`。
- 如果任務要「下判斷」就用 `pro`。
- 如果不確定，預設 `flash`，但在輸出前由 GPT 5.5 或 Codex 判定是否升級到 `pro`。

## Default Flow

1. Gemini 掃全局，輸出 architecture / relevant files / risk hotspots。
2. DeepSeek 整理問題、cleanup candidates、方案 A/B/C。
3. GPT 5.5 只讀濃縮材料，做決策與切任務。
4. Codex 依 task brief 做小範圍實作。
5. GPT 5.5 review diff。
6. Codex 修正 review findings。
7. GPT 5.5 做 final checklist。

小任務可以跳過 Gemini / DeepSeek，但不可跳過 task brief 與驗收標準。

## Task Size Policy

| Task Type | Default Flow |
| :--- | :--- |
| 小 bug | Codex 實作 + GPT diff review |
| 單 repo 中型改動 | Gemini 或 Codex 先整理 context，GPT 決策，Codex 實作 |
| 跨 repo 改動 | Gemini 掃全局 + DeepSeek inventory + GPT 決策 + Codex 分段 |
| 大 refactor | GPT 先切 phase / plan，Codex 或 Antigravity 分段執行 |
| 內容/課程草稿 | DeepSeek `flash` 或 Qwen 起草，GPT 定稿 |
| 翻譯/atom 批量處理 | Qwen 或 DeepSeek `flash` 批量跑，GPT 抽查 |
| 架構決策 | 必須 GPT 5.5 |

## Required Artifacts

每個非 trivial 任務至少要有：

- `Task Brief`：目標、背景、相關檔案、限制、方案、風險、驗收。
- `Implementation Packet`：給 Codex / executor 的窄 scope 指令。
- `Review Prompt`：給 GPT 5.5 review diff 的固定問題。
- `Handoff Summary`：milestone 結束或換 thread / 換電腦時使用。
- `DeepSeek Model Hint`：當任務要交給 DeepSeek 時，先標明 `flash` 或 `pro`。

模板在 `docs/tasks/templates/`。

## Directory Convention

建議每個新任務用一個目錄保存封包與回報：

```text
docs/tasks/<TASK_ID>/
  TASK_BRIEF.md
  GEMINI_SCAN.md
  DEEPSEEK_INVENTORY.md
  DEEPSEEK_DECISION.md
  GPT_DECISION.md
  CODEX_TASK.md
  GPT_DIFF_REVIEW.md
  HANDOFF_SUMMARY.md
```

如果任務很小，也可以只放 `docs/tasks/<TASK_ID>_PLAN.md`，但內容仍需符合 Task Brief 欄位。

## Thread Strategy

- 一個專案方向維持一個主 thread。
- 一個 major milestone 開一個新 thread。
- 小步驟不要各自開 thread。
- milestone 結束必須輸出 `Handoff Summary`，並存回 task 目錄或 `docs/handoffs/`。

## Startup Checklist For Any Agent

1. 讀 `GEMINI.md`。
2. 讀 `docs/index.md`。
3. 讀 `docs/runbooks/agent_reference_order.md`。
4. 讀 `docs/runbooks/multi_model_task_orchestration.md`。
5. 讀 `docs/tasks/TASK_INDEX.md`。
6. 若有指定 task，讀該 task 目錄內的 `TASK_BRIEF.md` 和最新 `HANDOFF_SUMMARY.md`。
7. 只在指定 repo / scope 內操作。

## Completion Checklist

任務結束前必須確認：

- Changed files 在 approved scope 內。
- 測試或驗證命令已執行，或記錄無法執行原因。
- 若跨 repo，資料契約與 release path 有明確驗證。
- GPT review 的必修問題已修正或明確 deferred。
- `TASK_INDEX.md`、worklog、handoff 已按需要更新。
