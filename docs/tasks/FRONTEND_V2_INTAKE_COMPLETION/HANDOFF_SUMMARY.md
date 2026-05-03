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
- Frontend commit: `99a4b9e6 feat: prefer core dictionary origins`.
- Frontend commit: `e8972299 test: refresh event repository production fixture`.
- Frontend commit: `6b72ec1a test: add korean v2 production validation`.
- Aggregator commit: `c56ab0f fix: emit frontend-loadable PRG manifest paths`.

## 目前決策

- Resolver location: `lingo-frontend-web/lib/features/study/data/repositories/frontend_content_contract_resolver.dart`.
- `manifest.lessons[].path` is authoritative for study lesson body path when present.
- `files.study_discovery` is authoritative for study discovery.
- `modular_lessons.json` is no longer allowed as an independent truth source in `LessonRegistryRepository`.
- `StudyContentLocator` remains as compatibility fallback only.
- Dictionary, grammar, and learning-library are not included in this resolver slice.
- Dictionary origin precedence is now service-owned:
  1. `dictionary_core.entries[].origin`
  2. `mapping_v2.entry_refs.origin` / `sense_refs.origin`
  3. candidate `origin`
  4. `row_origin`
  5. legacy top-level core origin
- No-context multi-entry atoms do not arbitrarily choose `entries[0]`.

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
- `frontend-v2-intake-04` is complete.
- `frontend-v2-intake-05` is complete.
- `frontend-v2-intake-06` is complete.
- `FRONTEND_V2_INTAKE_COMPLETION` is complete.
- `EventRepository` now ignores empty overlay results and falls back to manifest-resolved atom loading.
- PRG prototype manifest output now converts global-manifest candidate paths into frontend-loadable asset keys under `assets/content/production/packages/{lang}/...`.
- PRG `production_plan.packaged_artifacts[].path` still preserves the original candidate/global-manifest path for provenance and staging traceability.

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

- Current real Korean production validation target is `ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson` for video core/i18n and event repository coverage.
- Dictionary thread handoff says no runtime contract shape change; frontend keeps `mapping_v2` primary and treats `mapping_v2` origin cache as fallback until the dictionary core-origin migration reaches its Phase 3 validation gate.

## 下一步

1. Review and merge frontend dictionary thread changes with the final frontend state.
2. Keep `mapping_v2` origin cache until Phase 3 validation proves frontend passes without it.
3. If PRG promotion resumes, run both PRG tests and frontend asset validation before deploying generated manifests.

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
- Command: `flutter test test/services/dictionary_service_test.dart test/core/repositories/dictionary_repository_test.dart test/core/asset_integrity_test.dart test/dictionary_overlay_logic_test.dart test/widgets/immersive_dictionary_overlay_test.dart test/features/dictionary/presentation/widgets/dictionary_meaning_section_test.dart`
- Result: pass after dictionary core origin join slice.
- Command: `flutter analyze`
- Result: pass after dictionary core origin join slice.
- Command: `flutter test test/repositories/event_repository_test.dart test/repositories/event_repository_integration_test.dart`
- Result: pass after replacing stale event fixture with a current manifest-listed production video lesson.
- Command: `flutter test test/core/korean_v2_production_validation_test.dart test/repositories/event_repository_test.dart test/repositories/event_repository_integration_test.dart && flutter analyze`
- Result: pass after real Korean v2 production validation slice.
- Command: `python -m unittest tests/test_prg_frontend_contract.py tests/test_prg_provenance_bridge.py tests/test_frontend_asset_bridge.py -v`
- Result: pass after PRG/frontend handoff path fix.
- Command: `python scripts/sync_frontend_assets.py --validate-only`
- Result: pass; invokes frontend `make validate-assets`, which passes `test/core/asset_integrity_test.dart`.
