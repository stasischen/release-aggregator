# DeepSeek Inventory

Task: `FRONTEND_V2_INTAKE_COMPLETION`
Date: 2026-05-04
Routing: `flash -> pro`

## Scope

Repos inspected:

- `lingo-frontend-web`
- `release-aggregator`
- `content-ko`

Primary question:

- Which frontend runtime surfaces still bypass `content_v2`-derived stable contracts or hardcode production package layout?

## Summary

The frontend now has a stronger dictionary mapping v2 intake after commit `5abcc31c` in `lingo-frontend-web`, but the broader frontend v2 intake is not complete.

Current state by surface:

| Surface | Current State | Risk | Disposition |
| :--- | :--- | :--- | :--- |
| Study lesson discovery | Mixed: `manifest.json`, `lesson_catalog.json`, hardcoded `modular_lessons.json` | high | fix next |
| Study lesson body loading | Hardcoded path construction through `StudyContentLocator` | high | fix next |
| Dictionary mapping | `mapping_v2.json` primary; candidate metadata preserved; `mapping.json` fallback | medium | keep, review later |
| Grammar notes | Uses `grammar_index.json` by global ID | low | keep |
| Learning Library / Sentence Bank | Uses artifact/index data source and tests | low | keep |
| PRG/frontend handoff | Prototype outputs and frontend target still need final contract verification | high | decide after study resolver |
| Real content validation | Some asset integrity exists; legacy helper still hardcodes old study paths | medium | fix after resolver |

## Pain-Point Inventory

### P1 — Study content locator hardcodes production package layout

Evidence:

- `lingo-frontend-web/lib/features/study/data/repositories/study_content_locator.dart:7`
- `corePath()` constructs `assets/content/production/packages/$lang/video/core/$lessonId.json`.
- `corePath()` constructs `assets/content/production/packages/$lang/core/$t/$baseFolder/$lessonId.json`.
- `i18nPath()` constructs `assets/content/production/packages/$lang/i18n/$formattedLocale/...`.
- `modularPath()` constructs `assets/content/production/packages/$lang/lessons/$lessonId/build/lesson_content.v1.json`.

Risk:

- UI-facing study runtime depends on physical bundle layout instead of a stable resolver contract.
- Any PRG output shape or package layout change can break lesson loading.

Recommended disposition:

- Fix next.
- Replace call sites with manifest-driven resolver.
- Keep `StudyContentLocator` only as a compatibility implementation detail, not the public study runtime boundary.

### P1 — Lesson registry has independent hardcoded modular truth source

Evidence:

- `lingo-frontend-web/lib/features/study/data/repositories/lesson_registry_repository.dart:20`
- `_productionManifestPath = assets/content/production/manifest.json`
- `_modularRegistryPath = assets/content/production/packages/ko/lessons/modular_lessons.json`
- `_loadModularMetadata()` hardcodes `assets/content/production/packages/ko/lessons/$normalizedId/build/lesson_content.v1.json`

Risk:

- `modular_lessons.json` can diverge from production `manifest.json`.
- Lesson metadata and lesson body path are discovered through different authorities.

Recommended disposition:

- Fix next.
- Use `manifest.lessons[].path` and `files.study_discovery` as primary.
- Treat `modular_lessons.json` as compatibility only if it is listed by manifest or explicitly allowed by GPT decision.

### P2 — ConfigLoader is manifest-based but still named legacy V4

Evidence:

- `lingo-frontend-web/lib/core/services/config_loader.dart:25`
- `loadUnifiedManifest()` loads `assets/content/production/manifest.json`.
- `loadStudyDiscovery()` resolves `files.study_discovery`.

Risk:

- The implementation is mostly useful, but naming and comments still call it Universal V4.
- Downstream may keep treating manifest as raw schema instead of a frontend contract.

Recommended disposition:

- Keep.
- Let the new resolver wrap this behavior rather than replacing it immediately.

### P2 — Dictionary runtime is partially complete after mapping v2 intake

Evidence:

- `lingo-frontend-web/lib/core/repositories/dictionary_repository.dart:113`
- `loadChunkMapping()` now loads `mapping_v2.json` as primary and falls back to `mapping.json`.
- `DictionaryMappingCandidate` preserves `homograph_key`, `entry_refs`, `sense_refs`, `origin`, and `row_origin`.
- `resolveSurfaceToCandidates()` exposes ordered candidate lists.

Risk:

- Dictionary still consumes packaged runtime assets, not raw `content_v2`.
- This is acceptable if package manifest is the stable frontend artifact.

Recommended disposition:

- Do not redo now.
- Keep dictionary as completed first slice unless dictionary review thread changes the contract.
- Remaining dictionary work should be compatibility/UI disambiguation, not source-truth cleanup.

### P2 — Legacy content validation helper hardcodes old study paths

Evidence:

- `lingo-frontend-web/test/helpers/content_test_helper.dart:19`
- Paths include `packages/$lang/yarn/$lessonId.json`, `packages/$lang/article/$lessonId.json`, `packages/$lang/core/lessons/$lessonId.json`, and `packages/$lang/core/$lessonId.json`.
- `loadChunkMapping()` in the helper parses `mapping_v2.json` but only returns atom IDs, not candidates.

Risk:

- Tests can pass while real study runtime contract remains wrong.
- Future mapping v2 candidate behavior is not represented in content helper tests.

Recommended disposition:

- Fix after study resolver contract.
- Real Korean v2 fixture validation should load through the same resolver path as app runtime.

### P3 — Grammar notes are already index-gated

Evidence:

- `lingo-frontend-web/lib/core/services/grammar_note_service.dart:17`
- Uses `assets/content/grammar/grammar_index.json`.
- Resolves global grammar ID to relative note path.

Risk:

- Low. It still has a physical base folder, but the public lookup is index-gated.

Recommended disposition:

- Keep.
- Include in resolver only if GPT wants a unified content resolver facade.

### P3 — Learning Library / Sentence Bank is the cleanest artifact boundary

Evidence:

- Asset tree includes `assets/content/production/artifacts/ko/core/*_index.json`.
- Tests exist for artifact learning-library data source, mapper, and verification.

Risk:

- Low for this task.

Recommended disposition:

- Do not change in next slice.
- Use as reference pattern for frontend-stable artifact intake.

### P1 — PRG/frontend handoff still needs final alignment

Evidence:

- `release-aggregator/staging/prototype_output/manifest.json`
- `release-aggregator/staging/prototype_output/lesson_catalog.json`
- `release-aggregator/staging/prototype_output/production_plan.json`
- Existing PRG review identified prototype output and production target questions.

Risk:

- Frontend resolver could target a contract PRG does not actually produce.

Recommended disposition:

- Decide after study resolver contract.
- PRG validation should assert the same manifest/catalog fields used by frontend resolver.

## Proposed Solutions

### Option A — Minimal FrontendContentContractResolver

Define one frontend resolver that owns:

- `loadManifest()`
- `loadStudyDiscovery()`
- `resolveLessonMetadata(lessonId)`
- `resolveLessonBodyPath(lessonId)`
- `resolveOverlayPath(lessonId, locale)` only if the manifest/catalog exposes it

Rules:

- Manifest-listed `lessons[].path` is primary for lesson body.
- `files.study_discovery` is primary for catalog/discovery.
- `StudyContentLocator` remains compatibility only.
- No Flutter runtime reads `content-ko/content_v2` raw paths.

Pros:

- Narrow enough for Codex.
- Directly fixes P1 study risks.
- Does not disturb dictionary/grammar/learning-library.

Cons:

- May need temporary dual-path behavior for video/core legacy lessons.

### Option B — Make StudyContentLocator manifest-aware

Keep current API but inject manifest lookup inside `StudyContentLocator`.

Pros:

- Smaller code movement.

Cons:

- Keeps a path builder as the conceptual boundary.
- More likely to preserve legacy coupling.

### Option C — Wait for PRG final production artifact

Defer frontend study changes until PRG production bundle is promoted.

Pros:

- Avoids building against prototype artifacts.

Cons:

- Blocks frontend cleanup.
- Current runtime remains fragile.

## Recommendation

Choose Option A.

Use GPT 5.5 to approve the exact resolver API before implementation. The next Codex slice should only target study discovery/body loading, not dictionary, grammar, or learning-library.

## Suggested Next Action

Create `GPT_DECISION.md` with this decision request:

1. Approve `FrontendContentContractResolver`.
2. Decide whether `manifest.lessons[].path` is authoritative for lesson body path.
3. Decide whether `modular_lessons.json` is allowed only when manifest-listed.
4. Decide how to handle legacy video/core/i18n fallback.

## Validation Notes

Recent frontend dictionary mapping v2 validation already passed in `lingo-frontend-web`:

- `flutter test test/core/repositories/dictionary_repository_test.dart test/services/dictionary_service_test.dart test/core/asset_integrity_test.dart`
- `flutter test test/dictionary_overlay_logic_test.dart test/widgets/immersive_dictionary_overlay_test.dart test/features/dictionary/presentation/widgets/dictionary_meaning_section_test.dart`
- `flutter analyze`

No new validation command was needed for this inventory-only doc update.
