---
description: How to implement Golden Tests for visual regression protection / 如何實作 Golden Tests 進行視覺回歸保護
---

# Golden Test Workflow / Golden Test 工作流

## 🎯 Purpose / 目的
Golden Tests capture screenshots of widgets and compare them against approved "golden" baseline images. Any visual change will cause the test to fail, providing a safety net against UI regressions.
Golden Tests 擷取 Widget 的截圖並與核可的「黃金標準」基準圖進行比對。任何視覺變化都會導致測試失敗，為 UI 回歸提供安全網。

## 📦 Prerequisites / 先決條件
1. Add dependencies to `pubspec.yaml`:
   ```yaml
   dev_dependencies:
     golden_toolkit: ^0.15.0
   ```
2. Run `flutter pub get`

## 🔧 Implementation Steps / 實作步驟

### 1. Create Golden Test File
Create a test file in `test/goldens/` (e.g., `test/goldens/immersive_overlay_golden_test.dart`).

### 2. Write Golden Test Structure
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';

void main() {
  testGoldens('ImmersiveDictionaryOverlay golden', (tester) async {
    await loadAppFonts();
    
    // Build your widget
    await tester.pumpWidgetBuilder(
      YourWidget(),
      surfaceSize: const Size(400, 600),
    );
    
    // Generate/compare golden
    await screenMatchesGolden(tester, 'overlay_standard');
  });
}
```

### 3. Generate Initial Baselines
// turbo
```bash
flutter test --update-goldens test/goldens/
```
This creates `.png` files in `test/goldens/` that become your baseline.

### 4. Run Golden Tests
```bash
flutter test test/goldens/
```
If images differ, the test fails with a visual diff report.

## ✅ Best Practices / 最佳實踐

| Do ✅ | Don't ❌ |
|-------|---------|
| Use fixed `surfaceSize` for consistency | Rely on platform-specific fonts |
| Load custom fonts with `loadAppFonts()` | Use random data in widgets |
| Run on same OS/Flutter version | Run across different CI environments without configuration |

## 🚀 When to Use / 何時使用
- **After UI is finalized**: Don't add Golden Tests during active UI development phase.
- **For critical UI components**: Premium overlays, brand-consistent layouts.
- **Before major refactors**: Lock in current behavior before changing structure.

## 📂 File Organization / 檔案組織
```
test/
├── goldens/
│   ├── immersive_overlay_golden_test.dart  (Test code)
│   └── goldens/                             (Generated images)
│       └── overlay_standard.png
├── services/
└── widgets/
```
