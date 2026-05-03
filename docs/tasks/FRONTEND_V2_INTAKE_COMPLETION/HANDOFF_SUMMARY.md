# Handoff Summary

## 已完成

- Created execution plan and inventory for frontend v2 intake.
- Approved the study-owned `FrontendContentContractResolver` contract.
- Implemented first study resolver slice in `lingo-frontend-web`.
- Frontend commit: `563181ed feat: resolve study lessons from frontend contract`.
- Frontend commit: `5193205e feat: resolve event lessons from frontend contract`.
- Frontend commit: `01f6a399 feat: resolve modular study artifacts from contract`.
- Frontend commit: `dbdda4c5 feat: centralize video and overlay content paths`.
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
- `ModularLessonRepository` now uses `FrontendContentContractResolver.resolveLessonBodyPath()`.
- `ProjectionSeedRepository` now uses resolver-owned p1/p2 sibling artifact paths derived from manifest `path`.
- `VideoRepository` now resolves core video paths through `FrontendContentContractResolver.resolveVideoCorePath()`, preferring manifest `path` before video compatibility fallback.
- `I18nOverlayService` now resolves legacy core/i18n overlay paths through resolver-owned compatibility methods instead of calling `StudyContentLocator` directly.
- Remaining direct `StudyContentLocator` usage is limited to resolver compatibility fallback and the locator class itself.
- `frontend-v2-intake-03` is complete.

## DeepSeek Model

- Recommended: flash for first-pass dictionary/UI inventory, pro for adapter or UI contract decisions.
- Reason: study path coupling is now resolved; next tasks move into dictionary display semantics and real production validation.
- If switching models, next step should use: `deepseek-v4-flash` for inventory and `deepseek-v4-pro` before changing dictionary UI semantics.

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

- Which real Korean v2 production fixture should become the stable end-to-end validation target.
- Existing `test/repositories/event_repository_test.dart` uses `ko_l1_dialogue_a1_01`, which is not listed in current `assets/content/production/manifest.json`; update or retire that fixture before treating it as a regression signal.
- Dictionary thread handoff says no runtime contract shape change; frontend should keep `mapping_v2` primary and treat `mapping_v2` origin cache as required until the dictionary core-origin migration reaches its Phase 3 validation gate.

## 下一步

1. Start `frontend-v2-intake-04`: dictionary UI/domain alignment around `mapping_v2` candidate semantics.
2. Use dictionary handoff assumptions: candidate identity prefers `homograph_key`, `entry_no` is atom/candidate-local only, origin display prefers `entry_refs.origin` / `sense_refs.origin`.
3. Add real Korean v2 validation coverage after dictionary UI/domain behavior is settled.
4. Update the stale `EventRepository` test fixture to a current manifest-listed asset or move event coverage to resolver-level tests.

## 不要重做 / 不要改的東西

- Do not redo dictionary mapping v2 intake unless dictionary review changes contract.
- Do not include Stitch UI or design-token work.
- Do not remove `StudyContentLocator` yet; it is still needed for resolver-owned fallback.
- Do not read raw `content-ko/content_v2` paths from Flutter runtime.

## Latest Validation

- Command: `flutter test test/features/study/data/repositories/lesson_registry_repository_test.dart test/core/asset_integrity_test.dart && flutter analyze`
- Result: pass after modular artifact resolver slice.
- Command: `flutter test test/features/study/data/repositories/lesson_registry_repository_test.dart test/features/video/data/video_repository_test.dart test/core/asset_integrity_test.dart && flutter analyze`
- Result: pass after video and overlay path centralization.
- Command: `flutter test test/repositories/event_repository_test.dart`
- Result: fails because `ko_l1_dialogue_a1_01` is not present in the current production manifest.
- Command: `flutter test test/features/video/data/video_repository_test.dart test/features/study/presentation/screens/modular_lesson_runtime_screen_test.dart`
- Result: video repository tests passed; `modular_lesson_runtime_screen_test.dart` has unrelated existing UI failures around drawer/TextField/pumpAndSettle.
- Command: `flutter analyze`
- Result: pass.
