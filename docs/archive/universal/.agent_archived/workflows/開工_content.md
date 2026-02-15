---
description: Content Production Session Start / 內容生產開工協議
---

# /開工_content (Content Session Start)

專注於內容生產與邏輯處理的新工作階段標準程序。
Standard procedure for starting a new Content Production session.

## ✅ 1. 環境檢查 (Environment Check)

### A. Git 狀態
確保工作區乾淨，並拉取最新遠端代碼。
Ensure clean workspace and pull latest remote changes.

```bash
// turbo
git status
git pull
```

### B. Meta-Brain (AI 大腦) 🧠
確保 Agent 技能庫已建立連結並更新。
Ensure Meta-Brain skills are linked and updated.

```bash
// turbo
ls -la .antigravity/
cat .antigravity/AGENT.md 2>/dev/null || cat ~/Dev/meta-brains/AGENT.md
```

### C. Python 環境與依賴 (Python Dependencies)
確認 Python 虛擬環境套件狀態，這是內容腳本運行的基礎。
Check Python venv package status for content scripts.

```bash
// turbo
# Windows: ./.venv/Scripts/pip list | Select-String -Pattern "pandas|openai|requests"
# Linux/MacOS: ./.venv/bin/pip list | grep -E "pandas|openai|requests"
./.venv/bin/pip list | grep -E "pandas|openai|requests"
```

## 📝 2. 任務規劃 (Task Planning)

### A. 閱讀內容核心文檔 (Core Content Docs)

必須閱讀以下文件以掌握專案狀態：
Must read the following documents:

- `.agent/workflows/universal_project_rules.md`
- `.agent/workflows/v5_content_pipeline.md` (內容開發必讀 / MUST READ for Content Dev)
- `docs/tech/universal/engineering/dictionary_schema_spec.md`
- `lingostory_universal/README.md`
- `TASK.md`

### B. Check Content Integrity (Optional)
若認為有必要，可執行內容完整性檢查。
Run content integrity check if deemed necessary.

```bash
# Optional
# Requires language code (e.g., thi, ko, de)
# python3 lingostory_universal/manage_content.py validate {lang}
```

## 🎬 3. 開始執行 (Execution)

在計畫獲得使用者核准後開始工作。
Start working after the plan is approved.
