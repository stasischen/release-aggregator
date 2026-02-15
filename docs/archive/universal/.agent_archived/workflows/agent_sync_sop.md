---
description: Agent Git-based Sync Protocol (GMAO v1.3 with AME)
---

# 🤖 Agent Sync Protocol (GMAO v1.3)

包含分層架構 (Tiered Workflow)、自動模型升級協議 (AME) 與任務邊界保護。

---

## 📝 計畫同步協議 (Plan-to-Task Sync)

**目的**: 確保 `REFACTORING_PLAN.md` (人類可讀) 與 `AGENT_TASKS.json` (機器可讀) 之間的一致性。

### 同步流程

1. **使用者觸發**: 使用者詢問「目前有哪些任務待處理？」或類似指令
2. **Agent 掃描**: 掃描 `REFACTORING_PLAN.md` 並比對 `AGENT_TASKS.json`
3. **差異報告**: Agent 報告新增/不一致/可移除的任務
4. **手動同步**: 經使用者確認後，Agent 更新 `AGENT_TASKS.json`

### 報告範本

```markdown
## 📋 任務同步報告

### 🆕 待新增到 AGENT_TASKS.json
| # | 任務標題 | 優先級 | 來源 |
|---|---------|-------|------|
| 1 | [任務名稱] | High/Medium/Low | REFACTORING_PLAN.md #X |

### ⚠️ 狀態不一致
| 任務 ID | Plan 狀態 | Tasks 狀態 | 建議動作 |

### 🗑️ 可移除
| 任務 ID | 原因 |

是否要我執行同步？
```

### 注意事項
- Agent **不會自動同步**，必須經過使用者確認
- 同步後應立即 commit 並 push

---

## ⏱️ Timeout Policy (v1.3 更新)

| 階段 | 時間 | 說明 |
|------|------|------|
| **ACTIVE** | 0-15 分鐘 | 正常工作中（有 commit 活動） |
| **IDLE** | 15-45 分鐘 | 無 commit 但未超時 |
| **STALE** | 45-60 分鐘 | 超時警告 |
| **STUCK** | > 60 分鐘 | **請其他 Agent 通知用戶** |

```json
{
  "timeout_policy": {
    "warning_at_minutes": 25,
    "grace_period_minutes": 45,
    "stuck_at_minutes": 60,
    "require_progress_commit": true,
    "auto_release": false
  }
}
```

> [!WARNING]
> **超過 60 分鐘不會自動釋放任務！**
> 其他 Agent 若發現 STUCK 任務，應通知用戶：
> ```
> ⚠️ 任務 [task-id] 已停滯超過 60 分鐘
> 負責人: [agent-id]
> 最後 heartbeat: [timestamp]
> 建議: 請確認該 Agent 是否仍在工作
> ```

---

## 📈 Automatic Model Escalation (AME)

為了平衡成本與能力，我們根據失敗次數自動升級建議模型。

### Model Tiers (模型層級)

| Tier | 代表模型 | 觸發條件 | 適用情境 |
|------|---------|---------|---------| 
| **Tier 1 (Base)** | Sonnet / Flash | `try_count` 0-1 | 初次嘗試，簡單實作，測試運行 |
| **Tier 2 (Think)** | Sonnet 3.5 (Thinking) / Pro Low | `try_count` 2-3 | 兩次失敗後，需要推理與思考 |
| **Tier 3 (Deep)** | Opus / Pro High | `try_count` > 3 | 多次失敗，需要深度邏輯與架構修正 |

### 升級規則

當任務被退回 (Status `REVIEW` -> `TODO`) 時：

1. **Reviewer (Architect) 執行**:
   - `try_count` 加 1
   - 檢查是否達到升級門檻 (2 或 4)
   - 如果達到，升級 `model_tier`
   - 更新 JSON 並 Push

2. **Builder 執行**:
   - 領取任務前，**必須檢查 `model_tier`**
   - 如果 `model_tier` 要求比當前模型高，**暫停並通知用戶切換模型**

> [!WARNING]
> **Model Tier 不符時必須暫停通知！** 不可跳過此步驟直接開始工作。

---

## 🛑 模型切換通知協議 (Mandatory Switch Protocol)

**核心原則**: Agent 無法自行切換模型。在任何需要切換模型的時機，Agent **必須停止執行並明確通知使用者**。

### 強制停止點 (Checkpoints)

| 階段 | 觸發條件 | Agent 必須說明 |
|------|---------|---------------|
| **開工 (Startup)** | 任務 `model_tier` 高於當前模型 | 「此任務需要 Tier-X 模型，請切換至 [具體模型名稱]」 |
| **執行 (Execution)** | 遇到 2 次失敗 (AME Trigger) | 「根據 AME 協議，建議升級至 Tier-2 (Thinking)，請切換模型後我將繼續」 |
| **審查 (Review)** | 任務進入 REVIEW 狀態 | 「Builder 已完成，請切換至 Architect 模型 (Opus/Tier-3) 進行審查」 |
| **交接 (Handoff)** | 需要不同能力的模型 | 「此階段需要 [規劃/實作/審查] 能力，建議切換至 [模型名稱]」 |

### 通知範本

```
⚠️ 模型切換請求

當前模型: [目前模型]
建議模型: [建議模型]
原因: [觸發原因]

請在 IDE 中切換模型後回覆 "Continue" 或 "繼續"。
```

### 階段-模型對應表

| 階段 | 建議模型 | 說明 |
|------|---------|------|
| **規劃 (Planning)** | Opus / Tier-3 | 需要深度架構分析與任務分解 |
| **實作 (Execution)** | Sonnet / Tier-1 | 適合快速實作與測試執行 |
| **審查 (Review)** | Opus / Tier-3 | 需要架構評估與品質判斷 |
| **除錯 (Debugging)** | Sonnet Thinking / Tier-2 | 需要推理與根因分析 |

---

## 📋 Quick Reference

```
開工: git pull → 檢查 Model Tier → 領取 TODO 任務 → push
工作: 每 30 分鐘更新 heartbeat
交付: Builder -> REVIEW -> Architect (Review & Escalation)
收工: 更新狀態 → push
```

#### 📦 Task Archival
When `AGENT_TASKS.json` becomes too large:
```bash
python3 scripts/archive_tasks.py
```
- Moves `DONE` tasks to `.agent/archive/tasks_archive.jsonl`.
- Keeps the active list clean for distributed agents.

---

## Phase A-0: Environment Context (Local)
**Applicable when**: Setting up a new machine, or switching active models.

Each Agent must configure their local context to align capacity with task requirements.

```powershell
# Windows (PowerShell)
./scripts/set_model.ps1 -ModelName "Flash"

# Mac/Linux (Bash)
./scripts/set_model.sh "Flash"
```

> [!NOTE]
> This generates `.agent/local/model_context.json`.
> This file is **gitignored** to prevent cross-machine conflicts.

## Phase A: Startup Handshake (開工握手)

```bash
# 1. 同步最新代碼 & 啟動 Heartbeat
git pull
python scripts/agent_heartbeat.py
```

### Model Tier 檢查 (v1.3 新增)

領取任務前，Agent 必須：
1. 檢查任務的 `model_tier` 要求
2. 比對自己的 `.agent_identity.json` 中的 `current_model_tier`
3. 若不符，**暫停並通知用戶**：
   ```
   ⚠️ 任務 [task-id] 要求 tier-[N] 模型
   當前模型: tier-[M]
   建議: 請切換至 [建議模型] 後繼續
   ```

---

## Phase B: Task Claiming (領取任務)

### 步驟 1: 尋找可領取任務

```python
# 篩選條件
task.status == "TODO"
task.role == "builder" (或 architect)
task.model_tier <= 我的當前模型強度 (Self-Assessment)
```

### 步驟 2: 領取 (兩階段鎖)

1. 更新 `AGENT_TASKS.json` 的 `status`, `assignee`, `heartbeat`。
2. `git add` & `git commit` & `git push`。

---

## Phase C: Working (工作中)

保持 `agent_heartbeat.py` 在背景執行即可。

### Session Log (v1.3 新增)

**強制執行**: 每次開始工作前，必須在 `.agent/sessions/[task-id].md` 簽到。這有助於多 Agent 協作時了解誰在活躍。

```markdown
## [Date] Session Start
- **Agent**: [Agent-Name]
- **Goal**: [本次工作目標]

## Progress Log

### HH:MM - [Action]
- 完成了什麼
- Commit: [hash]
```

---

## Phase D: Completion & Escalation

### 提交任務 (Builder)

### 提交任務 (Builder)

1. **建立 Handoff Ticket**:
   - 複製模板: `.agent/templates/review_request_template.md`
   - 建立檔案: `.agent/handoffs/[task-id]_review_request.md`
   - 填寫測試證據與變更清單。

2. **更新狀態**: 將 `AGENT_TASKS.json` 狀態改為 `REVIEW`。

3. **提交代碼**: `git commit` 包含 handoff ticket 檔案。

4. **通知用戶 (Mandatory)**:
   ```
   🎫 任務 [task-id] 已提交審查
   Handoff Ticket: .agent/handoffs/[task-id]_review_request.md
   建議: 請切換至 Architect (Tier-3) 讀取 Ticket 並進行審查。
   ```

> [!WARNING]
> **Builder 不可直接將任務標記為 DONE！**
> 必須經過 Architect 審查後才能標記完成。

### 審查任務 (Architect)
- **通過**: 改為 `DONE`。
- **失敗**: 
  - 改回 `TODO`
  - `try_count += 1`
  - 若 `try_count >= 2`，設定 `model_tier = "tier-2"`
  - 若 `try_count >= 4`，設定 `model_tier = "tier-3"`
  - 填寫 `last_error` 或 `feedback`

---

## 📊 Status Definitions (v1.3 更新)

| Status | 說明 |
|--------|------|
| `TODO` | 待領取 |
| `IN_PROGRESS` | 正在執行中 |
| `ACTIVE` | 正在編碼（最近 15 分鐘有 commit） |
| `IDLE` | 無動作但未超時（15-45 分鐘） |
| `STALE` | 超時警告（45-60 分鐘） |
| `REVIEW` | 完成待審核 |
| `DONE` | 已完成 |
| `BLOCKED` | 被依賴擋住 |
| `CONFLICT` | 有衝突需人工介入 |

---

## 🔧 Agent Configuration

在 `.agent_identity.json` 中配置你的預設能力：

```json
{
  "agent_id": "Agent-Home-Desktop",
  "current_model_tier": "tier-1",
  "capabilities": ["flutter", "test"]
}
```

---

## 🔒 Task Ownership (v1.3 新增)

參見 `/task_ownership` workflow 了解跨任務邊界規則。

核心原則：
- 不修改其他 Agent 鎖定的檔案
- Lint 修復需檢查檔案所有權
- 依賴性修改需記錄在 history
