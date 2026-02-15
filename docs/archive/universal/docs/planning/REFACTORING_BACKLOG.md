# 重構待辦清單 (Refactoring Backlog)

**建立日期**: 2026-01-21
**最後更新**: 2026-01-21

本文件列出經過深度程式碼審查後發現的所有重構項目，按優先級與複雜度排序。

---

## 📊 總覽 (Overview)

| 類別 | 數量 | 預估工時 |
| :--- | :--- | :--- |
| 🔴 高優先級 | 2 項 | 4-6 小時 |
| 🟡 中等優先級 | 4 項 | 6-8 小時 |
| 🟢 低優先級 | 4 項 | 2-4 小時 |

---

## 🔵 下一步行動 (Next Actions)

依據建議順序執行：

1. **H7**: Study Navigation 邏輯提取 (New)
2. **H8**: Mini-Game UI Kit 標準化 (Refined L4)
3. **L3**: DictionaryService 職責精簡
4. **L2**: 測試覆蓋率擴展

---

## 🔴 高優先級 (High Priority)

### H7. TeachingEventsListScreen 導航邏輯提取 (New)

- **檔案**: `lib/features/study/presentation/screens/teaching_events_list_screen.dart`
- **問題**: `_navigateToEvent` 超過 100 行，判斷邏輯複雜，難以測試。
- **建議**: 建立 `StudyNavigator` 服務處理 event 導航判斷。
- **預估工時**: 2 小時
- **狀態**: [x] 已處理 (2026-01-25)
- **成果**:
  - 建立 `StudyNavigator` 服務
  - 解耦 `TeachingEventsListScreen` 導航邏輯


### H8. Mini-Game UI Kit 建立與應用 (New)

- **目標**: 落實 L4 小遊戲標準化。
- **任務**: 
  - 建立 `MiniGameOptionCard` (取代各處自定義按鈕)
  - 建立 `MiniGameHeader` (顯示分數與關閉)
  - 在 `CafeSlangScreen` 與 `SinoNumbersScreen` 應用。
- **預估工時**: 3 小時
- **狀態**: [x] 已處理 (2026-01-25)
- **成果**:
  - 建立 Widget Kit: `MiniGameScaffold`, `MiniGameHeader`, `MiniGameOptionCard`
  - 重構 `CafeSlangScreen` 使用標準元件



### H1. DictionaryContent Widget 拆分

- **檔案**: `lib/features/dictionary/presentation/widgets/dictionary_content.dart`
- **行數**: 516 行 → 335 行 (-35%)
- **問題**:
  - `build()` 方法超過 380 行
  - 包含多個私有輔助方法 (`_buildBadge`, `_buildTagBadge` 等)
  - 難以測試與維護
- **建議**:
  - 拆分為: `DictionaryHeader`, `DictionaryTagList`, `DictionaryMeaningList`, `DictionaryActionRow`
- **預估工時**: 2-3 小時
- **狀態**: [x] 已處理 (2026-01-21)
- **成果**:
  - 建立 `DictionaryHeader` widget (125 lines)
  - 建立 `DictionaryBadgeRow` widget (125 lines)
  - 建立 `DictionaryMeaningSection` widget (75 lines)
  - DictionaryContent 減少 181 行程式碼

---

### H2. SpeakingChallengeScreen 拆分

- **檔案**: `lib/features/study/presentation/screens/games/speaking_challenge_screen.dart`
- **行數**: 618 行 → 334 行 (Phase A: -46%)
- **問題**:
  - 同時處理 STT 初始化、錄音邏輯、UI 渲染、結果反饋
  - 大量 `setState` 調用 (6 處)
- **建議**:
  - 建立 `SpeakingChallengeController` (Notifier)
  - 將 STT 邏輯抽離為專用方法
  - UI 層只負責渲染
- **預估工時**: 2-3 小時 (分階段)
- **狀態**: [~] Phase A 完成 (2026-01-21)
- **Phase A 成果** (UI Widget 提取):
  - 建立 `SpeakingErrorView` widget (33 lines)
  - 建立 `SpeakingPromptCard` widget (60 lines)
  - 建立 `SpeakingMicButton` widget (37 lines)
  - 建立 `SpeakingFeedbackPanel` widget (185 lines)
  - SpeakingChallengeScreen 減少 284 行程式碼
- **Phase B** (Controller 提取): 待處理

---

### H3. debugPrint 清理

- **位置**: 12 處生產程式碼
- **檔案列表**:
  - `dream_weaver_screen.dart` (3 處: 行 331, 360, ...)
  - `dream_audio_service.dart` (4 處: 行 18, 31, 36, 45)
  - `dashboard_screen.dart` (行 135)
  - `peep_composer.dart` (行 161)
  - `article_content_layout.dart` (行 160)
  - `standard_dialogue_adapter.dart` (行 74)
  - `content_report_bottom_sheet.dart` (行 124)
- **建議**: 全部替換為 `Logger.debug()` 或移除
- **預估工時**: 30 分鐘
- **狀態**: [x] 已處理 (2026-01-21)

---

### H4. EventOccurrenceScreen 拆分

- **檔案**: `lib/features/study/presentation/screens/event_occurrence_screen.dart`
- **行數**: 412 行
- **問題**:
  - 同時處理字典初始化、音效、小遊戲啟動、對話渲染
  - 19 個方法 (包括 9 個私有方法)
- **建議**:
  - 已有 `TurnNavigationController`，但仍有大量 UI 邏輯
  - 將 `_buildCharacter`, `_buildOptionsOverlay`, `_buildChoiceButton` 抽為獨立 Widget
  - 將小遊戲啟動邏輯移至 `GameLauncher` 工具類
- **預估工時**: 2 小時
- **狀態**: [x] 已處理 (2026-01-21)
- **成果**:
  - 建立 `EventCharacterDisplay` widget (55 lines)
  - 建立 `EventOptionsOverlay` widget (100 lines)
  - 建立 `GameLauncherUtils` utility (40 lines)
  - EventOccurrenceScreen 減少 182 行 (412 → 230, -44%)

---

### H5. SettingsScreen 拆分

- **檔案**: `lib/features/profile/presentation/settings_screen.dart`
- **行數**: 470 行 → 360 行 (-23%)
- **問題**:
  - 包含 13 個私有方法
  - 語言選擇邏輯與 UI 混合
- **建議**:
  - 將語言選擇器移至獨立 `LanguagePickerBottomSheet`
  - 將頭像區塊移至 `AvatarHeaderWidget`
  - 將 BGM 設定移至 `BgmSettingsTile`
- **預估工時**: 1.5 小時
- **狀態**: [x] 已處理 (2026-01-21)
- **成果**:
  - 建立 `AvatarHeader` widget (90 lines)
  - 建立 `LanguagePickerSheet` utility (150 lines)
  - SettingsScreen 減少 110 行程式碼

---

### H6. SttService 職責拆分

- **檔案**: `lib/core/services/stt_service.dart`
- **行數**: 339 行
- **問題**:
  - 同時處理權限、平台差異、錄音、相似度計算、反饋生成
- **建議**:
  - `SttPermissionHelper`: 權限檢查
  - `SttRecorder`: 錄音與轉錄
  - `SttFeedbackGenerator`: 根據分數生成回饋
- **預估工時**: 2-3 小時
- **狀態**: [x] 已處理 (2026-01-22)
- **成果**:
  - 建立 `lib/core/services/stt/` 模組化目錄
  - 成功將 `SttService` 轉為 Façade 模式，減少 75% 邏輯密度
  - 加入 `SttFeedbackGenerator` 單元測試並通過驗證

---

## 🟡 中等優先級 (Medium Priority)

### M1. VideoRepository 硬編碼數據外部化

- **檔案**: `lib/features/video/data/video_repository.dart`
- **行數**: 163 行
- **問題**:
  - `_videoMetadataRegistry` 靜態 Map 硬編碼影片元數據
  - 新增影片需修改 Dart 程式碼
- **建議**:
  - 移至 `assets/config/video_metadata.json`
  - 或建立 `VideoMetadataService` 從遠端獲取
- **預估工時**: 1 小時
- **狀態**: [x] 已處理 (2026-01-21)
- **成果**:
  - 建立 `assets/config/video_metadata.json`
  - `VideoRepository` 改為非同步載入
  - `VideoPlayerScreen` 支援非同步 metadata 初始化

---

### M2. DreamWeaverScreen 資料驅動化

- **檔案**: `lib/features/dream_weaver/screens/dream_weaver_screen.dart`
- **行數**: 444 行
- **問題**:
  - `_getPuzzleConfig()` 硬編碼拼圖邏輯
  - 技術 Spike 遺留的技術債
- **建議**:
  - 將 `PuzzleConfig` 移至 JSON 設定檔
  - 或整合 V5 Content Pipeline
- **預估工時**: 2-3 小時
- **狀態**: [x] 已處理 (2026-01-22)
- **成果**:
  - 建立 `PuzzleConfig` 模型與 JSON Schema
  - 遷移硬編碼數據至 `assets/config/dream_puzzle_configs.json`
  - 實作 `DreamPuzzleService` 支持動態載入

---

### M3. VideoPlayerScreen 邏輯抽離

- **檔案**: `lib/features/video/presentation/screens/video_player_screen.dart`
- **行數**: 304 行
- **問題**:
  - 8 處 `setState` 調用
  - UI 與播放邏輯混合
- **建議**:
  - 建立 `VideoPlayerNotifier`
  - 將字幕加載、時間軸同步、播放狀態管理移出 UI 層
- **預估工時**: 1.5 小時
- **狀態**: [x] 已處理 (2026-01-21)
- **成果**:
  - 建立 `VideoPlayerController` (POJO + `StateProvider`)
  - 建立 `VideoPlayerState` (Immutable)
  - VideoPlayerScreen 改為 `ConsumerWidget` 並移除所有 `setState`
  - 採用 Controller Pattern 分離邏輯與 UI

---

### M4. catch (e) 異常處理強化

- **數量**: 46 處
- **重災區**:
  - `dictionary_repository.dart`: 4 處
  - `stt_service.dart`: 4 處
  - `mini_game_audio_helper.dart`: 5 處
  - `game_content_generator.dart`: 3 處
  - `tts_service.dart`: 3 處
- **建議**:
  - 對於可預期錯誤，明確捕捉類型
  - 對於不可預期錯誤，加入 `Logger.error()` 並考慮錯誤上報
- **預估工時**: 2 小時
- **狀態**: [x] 已處理 (2026-01-22)
- **成果**:
  - 建立 `AppException` 標準化異常層級
  - 重構 Dictionary, TTS, STT 等核心服務的錯誤處理
  - 解決因異常類型不匹配導致的測試回歸問題

---

### M5. setState 遷移至 Notifier (分階段)

- **數量**: 60+ 處
- **優先處理**:
  1. `video_player_screen.dart`: 8 處
  2. `speaking_challenge_screen.dart`: 6 處 (與 H2 合併處理)
  3. `lingo_type_screen.dart`: 5 處
  4. `pattern_drill_screen.dart`: 3 處
- **建議**: 逐步遷移，每個 Screen 建立對應 Controller
- **預估工時**: 4-6 小時 (分多次)
- **狀態**: [~] 階段性完成 (2026-01-21: VideoPlayer; 2026-01-22: LingoType)

---

### M6. 語言設定硬編碼清理

- **檔案**: `lib/features/profile/presentation/settings_screen.dart`
- **問題**:
  - `_getLanguageName()` / `_getFlag()` 硬編碼語言名稱與旗幟
- **建議**:
  - 移至 `LanguageConfig` 或 `ui_strings.json`
- **預估工時**: 1 小時
- **狀態**: [x] 已處理 (2026-01-22)
- **成果**:
  - 建立 `TargetLanguage` 擴展屬性 (`flag`, `defaultName`)
  - 將所有語言本地化名稱移至 `ui_strings_*.json` 資產
  - 自動化腳本更新 8 個本地化檔案
  - 移除 `SettingsScreen` 與 `LanguagePickerSheet` 中的硬編碼邏輯

---

## 🟢 低優先級 (Low Priority)

### L1. Analyzer 警告清理

- **數量**: 24 issues
- **類型**:
  - `unnecessary_null_check_pattern`: 14 處
  - `avoid_print`: 10 處 (主要在測試檔案)
  - `asset_directory_does_not_exist`: 部分未建立的資產目錄
- **預估工時**: 30 分鐘
- **狀態**: [x] 已處理 (2026-01-21)

---

### L2. 測試覆蓋率擴展

- **已有測試**:
  - ✅ `SrsEngine` (100%)
  - ✅ `TurnNavigationController` (100%)
  - ✅ `DictionarySearchEngine`
- **建議新增**:
  - [ ] `SttService` (至少 `calculateSimilarity` 方法)
  - [ ] `DictionaryService` (核心查詢方法)
  - [ ] `VideoRepository` (`loadSubtitles` 方法)
  - [ ] `GameContentGenerator` (內容生成邏輯)
- **預估工時**: 4-6 小時
- **狀態**: [ ] 待處理

---

### L3. DictionaryService 職責精簡

- **檔案**: `lib/core/services/dictionary_service.dart`
- **行數**: 329 行
- **問題**:
  - `getSubtitleFromAtoms` 屬於視訊功能特定邏輯
  - `getTurnText` 屬於對話系統邏輯
- **建議**:
  - 將格式化邏輯移至 `SubtitleFormatter` 或 `AppUtils`
- **預估工時**: 1 小時
- **狀態**: [x] 已處理 (2026-01-25)
- **成果**:
  - 重構 DictionaryService 移除 Formatter 邏輯


---

### L4. 小遊戲 Screen 標準化

- **相關檔案**:
  - `cafe_slang_screen.dart`
  - `sino_numbers_screen.dart`
  - `typing_challenge_screen.dart`
  - `pattern_drill_screen.dart`
  - `lingo_type_screen.dart`
- **問題**: 各小遊戲 UI 結構不一致
- **建議**: 建立 `MiniGameScaffold` 統一外框樣式
- **預估工時**: 2 小時
- **狀態**: [ ] 待處理

---

## 📅 建議執行順序

| 階段 | 項目 | 理由 |
| :--- | :--- | :--- |
| **第一階段** | H3 (debugPrint) | 快速勝利，低風險 |
| **第一階段** | L1 (Analyzer) | 與 H3 同時處理 |
| **第二階段** | H1 (DictionaryContent) | 高可見度，影響使用者體驗 |
| **第二階段** | H5 (SettingsScreen) | 職責清晰，容易拆分 |
| **第三階段** | H2 (SpeakingChallenge) | 複雜度高，需仔細測試 |
| **第三階段** | H6 (SttService) | 可與 H2 同時處理 |
| **第四階段** | M1-M3 (Video/Dream) | 功能模組，獨立處理 |
| **第五階段** | M4-M5 (異常/setState) | 需全面審視，分批處理 |
| **最終階段** | L2-L4 (測試/標準化) | 長期維護目標 |

---

## 📝 處理記錄 (Processing Log)

| 日期 | 項目 | 處理狀態 | 負責人 | 備註 |
| :--- | :--- | :--- | :--- | :--- |
| 2026-01-21 | 文件建立 | ✅ 完成 | Agent | 初始審查結果 |
| 2026-01-21 | H3, L1 清理 | ✅ 完成 | Agent | 清除 debugPrint 與 null 斷言警告 |

---

**Last Updated**: 2026-01-22 02:45
