---
description: App Development Session End / App 開發收工協議
---

# /收工_app (App Session Wrap-up)

專注於 Flutter App 開發的收工流程。
Wrap-up procedure for Flutter App development.

## ✅ 1. 驗證與檢查 (Validation & Check)

### A. 代碼分析 (Analyze)
確保代碼符合 Lint 規範且無錯誤。
Ensure code follows linting rules and has no errors.

```bash
// turbo
cd lingourmet_universal
flutter analyze
```

### B. 模型檢查 (Models)
確保所有 Freezed/Riverpod 模型已重新生成。
Ensure all Freezed/Riverpod models are regenerated.

```bash
// turbo
cd lingourmet_universal
dart run build_runner build --delete-conflicting-outputs
```

## 📝 2. 文檔更新 (Documentation Update)

### A. 更新 task.md (Task.md Update & Archival)
1. 標記完成的任務 `[x]`。
2. 將詳細項目移至 `work_log`。
3. 更新 `task.md` 僅保留高層級項目。

### B. 更新 implementation_plan.md
反映當前實作的最新狀態。

### C. 建立 work_log/YYYY-MM-DD_session.md
記錄 `Completed`, `Future Tasks`, `Known Issues`。

### D. 更新組件登記冊 (Optional)
如有新組件，更新 `lingourmet_universal/COMPONENTS.md`。

## 📦 3. Git 提交與同步 (Commit & Sync)

```bash
git add .
git commit -m "feat/fix(app): [Feature] Description"
git pull --rebase origin master
git push origin master
```

## 🎬 4. 結束會議 (End Session)
向使用者匯報進度並通知結束。
