# Canonical Library Route Migration Brief

## Goal

Move Library reference surfaces onto stable learner-facing routes after the
Stitch UI transfer is visually accepted, without reconnecting users to old
Knowledge Lab / Sentence Bank / video entry points or dev/testbed surfaces.

This is a routing brief only. Do not change lesson runtime contracts, content
schemas, `content-ko`, or `content-pipeline` as part of this migration.

## Current Route Inventory

Current working routes in `lingo-frontend-web`:

| Surface | Current working route | Screen | Status |
| --- | --- | --- | --- |
| Library hub | `/library` | `LibraryHubScreen` | Keep |
| Knowledge index | `/library/knowledge-lab` | `KnowledgeLabHomeScreen` | Legacy product name |
| Knowledge detail | `/library/knowledge-lab/item/:knowledgeId` | `KnowledgeItemDetailScreen` | Legacy product name |
| Knowledge topic | `/library/knowledge-lab/topic/:topicId` | `TopicDetailScreen` | Legacy product name |
| Vocab detail | `/library/knowledge-lab/vocab/:vocabId` | `VocabDetailScreen` | Legacy product name |
| Sentence index | `/library/sentence-bank` | `SentenceBankHomeScreen` | Legacy product name |
| Sentence detail | `/library/sentence-bank/sentence/:sentenceId` | `SentenceDetailScreen` | Legacy product name |
| Source detail | `/library/sentence-bank/source/:sourceId` | `SourceDetailScreen` | Legacy product name |
| Dictionary hub | `/library/dictionary?q=` | `StudyDictionaryHubScreen` | Keep hub route |
| Video list | `/study/video` | `VideoListScreen` | Study/source route |
| Video player | `/study/video/player` with `state.extra` video id | `VideoPlayerScreen` | Not deep-linkable |

Existing redirects:

| Legacy route | Current redirect |
| --- | --- |
| `/study/knowledge-lab` | `/library/knowledge-lab` |
| `/study/knowledge-lab/topic/:topicId` | `/library/knowledge-lab/topic/:topicId` |
| `/study/knowledge-lab/item/:knowledgeId` | `/library/knowledge-lab/item/:knowledgeId` |
| `/study/knowledge-lab/vocab/:vocabId` | `/library/knowledge-lab/vocab/:vocabId` |
| `/study/sentence-bank` | `/library/sentence-bank` |
| `/study/sentence-bank/source/:sourceId` | `/library/sentence-bank/source/:sourceId` |
| `/study/sentence-bank/sentence/:sentenceId` | `/library/sentence-bank/sentence/:sentenceId` |
| `/study/dictionary` | `/library/dictionary` |
| `/video` | `/study/video` |

## Canonical Route Target

Introduce these learner-facing routes:

| Canonical route | Target screen | Notes |
| --- | --- | --- |
| `/library/knowledge` | `KnowledgeLabHomeScreen` | Knowledge-First Lab index. Do not call it source/content home. |
| `/library/knowledge/item/:knowledgeId` | `KnowledgeItemDetailScreen` | Decode path parameter. |
| `/library/knowledge/topic/:topicId` | `TopicDetailScreen` | Keep only if topic surface remains useful after sparse-topic review. |
| `/library/knowledge/vocab/:vocabId` | `VocabDetailScreen` | Keep as secondary reference route. |
| `/library/sentences` | `SentenceBankHomeScreen` | Sentence reference index. |
| `/library/sentences/:sentenceId` | `SentenceDetailScreen` | Primary sentence microscope route. |
| `/library/sentences/source/:sourceId` | `SourceDetailScreen` | Source evidence route. |
| `/library/dictionary` | `StudyDictionaryHubScreen` | Search route with query support remains valid. |
| `/library/dictionary/entry/:entryId` | `StudyDictionaryHubScreen` or dedicated entry screen | Add only if entry-id initialization exists. Otherwise defer. |
| `/library/videos` | `VideoListScreen` | Library reference browse path for video sources. |
| `/library/videos/:videoId` | `VideoPlayerScreen` | Deep-linkable player route; do not require `state.extra`. |

## Redirect Policy

Use redirects for old product names and study aliases. The app is not launched,
so compatibility is for developer links and test stability, not public SEO.

| Old route | Redirect target |
| --- | --- |
| `/library/knowledge-lab` | `/library/knowledge` |
| `/library/knowledge-lab/item/:knowledgeId` | `/library/knowledge/item/:knowledgeId` |
| `/library/knowledge-lab/topic/:topicId` | `/library/knowledge/topic/:topicId` |
| `/library/knowledge-lab/vocab/:vocabId` | `/library/knowledge/vocab/:vocabId` |
| `/library/sentence-bank` | `/library/sentences` |
| `/library/sentence-bank/sentence/:sentenceId` | `/library/sentences/:sentenceId` |
| `/library/sentence-bank/source/:sourceId` | `/library/sentences/source/:sourceId` |
| `/study/knowledge-lab*` | canonical `/library/knowledge*` equivalents |
| `/study/sentence-bank*` | canonical `/library/sentences*` equivalents |
| `/study/dictionary` | `/library/dictionary` |
| `/study/video` | Keep as Study source browse route initially |
| `/study/video/player` | Keep as old route but allow `state.extra`; prefer `/library/videos/:videoId` for deep links |
| `/video` | `/library/videos` |

Do not redirect these into canonical Library routes:

| Route | Reason |
| --- | --- |
| `/dev/testbed` | Internal QA only. |
| `/study/modular-preview/:previewId` | Internal/pilot lesson preview. |
| `/study/modular-runtime/:lessonId` | Lesson runtime pilot; not a Library reference route. |
| `/study/article` | Content-first source viewer, not Knowledge/Sentence reference. |

## Navigation Copy Policy

User-facing navigation should keep the app-level tabs:

- Home
- Study
- Library
- Practice
- Profile

Do not import Stitch bottom-nav labels such as `Index`, `Workbench`, or
`Analytics`.

Library hub cards should route to canonical routes after migration:

| Card | Route |
| --- | --- |
| Knowledge Lab / Knowledge | `/library/knowledge` |
| Sentence Bank / Sentences | `/library/sentences` |
| Dictionary | `/library/dictionary` |
| Videos | `/library/videos` |

The UI copy may still say "Knowledge Lab" if that remains the product name, but
the path should be `/library/knowledge` to avoid old `knowledge-lab` coupling.

## Implementation Order

1. Add canonical nested `GoRoute`s under `/library`.
2. Convert existing `/library/knowledge-lab*` and `/library/sentence-bank*`
   routes into redirects to canonical routes.
3. Add `/library/videos` and `/library/videos/:videoId`.
4. Keep `/study/video` as a Study tab source path during the first migration.
   Update `VideoListScreen` card taps based on the current parent route:
   - from `/study/video`, preserve `/study/video/player` until Study source
     flow is redesigned;
   - from `/library/videos`, navigate to `/library/videos/:videoId`.
5. Update in-app links in Knowledge, Sentence, Dictionary, Library hub, and
   video widgets to canonical routes.
6. Add redirect tests for all legacy Library/Study aliases.
7. Add smoke tests that canonical routes instantiate the expected screens.
8. Only after user QA, consider removing dead route aliases. Until then, keep
   redirects cheap and explicit.

## Tests To Add Or Update

Add a route-focused widget test file, for example:

```text
test/core/router/library_canonical_routes_test.dart
```

Required assertions:

- `/library/knowledge` renders `KnowledgeLabHomeScreen`.
- `/library/knowledge/item/:knowledgeId` renders `KnowledgeItemDetailScreen`.
- `/library/sentences` renders `SentenceBankHomeScreen`.
- `/library/sentences/:sentenceId` renders `SentenceDetailScreen`.
- `/library/sentences/source/:sourceId` renders `SourceDetailScreen`.
- `/library/dictionary?q=...` renders `StudyDictionaryHubScreen` and preserves
  query initialization.
- `/library/videos` renders `VideoListScreen`.
- `/library/videos/:videoId` renders `VideoPlayerScreen` without requiring
  `state.extra`.
- Legacy `/library/knowledge-lab*` routes redirect to `/library/knowledge*`.
- Legacy `/library/sentence-bank*` routes redirect to `/library/sentences*`.
- `/dev/testbed`, `/study/modular-preview/:previewId`, and
  `/study/modular-runtime/:lessonId` do not redirect into Library.

Update existing route-sensitive tests:

- `test/features/library/presentation/screens/library_hub_screen_test.dart`
- `test/features/learning_library/presentation/screens/knowledge_to_sentence_navigation_test.dart`
- `test/features/learning_library/presentation/screens/knowledge_lab_home_screen_test.dart`
- `test/features/learning_library/presentation/screens/sentence_bank_home_screen_test.dart`
- `test/features/video/presentation/screens/video_list_screen_test.dart`

## Acceptance Gates

Before the route migration can be considered complete:

- `flutter analyze` passes.
- Route smoke tests pass for canonical routes and legacy redirects.
- Existing Knowledge/Sentence/Dictionary/Video targeted tests pass.
- Asset integrity tests still pass.
- No user-facing route sends learners to `/dev/testbed`,
  `/study/modular-preview`, or `/study/modular-runtime`.
- No canonical route requires `state.extra` for a deep-linkable content id.
- In-app links use canonical routes, not old `knowledge-lab` or
  `sentence-bank` paths.

## Deferred Decisions

- Whether `/library/dictionary/entry/:entryId` should open a dedicated entry
  detail screen or initialize `StudyDictionaryHubScreen` with a resolved entry.
  Do not add this route until the entry-id initialization contract is clear.
- Whether `/study/video` should eventually redirect to `/library/videos` or
  remain a Study source path. Video is content-first, so this should wait for
  the broader Study/source navigation design.
- Whether topic and vocab routes remain first-class if content density stays
  sparse. Keep redirects and screens for now.

## Non-Goals

- Do not change lesson data format.
- Do not merge lesson runtime routes into Library.
- Do not touch `content-ko` or `content-pipeline`.
- Do not rename content architecture layers.
- Do not remove working redirects until the final UI QA pass is accepted.
