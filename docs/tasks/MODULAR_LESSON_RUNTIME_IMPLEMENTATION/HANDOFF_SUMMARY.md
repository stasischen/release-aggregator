# MODULAR_LESSON_RUNTIME_IMPLEMENTATION Handoff

## Status

Completed.

## Source Contract

Follow `MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF/CONTRACT_DECISION.md`.

## Implementation Boundaries

- Article uses `ArticleContentLayout` with a local frontend mapper.
- Support drawer remains immersive; canonical vocab support may reuse `UlvVocabDetailRenderer`.
- Video remains owned by `UlvVideoRenderer`.
- Modular routes remain internal/pilot.

## Validation Target

- Article runtime widget test.
- Support drawer/fallback tests.
- Video runtime smoke test.
- Route exposure guard test.
- `flutter analyze`.

## Implemented

- Added frontend-local `ArticlePayloadMapper`.
- Wired modular article nodes to existing `ArticleContentLayout`.
- Replaced article fail-soft placeholder with stable fallback for malformed payloads.
- Added shared `UlvFallbackWidget`.
- Routed canonical `kv.` vocab support to `UlvVocabDetailRenderer`.
- Kept `pattern` and `usage` as explicit unsupported stable fallbacks.
- Added video smoke coverage for fake player builder pass-through and existing callback wiring.
- Added route exposure guard for production lesson entry points.

## Validation Result

- `flutter test test/features/study/presentation/widgets/ulv/ulv_qa_regression_test.dart test/features/study/presentation/widgets/ulv/ulv_video_renderer_test.dart test/features/study/presentation/navigation_wiring_test.dart test/features/study/presentation/screens/modular_sentence_viewer_integration_test.dart` passed.
- `flutter test test/features/study/presentation/screens/modular_lesson_runtime_structure_test.dart test/features/study/presentation/widgets/ulv/ulv_qa_regression_test.dart test/features/study/presentation/widgets/ulv/ulv_video_renderer_test.dart test/features/study/presentation/navigation_wiring_test.dart` passed.
- `flutter analyze` passed.
