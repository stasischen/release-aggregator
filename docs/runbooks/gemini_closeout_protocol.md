# Gemini Closeout Protocol (收工協議)

## Goal

當使用者說「收工」時，Agent 必須完成以下三件事：

1. **提交所有變更** 到各個 touched repo。
2. **撰寫當日 Worklog** 到 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`。
3. **輸出收工報告** 供使用者確認。

若本次為 `gsd_phase` 模式，另外必須：
4. **回寫每個 touched repo 的 `STATE.md`**（已完成任務、blockers、next task）。
5. **同步 aggregator 任務狀態**（`docs/tasks/` 相關任務檔與索引）。

---

## Step 1: 提交變更

對每個在本次 Session 中修改過的 Repo 執行：

```bash
# // turbo
cd <repo_path>
git add .
git status  # 確認變更內容
git commit -m "<type>: <description>"
git push origin main
```

### Step 1.5: GSD State Sync (only for `gsd_phase`)
- 每個 touched repo 必須確認 `STATE.md` 已更新且納入 commit。
- 若 task 狀態改變（active -> completed / blocked），同步更新 aggregator 的任務檔與 `TASK_INDEX.md`。
- 若本次只完成部分 phase，需在 `STATE.md` 明確記錄尚未完成的 Task IDs。
- 若為 `release-aggregator` session，必須檢查 `docs/tasks/TASK_INDEX.md` 是否需要同步更新（active/completed 變更）。

## Step 2: 撰寫 Worklog

> [!CAUTION]
> **Worklog 必須且只能寫入 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`。**
> 絕對不能寫入各 Repo 本地的 docs/ 或其他位置。
> 每天只有一份 Worklog，如果該日已有 Worklog，則 **追加 (append)** 新的 Session 紀錄。

### ⚠️ 多 Agent 防覆蓋規則 (Anti-Overwrite Protocol)

多個 Agent 可能在同一天操作同一份 Worklog。如果不遵守以下規則，**後寫入的 Agent 會靜默覆蓋前一位 Agent 的紀錄**。

#### 必須遵守的 4 步安全寫入流程

```text
Step 2a: git pull          — 拉取最新版本，確保不會覆蓋其他 Agent 的提交
Step 2b: 讀取現有檔案      — 確認已有內容，決定追加位置
Step 2c: 追加寫入          — 只在末尾追加，絕不覆蓋
Step 2d: 立即 commit+push  — 縮短衝突視窗
```

#### Step 2a: 先 Pull

```bash
# // turbo
cd d:\Githubs\lingo\release-aggregator
git pull origin main
```

#### Step 2b: 讀取現有檔案

```text
# // turbo
view_file release-aggregator/docs/worklogs/YYYY-MM-DD.md
```

- 如果檔案存在：記住最後一行的行號，用於追加。
- 如果檔案不存在：可以安全建立新檔案。

#### Step 2c: 追加寫入（安全工具選擇）

> [!WARNING]
> **禁止行為** (以下任何一項都會導致覆蓋)：
>
> - ❌ 使用 `write_to_file` 搭配 `Overwrite: true` 寫入已存在的 Worklog
> - ❌ 不先 `git pull` 就直接寫入
> - ❌ 不先讀取檔案就直接寫入
>
> **正確行為**：
>
> - ✅ 如果檔案已存在：使用 `replace_file_content` 或 `multi_replace_file_content`，在檔案末尾追加新的 Session 區塊
> - ✅ 如果檔案不存在：可以使用 `write_to_file`（此時 Overwrite 為 false）
> - ✅ 或者使用 shell 的 `cat >> file` 追加模式

#### Step 2d: 立即提交

```bash
# // turbo
cd d:\Githubs\lingo\release-aggregator
git add docs/worklogs/
git commit -m "worklog: YYYY-MM-DD session update"
git push origin main
```

### Worklog 格式

```markdown
# Daily Worklog - YYYY-MM-DD

## Session: <HH:MM> - <描述>

### Summary
- <本次 Session 的主要成果，1-3 行>

### Changed Repos
| Repo | Branch | Commit | Status |
|---|---|---|---|
| content-ko | main | abc1234 | done |
| release-aggregator | main | def5678 | done |

### Pending Decisions
- <如有未決事項列出>

### Blockers
- <如有 blocker，填原因與影響；若無填 none>

### Next Actions
1. <下一步行動>
```

### 追加規則

如果當天已存在 Worklog：

1. 在檔案末尾追加 `---` 分隔線。
2. 然後追加新的 `## Session:` 區塊。
3. **不要覆蓋已有內容。**
4. **不要重寫標題 `# Daily Worklog`**（它已經存在）。

### Step 2.5: Closeout Checklist（release-aggregator）
若本次 session 在 `release-aggregator` 執行，收工前必須逐項確認：
1. Worklog 已 append 到 `docs/worklogs/YYYY-MM-DD.md`（不可寫到其他位置）。
2. 本 phase touched repo 的 `STATE.md` 已同步（若本 repo 即 release-aggregator，檢查 `.planning/STATE.md`）。
3. 任務狀態若有變更，`docs/tasks/TASK_INDEX.md` 已同步。
4. 收工輸出包含 `blockers` 欄位（無則填 `none`）。

## Step 3: 輸出收工報告

向使用者展示簡明的收工摘要：

```yaml
task_id: <如有>
touched_repos: [content-ko, release-aggregator]
execution_mode: <classic_stage|gsd_phase>
commits:
  - repo: content-ko
    hash: abc1234
    message: "docs: update engine paths"
  - repo: release-aggregator
    hash: def5678
    message: "docs: update worklog"
worklog_path: docs/worklogs/2026-02-15.md
blockers: none
next_actions:
  - <待辦 1>
```

### Step 3.5: 下一階段交接輸出（Mandatory for phase workflow）
Agent 在每次流程結束時，必須額外輸出兩段：

1. `commit_reminder`
```yaml
commit_reminder:
  phase: <phase_id>
  repo: <repo_name>
  required_actions:
    - git add <phase_touched_paths>
    - git commit -m "<type>: <phase summary>"
    - git push origin <branch>
```

2. `next_phase_prompt`
```text
你在 <repo_path> 工作。請接續 GSD，執行 Phase <NEXT_PHASE_ID>（不要重做已完成 phase）。

先讀（順序固定）：
1) <repo>/SPEC.md
2) <repo>/PLAN.md
3) <repo>/STATE.md
4) <phase artifact files for NEXT_PHASE>

本次任務：
- 執行 /gsd:discuss-phase <NEXT_PHASE_ID> 或 /gsd:execute-phase <NEXT_PHASE_ID>（依 STATE.md 指示）
- 僅處理 <NEXT_PHASE scope>
- 完成後更新 STATE.md，回報變更檔案與驗證結果

限制：
- one-phase-one-repo
- docs/** 為 active protocol source
- docs/archive/** 只能參考，不可作為執行依據
```

若未輸出上述兩段，收工視為不完整。

## Step 4: 選擇性執行 Repo 專用檢查

根據 touched repo 執行對應的 closeout 子協議：

| Touched Repo | Closeout Sub-Protocol |
| :--- | :--- |
| `content-ko` | [closeout_content.md](closeout_content.md) |
| `lingo-frontend-web` | [closeout_frontend.md](closeout_frontend.md) |
| `content-pipeline` | [closeout_pipeline.md](closeout_pipeline.md) |
| `core-schema` | [closeout_schema.md](closeout_schema.md) |
| `release-aggregator` | [closeout_release.md](closeout_release.md) |

---

## Output Rules

- **永遠不要** claim 完成但沒有提供 commit hash 作為證據。
- **永遠不要** 把 worklog 寫到各 Repo 內部。
- 如果有未確定事項，寫進 Worklog 的 `Pending Decisions` 區塊。
- Worklog 區塊必須包含 `Blockers`（無則填 `none`）。
