# Modular Viewer Subtitle Runtime Brief

## Goal

Extend the modular viewer so it can read real subtitle-bearing source content for both `dialogue` and `video`, while staying inside the existing modular viewer architecture:

```text
source/build artifact
  -> adapter normalization
    -> subtitle segment model
      -> modular renderer / shell
        -> ULV support panel / anchor interaction
```

This is not a request to transplant the old `lllo` viewer wholesale. The target is to reuse proven subtitle interaction ideas while preserving the modular viewer's adapter + renderer split.

## Why This Exists

Current modular viewer already supports:

- source-build lesson fixtures under `docs/tasks/mockups/modular/data/curriculum-source`
- `dialogue` rendering via `dialogue_turns` / `dialogue_scenes`
- ULV runtime contract and panel-flow documents

What is still missing is a stable subtitle/runtime path that can:

- read dialogue turns as subtitle-like segments
- read real video source sentences with timestamps
- keep the same learner-facing interaction shape across dialogue and video
- feed sentence-level anchors into support/detail viewers

## Decision

Do not directly transplant `/Users/ywchen/Dev/lingo/lllo/tools/viewer.html`.

Use it only as reference for:

- sentence-level focus
- translation pairing
- dictionary / detail activation from sentence selection
- optional playback affordances

Do not import its Vue shell, monolithic lesson shape, or coupled dialogue/dictionary layout.

## Existing Sources To Reuse

### Modular Viewer Runtime

- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/adapter.js`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/app_v2.js`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/state.js`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/renderers/dialogue.js`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/renderers/core.js`

### ULV Contract / Gate

- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/UNIFIED_LESSON_VIEW_ARCHITECTURE.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/UNIFIED_LESSON_RUNTIME_CONTRACT.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/UNIFIED_LESSON_PANEL_FLOW.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/ULV_RUNTIME_MOCK_VERIFICATION.md`

### Real Video Evidence

- `/Users/ywchen/Dev/lingo/content-ko/content/core/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json`
- `/Users/ywchen/Dev/lingo/content-ko/content/i18n/zh_tw/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json`
- `/Users/ywchen/Dev/lingo/content-ko/content/core/learning_library/links/sources/src.ko.video.79Pwq7MTUPE.links.json`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.json`

### Old Viewer Reference Only

- `/Users/ywchen/Dev/lingo/lllo/tools/viewer.html`
- `/Users/ywchen/Dev/lingo/release-aggregator/tools/core_i18n_viewer/index.html`

## Target Runtime Model

Introduce one internal normalized model for subtitle-like primary content:

```json
{
  "surface_type": "dialogue|video",
  "segments": [
    {
      "segment_id": "stable id",
      "speaker": "optional speaker label",
      "ko": "target sentence",
      "translation": "resolved learner-facing translation",
      "start_ms": 0,
      "end_ms": 1900,
      "anchor_refs": ["knowledge or sentence refs"],
      "source_meta": {
        "node_id": "optional lesson node id",
        "scene_id": "optional scene id",
        "source_type": "dialogue|video"
      }
    }
  ]
}
```

Notes:

- `translation` is a runtime-resolved field, not a new upstream schema requirement.
- `start_ms` / `end_ms` are required for real video segments when available, optional for dialogue.
- `anchor_refs` may be empty; missing links must fail soft.

## Adapter Strategy

### Dialogue Input

Support:

- `payload.dialogue_turns`
- `payload.dialogue_scenes[].turns`

Normalize to subtitle segments by:

- preserving speaker when present
- resolving translation from `translations_i18n` or legacy `zh_tw` / `en`
- creating stable `segment_id`
- carrying scene metadata when present

### Video Input

Support real source content using:

- core video sentence list with timestamps
- i18n translation map keyed by sentence id
- optional links for sentence-level knowledge refs

Do not require a fully new lesson artifact just to test video rendering.

Instead, introduce an adapter path that can consume a real source-style video object and normalize it into the same segment model used by dialogue.

## Renderer Strategy

Do not create a second unrelated viewer shell.

Add or extend modular renderers so that:

- dialogue uses the normalized segment list instead of directly assuming `dialogue_turns`
- video also renders through a segment/timeline-aware view
- both support sentence selection, translation display, and TTS hooks

Suggested split:

1. shared subtitle/timeline rendering helper
2. dialogue wrapper renderer
3. video wrapper renderer

## UI Expectations

Dialogue and video should share:

- sentence/segment list
- selectable active segment
- translation visibility via existing learner prefs
- support-panel anchor activation

Video may additionally show:

- timestamp chip
- optional progress/timeline affordance

It should still fail soft into a readable sentence list if no media player is present.

## Interaction Contract

Segment selection must align with frozen ULV semantics:

- selected sentence maps to `activePrimaryAnchor`
- support views are driven by `activeSupportType`
- missing link data must not block primary reading/listening

Do not invent new global state names.

## What Not To Do

- do not transplant the old `lllo` Vue viewer shell
- do not invent a new upstream subtitle schema
- do not make Flutter-oriented abstractions here
- do not require real media playback to complete subtitle rendering
- do not rewrite unrelated KLab viewer behavior in the same slice

## Recommended Implementation Order

### Slice 1

Create a shared subtitle segment adapter for `dialogue`.

Acceptance:

- current lesson_01~03 dialogue nodes still render
- renderer uses normalized translation resolution
- no direct learner-facing dependency on raw legacy fields inside renderer body

### Slice 2

Add a `video` primary renderer fed by real `content-ko` source + i18n sample data.

Acceptance:

- one real video sample renders sentence list with timestamps
- translation resolves correctly
- no crash when media playback is absent

### Slice 3

Wire segment selection to support/detail anchors.

Acceptance:

- selecting a segment updates support context
- missing links show fail-soft state

## Verification

At minimum, implementation should let a reviewer manually test:

1. dialogue subtitle-like rendering from existing modular fixtures
2. one real video source rendered into segment/timestamp view
3. translation resolution via i18n-first fallback
4. segment selection without shell breakage
5. fail-soft behavior when no knowledge link or no media player is present

## Output Expectations For Gemini

Gemini should work in small slices, not one big rewrite.

For the first implementation round, it should:

- choose the smallest subtitle-runtime slice
- implement it
- provide exact local test instructions
- stop for review before expanding scope
