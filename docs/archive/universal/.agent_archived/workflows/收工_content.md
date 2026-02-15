---
description: Content Production Session End / 內容生產收工協議
---

# /收工_content (Content Session Wrap-up)

專注於內容生產與邏輯處理的收工流程。
Wrap-up procedure for Content Production.

## ✅ 1. 驗證與檢查 (Validation & Check)

### A. 語言與翻譯稽核 (Content Audit)
如果是內容變更，使用本地 LLM 進行自動化翻譯與稽核。
If content change, use Local LLM for automated translation and audit.

```bash
# Example for Korean (Modify as needed)
# python3 tools/v4/translate_dictionary.py ko --type core
```

### B. 內容完整性檢查 (Integrity Check)
```bash
# python3 lingostory_universal/manage_content.py validate {lang}
```

### C. 工具鏈與暫存腳本整理 (Toolchain Archival) 🛠️
**收工前檢查 `tools/temp_scripts/`**：
1. **歸檔**: 有價值的腳本移至 `tools/v5/`。
2. **清理**: 刪除一次性腳本。

## 📝 2. 文檔更新 (Documentation Update)

### A. 更新 task.md
標記完成任務，清理詳細項目至 work_log。

### B. 更新 implementation_plan.md
反映內容更動狀態。

### C. 建立 work_log/YYYY-MM-DD_session.md
記錄 `Completed`, `Future Tasks`, `Known Issues`。

## 📦 3. Git 提交與同步 (Commit & Sync)

```bash
git add .
git commit -m "feat/fix(content): [Update] Description"
git pull --rebase origin master
git push origin master
```

## 🎬 4. 結束會議 (End Session)
向使用者匯報進度並通知結束。
