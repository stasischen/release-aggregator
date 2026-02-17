# Gemini Startup Protocol (開工協議)

## Goal
在每次 Session 開始時，快速釐清目標並載入相關協議，然後開始執行。

> [!IMPORTANT]
> 若任務涉及多個 Repo、phase 拆分執行、或需嚴格 session 重開，必須走 GSD 模式並載入：
> `release-aggregator/docs/runbooks/gsd_multi_repo_workflow.md`

## Startup Sequence

### Step 0: 載入任務全景 (Task Discovery)

> [!IMPORTANT]
> 開工時**必須先讀取任務索引**，掌握全部進行中的任務。

// turbo
讀取任務索引（唯一入口，不要直接讀 JSON）：
```
view_file /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TASK_INDEX.md
```

讀完後，向使用者展示 **Active Tasks** 清單，詢問要做哪一個。
如果使用者選擇了特定任務，**再去讀取**對應的 `*_TASKS.json` 取得細節。

### Step 1: 確認目標
問使用者：
```
請問今天要做哪個任務？（可直接輸入編號或 task_id）
如果是全新任務，請告訴我目標 Repo 和任務類型。
```

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
active_docs_used: [<loaded docs>]
decomposition_check: <classic_stage 可填 n/a；gsd_phase 必填完整檢查>
execution_plan: <簡要計畫>
```

## Boundary Rules
- **語言**: 使用**繁體中文 (Traditional Chinese)** 交流，除非使用者明確要求其他語言。
- **Worklog 規則**: 每個 Session 結束時，worklog 必須寫入 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`（見收工協議）。
- **不要跨邊界**: 除非使用者明確要求，不要自動跳到其他 Repo 或 Stage。
- **Archive 唯讀**: `docs/archive/` 下的文件僅供參考比對，不可用為執行依據。
- **Task 全景**: 每次開工必須先列出 `docs/tasks/` 下的所有任務檔，不可只讀一個。
