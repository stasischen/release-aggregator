# Gemini Startup Protocol (開工協議)

## Goal
在每次 Session 開始時，快速釐清目標並載入相關協議，然後開始執行。

> [!IMPORTANT]
> 若任務涉及多個 Repo、phase 拆分執行、或需嚴格 session 重開，必須走 GSD 模式並載入：
> `release-aggregator/docs/runbooks/gsd_multi_repo_workflow.md`

## Startup Sequence

### Step -1: Resolve Machine Identity

Before any task discovery, determine whether this session has a local machine claim file.

- Read the shared summary first: `release-aggregator/docs/tasks/MACHINE_STATUS.md`
- Then read the local claim file at `release-aggregator/docs/tasks/machines/local.json` if present on this machine
- If no local claim exists yet, create `local.json` before claiming a task

Purpose:
- Make the current machine explicit at session start.
- Prevent two computers from silently working the same task.
- Ensure the session knows its current ownership before reading tasks.
- Determine the machine role before deciding how much of the global index to load.

### Step 0: Select Operating Mode

Use the machine identity to choose one of two operating modes:

| Mode | Default machine | What it may read |
|---|---|---|
| `controller` | `m5pro` | `MACHINE_STATUS.md`, `TASK_INDEX.md`, all relevant handoffs/reviews, and any task docs needed to assign or review work |
| `worker` | all other machines | only `local.json`, its own task handoff, and the minimum docs required for the assigned task |

Rules:
- `m5pro` is the default controller unless its local claim explicitly says otherwise.
- Worker machines must not read the full `TASK_INDEX.md` unless the controller tells them to do so.
- Worker machines should not inspect other machines' task files or status rows.
- If `local.json` is missing a task assignment, ask the controller or the user for the task before reading broader indexes.

### Step 1: Controller Task Discovery

> [!IMPORTANT]
> 只有 `controller` mode 需要先讀取任務索引，掌握全部進行中的任務。

// turbo
讀取任務索引（唯一入口，不要直接讀 JSON）：
```
view_file <repo_root>/docs/tasks/TASK_INDEX.md
```

讀完後，向使用者展示 **Active Tasks** 清單，詢問要做哪一個。
如果使用者選擇了特定任務，**再去讀取**對應的 `*_TASKS.json` 取得細節。

### Step 1b: Worker Task Entry

Worker mode 不讀全局任務索引，直接依照本機 claim 進入 task。

- 先讀 `local.json`
- 再讀 `local.json` 中列出的 active docs
- 如果 `local.json` 已經包含 `current_task`，直接進入該 task 的 handoff / plan
- 如果 `local.json` 沒有 `current_task`，先向 controller 或使用者確認，不要自行掃全局索引

Worker mode 的目標是：
- 只處理自己的 task
- 不浪費 token 在全局任務盤點
- 不碰其他機器的狀態或文件

### Step 2: 載入協議
根據使用者回覆，載入相關的 Active Docs：

| 目標 Repo | 需要載入的文件 |
|---|---|
| **任何 Repo** | `release-aggregator/docs/index.md`, `release-aggregator/docs/guides/REPO_RESPONSIBILITIES.md` |
| **跨 Repo / phase-based 任務** | `release-aggregator/docs/runbooks/gsd_multi_repo_workflow.md` |
| `content-ko` | `release-aggregator/docs/ops/stage_contract_matrix_ko.md` |
| `lingo-frontend-web` | `.agent/skills/flutter-coding-standards/SKILL.md` |
| `core-schema` | `release-aggregator/docs/guides/DATA_MODEL_CONTRACTS.md` |
| `lllo` | `docs/SETUP_FOR_AGENT.md` |

### Step 2.5: 決定執行模式
在執行前必須先判斷模式：
- `classic_stage`: 單一 Repo、單一 stage 任務。
- `gsd_phase`: 多 Repo 編排、phase 任務、需要新 session 切換。

判斷規則：
- touched_repos > 1 -> `gsd_phase`
- 任務描述含「phase/wave/里程碑拆分」-> `gsd_phase`
- 其餘預設 `classic_stage`

### Step 2.6: `gsd_phase` 分解檢查（Mandatory）
若 `execution_mode = gsd_phase`，在任何 `/gsd:execute-phase` 前，必須先輸出以下檢查結果：

```yaml
decomposition_check:
  request_scope: <原始需求一句話>
  phase_id: <phase id>
  target_repo: <only one repo>
  touched_paths: [<repo-scoped paths>]
  dependency_prev_phase: <none|phase id>
  boundary_statement: "本 phase 僅修改 <target_repo>。"
```

若無法填出 `target_repo = single`，或 `touched_paths` 橫跨多 repo，必須停止執行並先拆 phase。

### Step 3: 輸出執行計畫
開工前，向使用者確認：
```yaml
objective: <目標描述>
task_id: <從 Step 0 選擇的 task_id，或 NEW>
touched_repos: [<repo list>]
execution_mode: <classic_stage|gsd_phase>
machine_mode: <controller|worker>
active_docs_used: [<loaded docs>]
decomposition_check: <classic_stage 可填 n/a；gsd_phase 必填完整檢查>
execution_plan: <簡要計畫>
```

### Step 4: Default Prompts

If the session needs an explicit prompt to continue, use one of the following:

**Controller prompt**
```text
你現在是 controller，machine_id = m5pro。

先讀：
1. <repo_root>/docs/tasks/MACHINE_STATUS.md
2. <repo_root>/docs/tasks/TASK_INDEX.md
3. 相關 handoff / review files

你的工作是：
- 分配 task
- 統整 worker 回報
- 安排 review
- 更新共享狀態
```

**Worker prompt**
```text
你現在是 worker，machine_id = <YOUR_MACHINE_ID>。

先讀：
1. <repo_root>/docs/tasks/machines/local.json
2. local.json 裡列出的 active docs
3. 只和該 task 相關的 handoff / plan

不要讀：
- <repo_root>/docs/tasks/TASK_INDEX.md
- <repo_root>/docs/tasks/MACHINE_STATUS.md
- 其他機器的文件

你的工作是：
- 只做自己的 task
- 做完產出 review packet / handoff note
- 更新自己的 local.json
```

## Boundary Rules
- **語言**: 使用**繁體中文 (Traditional Chinese)** 交流，除非使用者明確要求其他語言。
- **Worklog 規則**: 每個 Session 結束時，worklog 必須寫入 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`（見收工協議）。
- **不要跨邊界**: 除非使用者明確要求，不要自動跳到其他 Repo 或 Stage。
- **Archive 唯讀**: `docs/archive/` 下的文件僅供參考比對，不可用為執行依據。
- **Encoding 安全**: 撰寫 script 時嚴禁包含 Emoji 或特殊 Unicode 字元，以避免 Windows 環境下的 `UnicodeEncodeError`。
- **Task 全景**: 只有 `controller` mode 必須先列出 `docs/tasks/` 下的所有任務檔；`worker` mode 不要讀全局索引，避免浪費 token。
