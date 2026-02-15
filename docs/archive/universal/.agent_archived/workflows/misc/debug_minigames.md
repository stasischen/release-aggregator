---
description: How to debug mini-games in the Flutter app / 如何調試 Flutter app 中的小遊戲
---

# Debug Mini-Games (小遊戲調試)

此指南說明如何調試與測試小遊戲（如 TypingChallenge, PatternDrill 等）。
This guide explains how to debug and test mini-games.

## 🔍 1. 常見問題與修復 (Common Issues & Fixes)

| Symptom / 症狀 | Cause / 原因 | Fix / 修復 |
| :--- | :--- | :--- |
| Game shows blank / 畫面空白 | Loading failed / 加載失敗 | Check data parsing & models / 檢查數據解析與模型 |
| Keyboard ignored / 鍵盤沒反應 | Not focused / 未聚焦 | Use `FocusNode.requestFocus()` |
| State not updating / 狀態未更新 | Riverpod issue | Use `ref.watch` or `ref.listen` |

## 🧪 2. 測試方式 (Testing Methods)

### A. 單元測試 (Unit Tests)
測試遊戲邏輯與狀態控制器。
Test game logic and state controllers.

```bash
flutter test test/games/pattern_drill_test.dart
```

### B. 視覺調試 (Visual Debugging)
使用 Flutter Inspector 檢查佈局邊界。
Use Flutter Inspector to check layout boundaries.

---
**Last Updated**: 2026-01-06
