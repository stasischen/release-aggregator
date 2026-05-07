# Video Library Route Brief

## Goal

Add a learner-facing video reference route without collapsing the Study video
flow into the Library reference system.

Video content is source material. The Library route should behave like a
reference browser for source evidence, transcript exploration, and dictionary
lookup. The Study route can continue to behave like a learning session entry
until the broader Study/source navigation model is redesigned.

This is a route and UI-scope brief only. Do not change lesson data format,
video atom schema, `content-ko`, or `content-pipeline` as part of this slice.

## Current State

Current frontend routes:

| Route | Behavior | Issue |
| --- | --- | --- |
| `/study/video` | Renders `VideoListScreen` | Study tab source path. |
| `/study/video/player` | Renders `VideoPlayerScreen` with `state.extra` video id | Not deep-linkable; fails if opened without extra. |
| `/video` | Redirects to `/study/video` | Legacy shorthand. |
| `/library/videos` | Not implemented | Library hub still sends video users to Study. |

Current screen behavior:

- `LibraryHubScreen` video card routes to `/study/video`.
- `VideoListScreen` title and copy are Study-oriented (`Video Learning`,
  `Pick your flavor`).
- `VideoListScreen` card taps always push `/study/video/player` with
  `state.extra`.
- `VideoPlayerScreen` can render a passed `videoId`, but router wiring does not
  expose `/library/videos/:videoId`.
- `SourceDetailScreen` source video CTA pushes `/study/video/player` with
  `state.extra`.

## Product Boundary

Use two route families with different meanings:

| Family | Route | Meaning |
| --- | --- | --- |
| Library reference | `/library/videos` | Browse video source references. |
| Library reference | `/library/videos/:videoId` | Deep-linkable source player with transcript, dictionary, and atom lookup. |
| Study source path | `/study/video` | Study tab entry for video learning. Keep initially. |
| Study source path | `/study/video/player` | Legacy player route. Keep as alias during migration. |

Do not redirect `/study/video` to `/library/videos` yet. A learner choosing
Study expects a session/source-learning flow, while a learner choosing Library
expects reference lookup and evidence browsing.

## Implementation Plan

### Slice 1: Deep-Linkable Library Video Routes

1. Add canonical routes under the Library shell:
   - `/library/videos`
   - `/library/videos/:videoId`
2. Change `/video` redirect target from `/study/video` to `/library/videos`.
3. Keep `/study/video` unchanged.
4. Keep `/study/video/player` working with `state.extra`, but add a safe
   fallback if extra is missing:
   - If route has no video id, return to `/study/video` or show a user-safe
     missing-video state.
5. Update `LibraryHubScreen` video card to push `/library/videos`.
6. Update `SourceDetailScreen` video source CTA to push
   `/library/videos/:videoId`.
7. Update `VideoListScreen` so card taps are route-aware:
   - From `/library/videos`, push `/library/videos/:videoId`.
   - From `/study/video`, keep pushing `/study/video/player` with `state.extra`
     until Study video flow is redesigned.

### Slice 2: Reference-Oriented Video List UI

Do after Slice 1 route correctness is validated.

`VideoListScreen` should support a reference mode when mounted under
`/library/videos`:

- Copy should describe source browsing and transcript lookup, not a lesson
  session.
- Cards should prioritize educational affordances:
  - target-language title
  - learner-language title/summary when available
  - level
  - source type/category
  - duration
  - transcript/atom coverage state if already available from runtime assets
- Do not show raw ids, internal lesson ids, atom ids, or pipeline terminology.
- Do not use counts as primary value unless the count maps to an action the
  learner understands, such as transcript lines or saved moments.

### Slice 3: Study Video Flow Decision

Do not start until after Library `/library/videos` QA.

Decide whether Study video should:

- remain a separate source-learning flow,
- route into modular lesson runtime,
- route into a future content/source session shell,
- or become an alias to the Library player.

This decision belongs with the broader content/source/lesson architecture, not
with the Library reference migration.

## Route Acceptance Rules

- `/library/videos` must render `VideoListScreen`.
- `/library/videos/:videoId` must render `VideoPlayerScreen(videoId: videoId)`
  without requiring `state.extra`.
- `/video` must redirect to `/library/videos`.
- `/study/video` must still render `VideoListScreen`.
- `/study/video/player` must not crash if opened without `state.extra`.
- Library hub video card must use `/library/videos`.
- Source detail video CTA must use `/library/videos/:videoId`.
- No user-facing Library link should push `/study/video/player`.

## Tests

Update or add:

- `test/core/router/library_canonical_routes_test.dart`
  - assert `/library/videos` path is canonical.
  - assert `/library/videos/:videoId` path is canonical and deep-linkable.
  - assert `/video` redirects to `/library/videos`.
- `test/features/video/presentation/screens/video_list_screen_test.dart`
  - existing Study route tap keeps `/study/video/player` behavior.
  - new Library route tap pushes `/library/videos/:videoId`.
- `test/features/library/presentation/screens/library_hub_screen_test.dart`
  - video card stub route changes from `/study/video` to `/library/videos`.
- A small router regression test for `/study/video/player` without extra:
  - should not throw cast error.

## Non-Goals

- Do not redesign video player UI in this route slice.
- Do not change video atom package shape.
- Do not add or remove video content.
- Do not change lesson runtime contracts.
- Do not make `/study/video` redirect to Library until the Study/source flow is
  explicitly decided.

## Recommended Next Code Slice

Implement Slice 1 only.

This is safe because it:

- fixes deep-linkability for Library video references,
- preserves the existing Study route,
- removes `state.extra` from canonical Library player routes,
- and gives user QA a stable URL for video source browsing.
