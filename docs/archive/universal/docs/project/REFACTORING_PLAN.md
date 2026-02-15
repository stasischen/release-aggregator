# 程式碼品質與維護性重構計畫 V3 (App Logic & Coverage)

**建立日期**: 2026-01-23  
**前置作業**: [重構歷史記錄](file:///d:/Githubs/Lingourmet_universal/technical/archive/refactoring/REFACTORING_HISTORY.md) 已歸檔。

---

## 🔴 高優先級 (High Priority)

### 1. 擴展核心邏輯測試覆蓋率 ✅ DONE (2026-01-23)
**現況**: 許多核心邏輯 (如 `MiniGameStateController`, `VideoPlayerController`) 缺少單元測試。

**已完成**:
- [x] `VideoPlayerController` 初始化與成功流程測試
- [x] `MiniGameController` 狀態機與邊界測試 (7 個 test cases)
- [x] `DictionaryRepository` 快取優先與 Asset 備援測試
- [x] `AssetLoader` 基礎載入測試

**審查發現 (Follow-up Items)**:

| 檔案 | 建議改進 | 優先級 |
|------|---------|--------|
| `video_player_controller_test.dart` | 補充 Error Flow 測試與 `toggleTranslation` 等方法 | Low |
| `dictionary_repository_test.dart` | 補充 `loadChunkMapping` 與 OTA 路徑測試 | Low |
| `asset_loader_test.dart` | 移除 `listAssets` 測試中的 try-catch 或標記 skip | Low |

**預估工時**: 4 小時 (已完成) + 1.5 小時 (Follow-up)

---

### 2. 實作端到端 (E2E) 整合測試 ✅ DONE (2026-01-23)
**現況**: 缺乏跨模組的完整課程流程測試。

**已完成**:
- [x] 建立 `complete_lesson_flow_test.dart` (10 個測試案例)
- [x] 測試完整的學習流程：課程開始 → 對話導航 → 選項分支 → 小遊戲挑戰 → 課程總結
- [x] 涵蓋邊界情況：無效選項、END 標記、進度追蹤
- [x] 修復 `LessonFlowController.jumpToTurn` 的 bug（正確處理 minigame turns）

**預估工時**: 3 小時 (已完成)

---

## 🟡 中優先級 (Medium Priority)

### 3. 架構現代化：Mini-Game 遷移至 Riverpod (DONE)
**現況**: `MiniGameStateController` 是基於 `State<T>` 的 mixin + `setState()`，強制使用 `StatefulWidget`。

**已完成**:
- [x] 將 Mixin 轉化為 Riverpod `Notifier` 模式。
- [x] 支援 `ConsumerWidget` 直接調用，減少 UI 層模板代碼。
- [x] 統一狀態管理模式，提升可測試性。
- [x] 實作單元測試驗證狀態遷移邏輯 (SentenceScramble, PatternDrill)。

**審查發現 (Follow-up Items)**:

| 檔案 | 建議改進 | 優先級 |
|------|---------|--------|
| `cafe_slang_provider.dart` | 建立單元測試驗證 Timer 邏輯與分數計算 | Medium |
| `sino_numbers_provider.dart` | 建立單元測試驗證不同階段 (Practice/Speed) 轉換 | Medium |

**預估工時**: 3 小時 (已完成) + 2 小時 (Follow-up)

---

### 4. 實作 Golden Tests (視覺回歸測試)
**現況**: 缺少視覺回歸測試，UI 變更難以自動監測。

**建議**:
- 為核心 Widget 建立 Golden Tests (`MiniGameScaffold`, `SubtitleOverlay`, `EventDialogueBox`)。
- 使用 `/golden_test_guide` workflow 作為參考。
- 整合到 CI/CD 流程。

**預估工時**: 2 小時

---

## 🟢 低優先級 (Low Priority / Nice-to-Have)

### 5. VideoRepository 職責進一步拆解
**現況**: `VideoRepository` 目前負責 Asset 搜尋、JSON 解析、翻譯查找與字串切分。

**建議**:
- 提取 `SubtitleParser` 獨立 Service。
- 將文字切分邏輯進一步解耦。

**預估工時**: 1.5 小時

---

### 6. Provider 架構全量標準化
**現況**: 專案中仍混合使用 `StateNotifier`, `ChangeNotifier` 與現代的 `Notifier`。

**建議**:
- 統一遷移至 Riverpod 2.x `Notifier` / `AsyncNotifier`。
- 優先遷移 `learning_provider.dart`, `cafe_slang_provider.dart` 等。

**預估工時**: 2 小時

---

## 驗證計畫

| 變更 | 驗證方式 |
|------|---------|
| 測試覆蓋 | `flutter test --coverage` 核心模組 > 80% |
| Mini-Game 遷移 | 5 個內建小遊戲功能正常且測試通過 |
| Golden Tests | 生成 Baseline 並在 CI 通過回歸檢查 |
| Repository 拆解 | Subtitle 載入速度無下降且代碼行數減少 |

---

> [!IMPORTANT]
> 本計畫聚焦於 **提升 App 端代碼的可維護性** 與 **減少回歸風險**。
> 建議優先執行 Phase 1 的測試覆蓋擴展。
