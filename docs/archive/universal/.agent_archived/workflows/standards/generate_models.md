---
description: Model Generation SOP / 模型生成標準程序 (build_runner)
---

# /generate_models - Code Generation Workflow / 程式碼生成工作流

## 🎯 Purpose / 目的
Ensure Freezed models and Riverpod providers are properly generated after any changes.
確保在任何修改後，Freezed 模型與 Riverpod Providers 都能正確生成。

## 📋 When to Use / 何時使用
- After modifying any file with `@freezed` or `@riverpod` annotations.
- After adding new model or provider files.
- When encountering "Undefined class" errors.

## 🔧 Steps / 步驟

### 1. Check for Modified Files (Optional)
```bash
git status
```
Look for changes in `lib/src/models/` or files with annotations.

### 2. Run Build Runner
// turbo
```bash
dart run build_runner build --delete-conflicting-outputs
```

### 3. Verify Generation
// turbo
```bash
flutter analyze
```
Expected: `No issues found!`

### 4. Run Tests
// turbo
```bash
flutter test
```

## ⚠️ Common Issues / 常見問題

| Issue / 問題 | Solution / 解決方案 |
|---|---|
| `Undefined class '$ModelCopyWith'` | Run build_runner again after a clean |
| Conflicting outputs | Use `--delete-conflicting-outputs` flag |
| Stale generated files | Delete `*.g.dart` and `*.freezed.dart`, then regenerate |

## 🧹 Full Clean Regeneration
// turbo
```bash
flutter clean
Get-ChildItem -Recurse -Filter "*.g.dart" | Remove-Item -Force
Get-ChildItem -Recurse -Filter "*.freezed.dart" | Remove-Item -Force
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```
