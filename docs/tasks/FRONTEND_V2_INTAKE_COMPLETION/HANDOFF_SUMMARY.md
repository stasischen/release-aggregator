# Handoff Summary

## 已完成

- Created execution plan and inventory for frontend v2 intake.
- Approved the study-owned `FrontendContentContractResolver` contract.
- Implemented first study resolver slice in `lingo-frontend-web`.
- Frontend commit: `563181ed feat: resolve study lessons from frontend contract`.
- Frontend commit: `5193205e feat: resolve event lessons from frontend contract`.
- Prior dictionary mapping v2 frontend commit remains baseline: `5abcc31c feat: load dictionary mapping v2 candidates`.

## 目前決策

- Resolver location: `lingo-frontend-web/lib/features/study/data/repositories/frontend_content_contract_resolver.dart`.
- `manifest.lessons[].path` is authoritative for study lesson body path when present.
- `files.study_discovery` is authoritative for study discovery.
- `modular_lessons.json` is no longer allowed as an independent truth source in `LessonRegistryRepository`.
- `StudyContentLocator` remains as compatibility fallback only.
- Dictionary, grammar, and learning-library are not included in this resolver slice.

## 重要上下文

- `LessonRegistryRepository` now loads manifest/study discovery through `FrontendContentContractResolver`.
- `LessonRegistryRepository` can refine discovery metadata with manifest-listed lesson body metadata.
- `EventRepository` now uses `FrontendContentContractResolver` for manifest lookup and fallback lesson body path loading.
- `I18nOverlayService`, `VideoRepository`, `ModularLessonRepository`, and seed repositories still have direct `StudyContentLocator` usage.
- The current `frontend-v2-intake-03` task is in progress, not complete, because those runtime call sites are not fully migrated.

## DeepSeek Model

- Recommended: pro for next decision/review, flash for grep inventory only.
- Reason: next slice touches runtime data loading and can break lesson/video display.
- If switching models, next step should use: `deepseek-v4-pro` for reviewing the remaining `StudyContentLocator` call-site migration plan.

## 相關檔案

- `lingo-frontend-web/lib/features/study/data/repositories/frontend_content_contract_resolver.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/lesson_registry_repository.dart`
- `lingo-frontend-web/test/features/study/data/repositories/lesson_registry_repository_test.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/event_repository.dart`
- `lingo-frontend-web/lib/core/services/i18n_overlay_service.dart`
- `lingo-frontend-web/lib/features/video/data/video_repository.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/modular_lesson_repository.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/projection_seed_repository.dart`

## 未解問題

- Whether `VideoRepository` should use manifest `path` for core video subtitle loading or keep video-specific path fallback.
- Whether `I18nOverlayService` should receive a resolver method for i18n overlays or stay as legacy compatibility for now.
- Which real Korean v2 production fixture should become the stable end-to-end validation target.
- Existing `test/repositories/event_repository_test.dart` uses `ko_l1_dialogue_a1_01`, which is not listed in current `assets/content/production/manifest.json`; update or retire that fixture before treating it as a regression signal.

## 下一步

1. Inventory remaining direct `StudyContentLocator` runtime call sites.
2. Decide whether `ModularLessonRepository` and projection seed repositories should share explicit resolver methods for `lesson_content.v1.json`, `p1_seed.v1.json`, and `p2_seed.v1.json`.
3. Update the stale `EventRepository` test fixture to a current manifest-listed asset or move event coverage to resolver-level tests.
4. Re-run targeted repository tests and `flutter analyze`.

## 不要重做 / 不要改的東西

- Do not redo dictionary mapping v2 intake unless dictionary review changes contract.
- Do not include Stitch UI or design-token work.
- Do not remove `StudyContentLocator` yet; it is still needed for fallback and unaffected call sites.
- Do not read raw `content-ko/content_v2` paths from Flutter runtime.

## Latest Validation

- Command: `flutter test test/features/study/data/repositories/lesson_registry_repository_test.dart test/core/asset_integrity_test.dart`
- Result: pass.
- Command: `flutter test test/features/study/data/repositories/lesson_registry_repository_test.dart test/core/asset_integrity_test.dart && flutter analyze`
- Result: pass.
- Command: `flutter test test/repositories/event_repository_test.dart`
- Result: fails because `ko_l1_dialogue_a1_01` is not present in the current production manifest.
- Command: `flutter test test/features/video/data/video_repository_test.dart test/features/study/presentation/screens/modular_lesson_runtime_screen_test.dart`
- Result: video repository tests passed; `modular_lesson_runtime_screen_test.dart` has unrelated existing UI failures around drawer/TextField/pumpAndSettle.
- Command: `flutter analyze`
- Result: pass.
