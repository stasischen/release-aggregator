# Sync Content Workflow (同步內容工作流)

此工作流定義了如何將已完成的 V4 內容同步至 Flutter App。
This workflow defines how to sync finalized V4 content to the Flutter app.

## 🚀 1. 同步流程 (Sync Steps)

### A. 自動化指令 (Automated Commands)
執行預定義的腳本將 `production` 內容同步至 App 的 assets 目錄。
Run the predefined script to sync `production` content to the App's assets directory.

```bash
# Sync all finalized content
python3 tools/v4/v4_sync.py
```

### B. 常見路徑 (Common Paths)
- **Source (production)**: `lingostory_universal/content/production/`
- **Destination (App Assets)**: `lingourmet_universal/assets/content/production/`

## 🛠️ 2. 維護與更新 (Maintenance)

- **更新 ContentService**: 如果 JSON 結構有變動，請同步更新 Dart 中的 `ContentService` 或相關 Model。
- **清理舊快照**: 必要時手動清理 `lingourmet_universal/assets/content/` 下的舊資料。

---
**Last Updated**: 2026-01-11
