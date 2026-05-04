# MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF Decision

## Status

Reviewed and accepted as a contract brief. This document converts Gemini's read-only inventory into implementation boundaries.

## Corrections To Gemini Inventory

- Hardcoded summary/footer strings are already fixed in frontend commit `9fce7823`; they are not active scope.
- `ArticleContentLayout` exists and is a valid reuse target, but payload mapping must be kept local to the Flutter runtime until lesson schema is finalized.
- `UlvSupportPanelSwitcher` already supports canonical Knowledge Lab, source, topic, vocab, and sentence namespaces through drawer renderers or stable fallbacks. The gap is not "all support is missing"; the gap is that `pattern`, `usage`, and direct `vocab` support-surface enum paths still show placeholder UI.
- `UlvVideoRenderer` already owns `VideoPlayerScreen` in the modular runtime. The remaining video contract is fallback/validation and smoke coverage, not a full ownership rewrite.

## Accepted Contract Boundaries

### Article Surface

Decision: Use existing `ArticleContentLayout` inside `UlvPrimarySurfaceAdapter`.

Implementation boundary:

- Add a local `ArticlePayloadMapper` in frontend runtime code.
- Map current `ModularNode.payload` into `ArticleParagraph` without changing lesson schema.
- Support title, paragraphs, localized translations, atoms/chunks where present.
- If payload is malformed, show a stable runtime fallback component. Do not expose `"Fail-Soft: Article surface placeholder"` in product runtime.

Rejected for now:

- Redirecting modular article nodes to `/study/article`.
- Changing lesson JSON schema.
- Building a new article renderer from scratch.

### Support Surface

Decision: Keep support drawer immersive and reuse existing side-panel-safe renderers.

Implementation boundary:

- Treat `knowledge_lab` with canonical IDs (`top.`, `kg.`, `src.`, `kv.`, `ex.`) as the primary support contract.
- Route `vocab` support to the existing `UlvVocabDetailRenderer` when a canonical `kv.` ID is available.
- Do not build full-screen `KnowledgeItemDetailScreen` inside the drawer.
- Keep `pattern` and `usage` implementation gated until their canonical ID/data ownership is decided.
- Replace ad-hoc "coming soon" support placeholder with a stable fallback component that clearly distinguishes unsupported type from missing data.

Rejected for now:

- Navigating out of the lesson drawer for normal support usage.
- Creating lesson-local pattern/usage/vocab semantics that bypass existing domain data.

### Video Surface

Decision: Keep `UlvVideoRenderer` as the modular runtime owner of `VideoPlayerScreen`.

Implementation boundary:

- Preserve optional `videoPlayerBuilder` for tests/injection.
- Keep default `VideoPlayerScreen` path for production.
- Add smoke coverage proving a modular video node initializes the player and forwards anchor/support callbacks.
- Missing `videoId` should remain a stable fallback/validation failure, not a crash.

Rejected for now:

- External route-driven playback for modular video nodes.
- Replacing `UlvVideoRenderer` ownership with a separate route contract.

### Route Exposure

Decision: Keep modular runtime and preview routes internal/pilot until article and support gates pass.

Implementation boundary:

- `/study/modular-runtime/:lessonId` remains internal/pilot.
- `/study/modular-preview/:previewId` remains internal showcase/QA.
- `/dev/testbed` remains dev-only.
- Beta/Experimental labels remain acceptable while routes are internal.
- Production curriculum/path routing must not point to modular runtime until smoke gates pass.

## Smoke-Test Matrix

| Surface | Test | Fixture | Pass Condition |
| :--- | :--- | :--- | :--- |
| Article | `ulv_article_integration_test.dart` | `ModularNode(contentForm: article)` with paragraph payload | `ArticleContentLayout` renders title, paragraphs, translation toggle, and no fail-soft placeholder |
| Support vocab | `ulv_support_flow_test.dart` | active support type/id for canonical `kv.` item | Drawer renders `UlvVocabDetailRenderer` or stable not-found fallback without coming-soon copy |
| Support topic/knowledge/source | update existing support switcher tests | canonical `top.`, `kg.`, `src.` IDs | Correct side-panel renderer is selected |
| Support pattern/usage | `ulv_support_fallback_test.dart` | `pattern` / `usage` support type without approved canonical data contract | Stable unsupported fallback is shown; no product-coming-soon copy |
| Video | `ulv_video_playback_test.dart` | `ModularNode(contentForm: video)` with `videoId` and fake player builder | Player builder initializes; anchor/support callbacks update session state |
| Route exposure | `navigation_wiring_test.dart` | app route/nav setup | Normal production curriculum/path does not route to modular runtime yet |

## Implementation Task Split

### Task 1: Article Runtime Surface

- Add `ArticlePayloadMapper`.
- Wire article case in `UlvPrimarySurfaceAdapter`.
- Add article integration test.
- No schema/content changes.

### Task 2: Support Drawer Stabilization

- Add/standardize `UlvFallbackWidget` for unsupported/missing support states.
- Route direct `vocab` support through `UlvVocabDetailRenderer` when ID is canonical.
- Keep `pattern` and `usage` as explicit unsupported-stable fallbacks until ownership is decided.
- Add support flow/fallback tests.

### Task 3: Video Runtime Smoke Gate

- Add video runtime smoke test with fake player builder.
- Assert anchor/support callbacks update modular session state.
- Keep default `VideoPlayerScreen` ownership in `UlvVideoRenderer`.

### Task 4: Route Exposure Guard

- Add navigation test proving production curriculum/path routes do not enter modular runtime.
- Keep Beta/Experimental labels on internal routes.

## Deferred

- Pattern/usage semantic renderer ownership.
- Production curriculum route into modular runtime.
- Removing Beta/Experimental labels.
- Lesson schema changes.
- Content pipeline changes.
- Domain model unification.
