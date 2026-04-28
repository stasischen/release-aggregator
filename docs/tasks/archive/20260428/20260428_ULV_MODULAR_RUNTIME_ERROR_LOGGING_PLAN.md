# Implementation Plan - Modular Lesson Runtime Detailed Error Logging

建立 Modular Lesson Runtime 的 Detailed Error Logging / 錯誤細節追蹤，讓 summary/result screen 能顯示更有診斷價值的資訊。

## User Review Required

> [!IMPORTANT]
> 本次變更將擴展 `PracticeEffortMetrics` 模型，並更新 `ModularSession.reportEffort` 的簽名。這將影響所有呼叫該方法的地方。
> 錯誤資料僅保存在記憶體（與 session 狀態綁定），且在 `replay` 時會被清除。

## Proposed Changes

### [Component] Presentation Models

#### [MODIFY] [practice_effort_metrics.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/models/practice_effort_metrics.dart)
- 新增 `errorCount` (int)
- 新增 `lastErrorCode` (String?)
- 新增 `lastErrorType` (String?)
- 新增 `lastErrorSample` (String?)
- 更新 `copyWith` 與建構子。

#### [MODIFY] [modular_lesson_result.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/models/modular_lesson_result.dart)
- 更新 `ModularNodeResult` 結構，加入錯誤相關欄位。
- 更新 `ModularLessonResult.aggregate` 邏輯，從 session 中提取錯誤資料。

---

### [Component] Providers

#### [MODIFY] [modular_runtime_provider.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/providers/modular_runtime_provider.dart)
- 更新 `ModularSession.reportEffort` 簽名，支援傳入錯誤欄位。
- 確保 `goToNode` (node transition) 時會封存當前 node 的狀態（既有邏輯已處理 duration，effort 資料原本就存在 Map 中）。
- 確保 `replay` 時會清除所有 metrics。

---

### [Component] Practice Renderers (Adapters)

#### [MODIFY] [ulv_typing_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_typing_renderer.dart)
- 在 `onEffort` 中回報打錯字等錯誤事件。

#### [MODIFY] [ulv_sentence_scramble_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_sentence_scramble_renderer.dart)
- 在 `onEffort` 中回報拼字錯誤。

#### [MODIFY] [ulv_speaking_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_speaking_renderer.dart)
- 在 `onEffort` 中回報語音辨識失敗、skip 或重試。

#### [MODIFY] [ulv_practice_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_practice_renderer.dart)
- 在 P1 (Chunk Assembly) 檢查答案錯誤時回報。

#### [MODIFY] [ulv_flashcard_review_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_flashcard_review_renderer.dart)
- 在 P2 (Flashcard) 評等為 'Again' 時回報最小摘要。

---

### [Component] Summary View

#### [MODIFY] [ulv_lesson_summary_view.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_lesson_summary_view.dart)
- 在 `_buildBreakdownList` 的 item 中顯示錯誤摘要（例如：`錯誤: 3`）。

## Verification Plan

### Automated Tests
- 執行 `test/features/study/presentation/providers/modular_runtime_stability_test.dart` 並新增錯誤追蹤測試。
- 新增 `test/features/study/presentation/models/practice_effort_metrics_test.dart` 驗證模型變更。
- 驗證 `replay` 是否正確清除錯誤資料。
- 驗證 `node transition` 不會導致錯誤資料污染。

### Manual Verification
- 進入 ULV Lesson，在練習節點故意出錯，最後在 Summary 頁面確認是否正確顯示錯誤次數與細節。
- 執行 Replay，確認 Summary 頁面重置。
