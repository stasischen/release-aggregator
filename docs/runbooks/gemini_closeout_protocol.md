# Gemini Closeout Protocol (收工協議)

## Goal
當使用者說「收工」時，Agent 必須完成以下三件事：
1. **提交所有變更** 到各個 touched repo。
2. **撰寫當日 Worklog** 到 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`。
3. **輸出收工報告** 供使用者確認。

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

## Step 2: 撰寫 Worklog

> [!CAUTION]
> **Worklog 必須且只能寫入 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`。**
> 絕對不能寫入各 Repo 本地的 docs/ 或其他位置。
> 每天只有一份 Worklog，如果該日已有 Worklog，則 **追加 (append)** 新的 Session 紀錄。

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

### Next Actions
1. <下一步行動>
```

### 追加規則
如果當天已存在 Worklog：
1. 在檔案末尾追加 `---` 分隔線。
2. 然後追加新的 `## Session:` 區塊。
3. **不要覆蓋已有內容**。

## Step 3: 輸出收工報告
向使用者展示簡明的收工摘要：
```yaml
task_id: <如有>
touched_repos: [content-ko, release-aggregator]
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

## Step 4: 選擇性執行 Repo 專用檢查
根據 touched repo 執行對應的 closeout 子協議：

| Touched Repo | Closeout Sub-Protocol |
|---|---|
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
