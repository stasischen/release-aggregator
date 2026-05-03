# Handoff Summary

## 已完成

- Created execution plan and inventory for frontend v2 intake.
- Approved the study-owned `FrontendContentContractResolver` contract.
- Implemented first study resolver slice in `lingo-frontend-web`.
- Frontend commit: `563181ed feat: resolve study lessons from frontend contract`.
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
- `EventRepository`, `I18nOverlayService`, `VideoRepository`, `ModularLessonRepository`, and seed repositories still have direct `StudyContentLocator` usage.
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

- Whether `EventRepository` should use the resolver for fallback atom path loading after `I18nOverlayService` fails.
- Whether `VideoRepository` should use manifest `path` for core video subtitle loading or keep video-specific path fallback.
- Whether `I18nOverlayService` should receive a resolver method for i18n overlays or stay as legacy compatibility for now.
- Which real Korean v2 production fixture should become the stable end-to-end validation target.

## 下一步

1. Inventory remaining direct `StudyContentLocator` runtime call sites.
2. Migrate `EventRepository` fallback loading to `FrontendContentContractResolver.resolveLessonBodyPath()`.
3. Add a targeted test proving manifest `path` wins over constructed study path.
4. Re-run targeted repository tests and `flutter analyze`.

## 不要重做 / 不要改的東西

- Do not redo dictionary mapping v2 intake unless dictionary review changes contract.
- Do not include Stitch UI or design-token work.
- Do not remove `StudyContentLocator` yet; it is still needed for fallback and unaffected call sites.
- Do not read raw `content-ko/content_v2` paths from Flutter runtime.

## Latest Validation

- Command: `flutter test test/features/study/data/repositories/lesson_registry_repository_test.dart test/core/asset_integrity_test.dart`
- Result: pass.
- Command: `flutter test test/features/video/data/video_repository_test.dart test/features/study/presentation/screens/modular_lesson_runtime_screen_test.dart`
- Result: video repository tests passed; `modular_lesson_runtime_screen_test.dart` has unrelated existing UI failures around drawer/TextField/pumpAndSettle.
- Command: `flutter analyze`
- Result: pass.
