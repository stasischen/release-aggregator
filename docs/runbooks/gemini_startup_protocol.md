# Gemini Startup Protocol (開工協議)

## Goal
在每次 Session 開始時，快速釐清目標並載入相關協議，然後開始執行。

## Startup Sequence

### Step 1: 確認目標
問使用者：
```
今天要做什麼？請告訴我：
1. 目標 Repo（可多個）
2. 任務類型（新功能 / 修 Bug / 文件整理 / 內容匯入）
3. 是否有特定的 task_id
```

### Step 2: 載入協議
根據使用者回覆，載入相關的 Active Docs：

| 目標 Repo | 需要載入的文件 |
|---|---|
| **任何 Repo** | `docs/index.md`, `docs/guides/REPO_RESPONSIBILITIES.md` |
| `content-ko` | `docs/ops/stage_contract_matrix_ko.md` |
| `lingo-frontend-web` | `.agent/skills/flutter-coding-standards/SKILL.md` |
| `core-schema` | `docs/guides/DATA_MODEL_CONTRACTS.md` |

### Step 3: 輸出執行計畫
開工前，向使用者確認：
```yaml
objective: <目標描述>
touched_repos: [<repo list>]
active_docs_used: [<loaded docs>]
execution_plan: <簡要計畫>
```

## Boundary Rules
- **語言**: 使用**繁體中文 (Traditional Chinese)** 交流，除非使用者明確要求其他語言。
- **Worklog 規則**: 每個 Session 結束時，worklog 必須寫入 `release-aggregator/docs/worklogs/YYYY-MM-DD.md`（見收工協議）。
- **不要跨邊界**: 除非使用者明確要求，不要自動跳到其他 Repo 或 Stage。
- **Archive 唯讀**: `docs/archive/` 下的文件僅供參考比對，不可用為執行依據。
