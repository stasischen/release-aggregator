# 流程優化提案計畫 (Workflow Optimization Plan)

分析目前的 Lingo 工作流程，我發現了幾個明顯的痛點，並提出以下優化方向。

## 1. 任務追蹤自動化 (Task Tracking Automation)
目前最大的痛點是手動同步 `XXX_TASKS.json` 和 `TASK_INDEX.md`。每次 Agent 完成一個小知識點或一堂課，都需要分別修改 JSON 檔案的 status 與 goal 括號內的進度，同時還要記得去 `TASK_INDEX.md` 更新對應的文字。這極容易出錯且耗費 Token。

*   **建議行動**: 執行 `FUTURE_BACKLOG_TASKS.json` 中的 `AUTO-TASK-01`。
*   **實作細節**:
    1.  在 `release-aggregator/scripts` 下建立一個 Python 腳本 (`sync_task_index.py`)。
    2.  該腳本會遍歷 `docs/tasks/` 下所有的 `*_TASKS.json` 檔案。
    3.  根據 JSON 內定義的任務總數與 `status: "DONE"` 的數量，自動計算進度 (例如 15/25)。
    4.  自動解析 `TASK_INDEX.md`，並使用 Regex 更新對應行的進度與狀態。
    5.  **進階**: 將此腳本加入 git hook (pre-commit) 或在 `/wrap` 收工協議中強制呼叫。

## 2. 減少跨 Repo 關聯操作的摩擦
目前架構分為 `content-ko`、`lllo` (編輯)、`content-pipeline`、`core-schema` 與 `release-aggregator`。

*   **痛點**: 像是在 `lllo` 修改了 C1 內容後，按照任務 `KO-INGEST-01`，我們需要手動將 `lllo` 的資料 pull 到 `content-ko`，然後執行 mapping pipeline。這牽涉到多個 Repo 的 git 切換與指令發布。
*   **建議行動 (Pipeline Integration)**:
    1.  完善 `CONTENT_PIPELINE_SEPARATION` 工作。將語言特定的引擎 (韓文解析) 與通用的建置流程分離。
    2.  建立跨 Repo 的自動化 ingested script。在 `release-aggregator` 提供一個 unified command (例如 `make ingest-ko`)，自動在背後執行 `git pull lllo` -> 複製到 `content-ko` 暫存區 -> 觸發 `content-ko` 的解析與轉檔。

## 3. 字典品質守門員 (Dictionary Quality Gates) 左移
在 `MAPPING_DICTIONARY_TASKS.json` 中，我們正在穩定字典流程。但目前許多欄位遺失 (如 i18n 未填) 要到最後 build 階段才會發現。

*   **建議行動**:
    1.  在編輯端 (目前可能是手動或 Agent 協助) 引入 pre-validation。
    2.  將 `content-ko/scripts/qa/check_atom_extraction_integrity.py` 整合到持續整合 (CI) 流程，或在提交翻譯 CSV 時就先檢查是否還有 `[zh-TW]` 作為 placeholder 的詞彙，擋下不完整的提交。

## 4. Prompt / Context 的優化
目前 Agent 啟動時必須去讀取大量的 runbook 和 `TASK.json`。

*   **建議行動**: 收斂 runbook 的數量，或在 `release-aggregator/docs/index.md` 建立更精簡的上下文入口，讓 Agent 能更快抓住當前脈絡。

## 結論與下一步
建議優先執行 **任務追蹤自動化 (AUTO-TASK-01)**，這能立即減少 Agent 和人類開發者在維護進度上的心智負擔。
