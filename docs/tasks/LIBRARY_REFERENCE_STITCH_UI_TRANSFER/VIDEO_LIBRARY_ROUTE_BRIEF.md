# Video Source Route Brief

## Goal

Move video browsing and playback onto a canonical Source route family:

```text
/sources/videos
/sources/videos/:videoId
```

Video, article, and dialogue are source content. They are the material learners
consume and analyze. Knowledge, sentence, and dictionary pages are reference
surfaces that help learners understand those sources. The app should encode
that product hierarchy in the route structure instead of mixing video into the
Library reference layer.

The app is not launched, so do not preserve legacy video route compatibility in
this slice.

## Product Model

Use these route layers:

| Layer | Routes | Meaning |
| --- | --- | --- |
| Reference Library | `/library/knowledge`, `/library/sentences`, `/library/dictionary` | Reusable learning references. |
| Source Content | `/sources/videos`, `/sources/videos/:videoId` | Content learners consume, inspect, and cite. |
| Study Flow | `/study`, lesson/session/path routes | Guided learning flow that may recommend or launch source content later. |

Do not put video under `/library/videos`. That would make Library a mixed
reference/source bucket and will become worse once article and dialogue source
viewers are added.

## Canonical Video Flow

| Route | Screen | Behavior |
| --- | --- | --- |
| `/sources/videos` | `VideoListScreen` | Source browser for available videos. |
| `/sources/videos/:videoId` | `VideoPlayerScreen(videoId: videoId)` | Deep-linkable source viewer with transcript, atom lookup, dictionary panel, and related knowledge hooks. |

Deprecated routes to remove from user-facing router:

| Old route | New behavior |
| --- | --- |
| `/study/video` | Remove. Study should not own the video browser route. |
| `/study/video/player` | Remove. Player must not depend on `state.extra`. |
| `/video` | Remove instead of redirecting; app is not launched. |
| `/library/videos` | Do not add. |

## Navigation Rules

- Library hub video card should not exist as a primary Library reference card
  unless the product copy clearly frames it as "Source Content". Prefer a
  separate Source entry point.
- Study home may link to `/sources/videos` or a specific
  `/sources/videos/:videoId`, but the URL remains a Source route.
- `SourceDetailScreen` video CTA should push `/sources/videos/:videoId`.
- Internal modular runtime video surfaces may keep embedding `VideoPlayerScreen`
  directly; they should not route through `/sources/videos` unless the learner
  explicitly leaves the lesson context.

## UI Copy Direction

`VideoListScreen` should stop using study-session copy such as "Video Learning"
or "Pick your flavor".

Use source/reference language instead:

- "Video Sources"
- "Explore real Korean sources"
- "Open transcript"
- "Study words in context"

Cards should prioritize:

- target-language title
- learner-language title/summary when available
- level
- source category
- duration
- source origin/channel

Avoid:

- raw ids
- internal lesson ids
- atom ids
- pipeline terminology
- counts with no learner action attached

## Implementation Plan

### Slice 1: Route Correctness

1. Add top-level `/sources/videos` route for `VideoListScreen`.
2. Add top-level `/sources/videos/:videoId` route for
   `VideoPlayerScreen(videoId: decoded videoId)`.
3. Remove `/study/video`, `/study/video/player`, and `/video` from
   `app_router.dart`.
4. Update all production video links to `/sources/videos*`:
   - Library hub or Source entry card
   - Study home video entry
   - Source detail video CTA
5. Update `VideoListScreen` card tap to push `/sources/videos/:videoId`.
6. Update tests to assert canonical Source routes only. Do not add fallback
   tests for old video routes.

### Slice 2: Source Browser UI Copy

After route correctness, update `VideoListScreen` presentation so it reads like
a source browser, not a temporary study gallery.

This can be a small copy/layout pass; do not redesign the player yet.

### Slice 3: Broader Source IA

Open a separate task for:

```text
/sources/articles
/sources/articles/:articleId
/sources/dialogues
/sources/dialogues/:dialogueId
/sources/:sourceType/:sourceId
```

Do not combine this with the video route migration unless route and source id
contracts are already ready.

## Tests

Update or add:

- `test/core/router/source_canonical_routes_test.dart`
  - `/sources/videos` resolves as canonical path.
  - `/sources/videos/:videoId` resolves as canonical path and does not require
    `state.extra`.
  - old `/study/video`, `/study/video/player`, `/video`, and
    `/library/videos` are not part of the expected canonical contract.
- `test/features/video/presentation/screens/video_list_screen_test.dart`
  - card tap from `/sources/videos` opens `/sources/videos/:videoId`.
- `test/features/library/presentation/screens/library_hub_screen_test.dart`
  - update or remove video card assertion based on the chosen source entry
    placement.
- Source detail tests:
  - source video CTA opens `/sources/videos/:videoId`.

## Acceptance Gates

- `flutter analyze` passes.
- Targeted router/video/source tests pass.
- No production link pushes `/study/video`, `/study/video/player`, `/video`, or
  `/library/videos`.
- `/sources/videos/:videoId` works from path parameter only.
- Existing video player controller and atom/dictionary behavior remain
  unchanged.

## Non-Goals

- Do not change video atom package shape.
- Do not alter content pipeline or `content-ko`.
- Do not redesign modular lesson runtime.
- Do not add article/dialogue source routes in this slice.
- Do not preserve old video route fallbacks.
