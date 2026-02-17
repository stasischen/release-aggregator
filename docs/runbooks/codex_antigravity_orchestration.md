# Codex <-> Antigravity Orchestration Protocol

## Goal
讓 `Codex` 專注在 `release-aggregator` 做規劃與驗證，讓多台電腦上的 `Antigravity` 只做執行；同時支援「一個任務拆多個 session」仍可穩定收斂。

## Roles

### Codex (Control Tower)
- 維護 task/phase 拆解、依賴、波次順序。
- 產出可執行封包（Execution Packet）。
- 收斂回報、判定是否進下一 wave 或回補修正。
- 更新 `docs/tasks/*`、`.planning/*`、`docs/worklogs/*`。

### Antigravity (Executor)
- 只執行單一 `plan_id`（或 Codex 指定的同 wave 多 plan）。
- 不擴 scope，不跨 repo。
- 可跨多 session 持續同一 plan。
- 在達到「完成門檻」或「阻塞門檻」時主動回報 Codex。

## End-to-End Flow

1. Codex 在 aggregator 拆 phase -> 拆 plan -> 標註 wave 與依賴。
2. Codex 發送 Execution Packet 到指定 Antigravity。
3. Antigravity 執行並定期回報 Progress Report。
4. Antigravity 在符合收斂條件時回報 Completion Candidate。
5. Codex 驗證並決策：
- `accept`: 標記 plan 完成，放行下一 plan/wave。
- `revise`: 要求小修（同 plan 繼續）。
- `split`: 拆出新 plan（scope 過大或偏移）。
- `block`: 記錄 blocker，回到規劃層處理依賴。

## Codex -> Antigravity: Execution Packet

每次下發必須完整提供以下欄位：

```yaml
execution_packet:
  task_id: <TASK_ID>
  phase_id: <phase number>
  wave_id: <W1|W2|...>
  plan_id: <phase-plan id>
  target_repo: <single repo>
  target_branch: <branch name>
  objective: <one-sentence outcome>
  scope_in:
    - <allowed file/path 1>
    - <allowed file/path 2>
  scope_out:
    - <explicitly forbidden area 1>
  dependencies:
    requires:
      - <plan_id or artifact>
    blocks:
      - <downstream plan_id>
  required_reads:
    - <abs path doc 1>
    - <abs path doc 2>
  required_commands:
    - <command 1>
    - <command 2>
  deliverables:
    - <file/artifact/report>
  done_criteria:
    - <checkable criterion 1>
    - <checkable criterion 2>
  test_gates:
    - <must-pass test/validator>
  report_format: progress_v1
```

## Antigravity -> Codex: Progress Report (session 可重複)

Antigravity 每個 session 結束或遇到事件時回報一次：

```yaml
progress_report_v1:
  task_id: <TASK_ID>
  phase_id: <phase>
  wave_id: <wave>
  plan_id: <plan>
  session_id: <machine+date+seq>
  status: <in_progress|completion_candidate|blocked|scope_risk>
  completion_ratio: <0-100>
  changed_files:
    - <path>
  commands_run:
    - <cmd + pass/fail>
  tests:
    passed:
      - <test name>
    failed:
      - <test name>
  deliverable_check:
    done:
      - <criterion id>
    remaining:
      - <criterion id>
  blockers:
    - <none or concrete blocker>
  risks:
    - <scope drift, flaky test, dependency missing...>
  proposed_next_action: <continue same plan|ask codex split|ready for verify>
  commit_ref: <hash or pending>
```

## 「差不多完成」判定規則（Antigravity 自主）

Antigravity 可以在多 session 中自行判斷何時回報 `completion_candidate`。

### Completion Candidate 條件（全部滿足）
- `completion_ratio >= 85`
- `done_criteria` 至少 80% 已滿足，且「核心驗收條件」全滿足
- `test_gates` 無 hard fail（可有非阻斷 warning）
- 無新增 scope（`scope_in` 外變更為 0，或已先經 Codex 批准）
- 有可審核提交（至少一個 commit hash，或清楚待提交差異）

### 不可宣告完成的情況
- 還有未解 blocker（依賴未到、測試 hard fail、資料契約不成立）
- 需要跨 repo 修改才能收斂
- 為了通過測試而臨時加入未批准範圍

### Blocked 門檻
任一條件成立就回報 `blocked`，暫停自行推進：
- 同一錯誤迭代 >= 3 次無進展
- 缺必要權限/資產/上游 artifact
- 預估剩餘工作超過原 plan 50%（表示應拆 plan）

## Codex Decision Matrix

收到 `completion_candidate` 後，Codex 用以下規則決策：

1. `accept`
- done criteria 與 test gate 均滿足。
- 標記 plan 完成，更新 `.planning/STATE.md`。

2. `revise`
- 僅剩局部問題（小修 < 30 分鐘）。
- 原 plan 不變，回傳精準修正項。

3. `split`
- 發現 scope 擴張或剩餘工作超過 1 個原子提交。
- 新增 `*-PLAN.md`，回傳新 packet。

4. `block`
- 依賴/契約未滿足。
- 在 task 與 worklog 記錄 blocker 與 owner。

## Session-Handoff Rule (多機/多次接力)

Antigravity 每次換機或重開 session 前，必須先貼「延續封包」：

```yaml
handoff_packet_v1:
  plan_id: <plan>
  latest_commit: <hash>
  current_status: <in_progress|completion_candidate|blocked>
  what_is_done:
    - <fact>
  what_remains:
    - <fact>
  exact_next_command:
    - <cmd>
  known_risks:
    - <risk>
```

沒有 `handoff_packet_v1` 不得直接接手執行。

## Executor Startup Guard (Mandatory)

Antigravity 每次「接到任務、準備開工」時，先做以下檢查：

1. 先在目標 repo 執行 `git pull`，再開始任何實作。
2. 若本地看不到指派的 task/plan/handoff 檔案，不可自行猜測補做。
3. 必須先回問使用者是否為：
- 本機尚未同步
- `release-aggregator` 尚未 push 最新任務
4. 在使用者確認同步策略前，停止進一步執行，避免錯版本開工。

## Minimal Operating Rhythm (Recommended)

1. Codex 只下發「一個 repo、一道 plan」到一台 Antigravity。
2. Antigravity 每完成一個小里程碑就回 `progress_report_v1`。
3. Codex 每回合只做一件事：`accept/revise/split/block`。
4. 進下一 wave 前，必須先完成上一 wave 全部 plan 的決策。

## Prompt Templates

### A) Codex 發給 Antigravity

```text
請執行以下 Execution Packet，僅限 scope_in 內操作，不可跨 repo。
若達到 completion candidate 條件，請用 progress_report_v1 回報。
若達到 blocked 門檻，立即回報 blocked 並停止擴 scope。

<貼上 execution_packet YAML>
```

### B) Antigravity 回報給 Codex

```text
以下是本次 session 的 progress_report_v1。
請回覆決策：accept / revise / split / block，並給下一步 packet。

<貼上 progress_report_v1 YAML>
```
