# Implementation Plan - In-App Lesson Insights

Establish a deterministic, local-only learning insights system for the Modular Lesson Runtime. This system will derive actionable insights from session performance data (retries, errors, duration) and display them in the lesson summary screen.

## User Review Required

> [!IMPORTANT]
> - Insights are derived strictly from the **current session's memory**. Because `effortMetrics` (retries/errors) are not currently persisted in the database schema (as per constraints), these insights will be most accurate for continuous sessions. If the app is restarted, only duration-based insights (which are persisted) will remain for previously completed nodes.
> - No external analytics will be used; all calculations are local and deterministic.

## Proposed Changes

### `lingo-frontend-web`

#### [NEW] [lesson_insights.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/models/lesson_insights.dart)
- Create a pure data model with strict stability rules for restart scenarios:
    - **Struggle Spotlight (Effort-Based)**: 
        - Rule: Only identified if `retryCount > 0` or `errorCount > 0` for any node.
        - Priority: `Max Retries -> Max Errors`.
        - **Stability**: If effort data is missing (e.g., after restart), this insight returns `null` rather than falling back to duration.
    - **Time Spotlight (Duration-Based)**:
        - Rule: Identifies the node with the highest `duration`.
        - **Stability**: Always available as duration is persisted.
    - **Dominant Error Types**: Frequency of `lastErrorType` among nodes with `errorCount > 0`.
    - **Category Efficiency (Restart-Safe Averages)**:
        - **Retry Avg**: `Sum(retries) / Count(nodes with effort data available)`. Nodes missing effort data are **excluded** from the denominator to avoid artificial dilution.
        - **Duration Avg**: `Sum(duration) / Count(total nodes of type)`. All nodes are included since duration is persisted.

#### [MODIFY] [ulv_lesson_summary_view.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_lesson_summary_view.dart)
- Integrate `LessonInsights` into the summary screen.
- UI elements (Truthful & Explicit):
    - **"難點聚焦" (Struggle Spotlight)**: Only shown if effort data exists. Displays the specific node and the struggle type (e.g., "最多次重試").
    - **"耗時最久" (Time Spotlight)**: Always shown. Displays the node that took the most time.
    - **"類別分析" (Category Analysis)**: Displays the Accuracy vs Pace breakdown using the defined denominator rules.

## Verification Plan

### Automated Tests
- `test/features/study/presentation/models/lesson_insights_test.dart`: Unit tests for the derivation logic.
    - Verify correct identification of max retry/duration nodes.
    - Verify error distribution calculation.
    - Verify empty/missing data handling.
- `test/features/study/presentation/widgets/ulv/ulv_lesson_summary_view_test.dart`: Update or add widget tests.
    - Ensure insights section appears when data is present.
    - Ensure graceful fallback when no effort/duration data exists.

### Manual Verification
- Run a lesson, purposely making errors in specific nodes.
- Verify the summary screen correctly identifies those nodes as "Challenging".
- Verify duration tracking is reflected.
- Replay the lesson and ensure insights are reset.
