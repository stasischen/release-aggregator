---
description: App Development Session Start / App 開發開工協議
---

# /開工_app (App Dev Session Start)

專注於 Flutter App 開發的新工作階段標準程序。
Standard procedure for starting a new Flutter App development session.

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

### C. App 依賴與分析 (App Dependencies)
確認 Flutter 依賴已安裝且無錯誤。
Ensure Flutter dependencies are installed and no errors.

```bash
// turbo
cd lingourmet_universal
flutter pub get
flutter analyze
```

## 📝 2. 任務規劃 (Task Planning)

### A. 閱讀開發核心文檔 (Core Dev Docs)

必須閱讀以下文件以掌握專案狀態：
Must read the following documents:

- `.agent/workflows/universal_project_rules.md`
- `technical/universal/engineering/coding_spec.md` (APP 開發必讀 / MUST READ for App Dev)
- `lingourmet_universal/README.md`
- `TASK.md`

### B. 更新計畫 (Update Plan)

確認 `task.md` 與 `implementation_plan.md` 與當前 App 開發目標一致。
Ensure `task.md` and `implementation_plan.md` align with App development goals.

## 🎬 3. 開始執行 (Execution)

在計畫獲得使用者核准後開始工作。
Start working after the plan is approved.
