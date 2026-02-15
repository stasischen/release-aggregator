---
description: Shift-Left Testing Workflow / 測試左移驗證工作流
---

# Shift-Left Testing (測試左移)

在部署到設備前，先透過靜態分析和單元測試驗證所有邏輯。
Verify all logic via static analysis and unit tests BEFORE deploying to device.

## 🛠️ 1. 核心流程 (Core Workflow)

1. **靜態分析 (Static Analysis)**: 確保代碼符合項目規範。
   ```bash
   flutter analyze
   ```
2. **單元測試 (Unit Testing)**: 針對業務邏輯編寫測試。
   ```bash
   flutter test
   ```
3. **組件測試 (Widget Testing)**: 測試 UI 狀態。

## ✅ 2. 優點 (Benefits)

- **早期發現開發錯誤** (Catch bugs early).
- **提高交付質量** (Improve delivery quality).
- **減少回歸風險** (Reduce regression risk).

---
**Last Updated**: 2026-01-06
