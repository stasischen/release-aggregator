# Handoff Notes: Unified Lesson View Flutter Transfer (ULVFT)

This document summarizes the state of the Unified Lesson View (ULV) implementation in Flutter following the completion of the `UNIFIED_LESSON_VIEW_FLUTTER_TRANSFER` task.

## 🏗️ Architecture: Master-Detail Shell

The core UI is implemented in `ModularLessonRuntimeShell`.
- **Wide Screens (> 800px)**: Side-by-side layout with a vertical divider. Primary content on the left, support panel on the right.
- **Narrow Screens (<= 800px)**: Primary content fills the screen. Support panels are accessed via an `endDrawer` (right-side drawer).
- **Navigation**: Integrated footer with "Previous", "Next", and "Complete" logic.

## 📺 Primary Surfaces (`UlvPrimarySurfaceAdapter`)

| Surface | State | Component | Notes |
| :--- | :--- | :--- | :--- |
| **Dialogue** | ✅ Production | `UlvSentenceAtomViewer` | Fully integrated with anchor selection and support requests. |
| **Video** | 🟡 Fail-Soft | `UlvVideoRenderer` | Functional renderer, awaiting final schema thread for advanced overlays. |
| **Article** | ❌ Placeholder | N/A | Currently shows a "Fail-Soft" placeholder widget. |

## 🛠️ Support Surfaces (`UlvSupportSurfaceAdapter`)

| Surface | State | Component | Notes |
| :--- | :--- | :--- | :--- |
| **Grammar** | ✅ Production | `UlvGrammarRenderer` | Standard detail view for grammar points. |
| **Knowledge Lab**| ✅ Production | `UlvSupportPanelSwitcher` | Dynamic router for Topic, Knowledge, Source, and Vocab details. |
| **Pattern** | ❌ Placeholder | N/A | Shows "Not yet implemented" fallback. |
| **Usage** | ❌ Placeholder | N/A | Shows "Not yet implemented" fallback. |
| **Vocab** | ❌ Placeholder | N/A | Shows "Not yet implemented" fallback. |

### Knowledge Lab Routing (`UlvSupportPanelSwitcher`)
- **Namespaces**: Supports `top.`, `kg.`, `src.`, `kv.` (canonical) and `T-`, `K-`, `S-` (legacy normalization).
- **Sentence Detail**: Currently shows a fallback noting that sentences are viewed in the full Library.

## 🧪 Testing & Validation

- **Layout Stability**: Verified via `modular_lesson_runtime_shell_test.dart` (Wide vs. Narrow screen behaviors).
- **Regression/Edge Cases**: Verified via `ulv_qa_regression_test.dart`.
    - Unknown `contentForm` fallback.
    - Unimplemented support surface fallback.
    - Missing `activeSupportId` handling.
    - Legacy ID normalization.
- **State Logic**: Partially covered by `modular_runtime_stability_test.dart` (selection/anchor logic).

## 🚩 Remaining Gaps & Next Steps

1.  **Article Surface**: Implement `UlvArticleRenderer` once the content contract is finalized.
2.  **Extended Support Surfaces**: Build out `Pattern`, `Usage`, and `Vocab` specific support adapters.
3.  **Video Overlays**: Transition `UlvVideoRenderer` from "Fail-Soft" to a rich interactive overlay system once the Batch D/E results are ready.
4.  **Sentence Support**: Decide if a lightweight "Sentence Support" panel is needed within the ULV or if the Library redirect is sufficient.

---
*Completed by Antigravity on 2026-04-27.*
