---
description: Feature Porting SOP / 功能移植標準程序
---

# /port_feature (移植功能)

從 Legacy 專案移植功能到 Universal 專案的標準程序。
Standard procedure for porting features from Legacy to Universal.

## 🔍 1. 此前提準備 (Preparation)

### A. 依賴分析 (Dependency Analysis)
檢查 Legacy 功能的依賴項（Service, Models, Widgets）。
Check dependencies of the legacy feature.

### B. 常見問題檢查 (Compatibility Check)
- **Freezed**: Universal 使用 3.x，需使用 `abstract class`。
- **TTS**: `TtsService.speak` 移除 `rate` 參數。
- **Logger**: `Logger.error` 使用命名參數。

## 🛠️ 2. 移植步驟 (Porting Steps)

### A. 模型層 (Models) [NEW]
優先移植模型，並執行 `build_runner`。
Port models first and run `build_runner`.

### B. 基礎設施 (Infrastructure)
確保所有共享 Widget 和工具類已就緒。
Ensure shared widgets and utils are available.

### C. 畫面層 (Screen) [MODIFY]
移植 UI 檔案並修復匯入與 API 不匹配問題。
Port UI files and fix imports/API mismatches.

## ✅ 3. 驗證 (Verification)

### A. 靜態分析 (Static Analysis)
確保移植檔案無錯誤。
Ensure no errors in ported files.

```bash
flutter analyze [path/to/ported/file]
```

---
**Last Updated**: 2026-01-06
