# KO Learning Source Mockup: `79Pwq7MTUPE`

## Goal
Use one existing `content-ko` video source as a concrete mockup for the app-side architecture discussion, without requiring token-level dialogue decomposition.

This mockup is sentence-first:
- reuse existing `content-ko` video sentences and zh-TW translations
- layer reusable grammar/pattern/connector knowledge on top
- defer token-level dictionary tapping to a later iteration

## Source Inputs
- Video core: [/Users/ywchen/Dev/lingo/content-ko/content/core/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json](/Users/ywchen/Dev/lingo/content-ko/content/core/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json)
- Video zh-TW: [/Users/ywchen/Dev/lingo/content-ko/content/i18n/zh_tw/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json](/Users/ywchen/Dev/lingo/content-ko/content/i18n/zh_tw/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json)
- Mockup JSON: [docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.json](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.json)

## What This Mockup Proves
- A source can remain the top-level learning object.
- Reusable knowledge items can live outside the source and be linked by sentence ID.
- Existing curriculum reports can serve as the source for a normalized grammar/pattern library.
- The app can support `main focus`, `hide familiar`, `boost for review`, and `shadowing` before token-level atom mapping is available.

## Proposed App Data Layers
1. `SourceSentenceLayer`
- sourced from `content-ko`
- fields: sentence text, translation, timestamps, source type

2. `KnowledgeLibraryLayer`
- sourced from normalized curriculum reports
- item kinds in this mockup:
  - `grammar_point`
  - `pattern_frame`
  - `connector_item`
  - `vocab_item`

3. `SourceKnowledgeLinkLayer`
- sentence ID -> knowledge item IDs
- this is the smallest new layer needed to power the product

4. `UserLearningState`
- hidden items
- boosted items
- shadowing completion

## Suggested First-Screen IA
1. Header
- source title, duration, channel, level estimate, theme tags

2. Primary Learning Focus
- show 4 to 6 boosted knowledge items first

3. Sentence Timeline
- Korean
- zh-TW
- time
- badges for linked grammar/pattern/connector items

4. Knowledge Panel
- tabs or stacked sections:
  - Grammar
  - Patterns
  - Connectors
  - Vocabulary

5. Shadowing
- sentence loop presets
- start with sentence-level repeat, not token-level interaction

## Architecture Notes
- Do not store full grammar explanations inside each source.
- Store one canonical knowledge item and attach many sentence/source refs to it.
- `pattern_frame` and `grammar_point` should remain separate types.
- `connector_item` should also stay separate; it behaves differently in UI and retrieval.
- `vocab_item` in this mockup is lightweight and sentence-linked only. It is not yet a replacement for the full dictionary layer.

## Why This Fits The Existing App Direction
- It preserves existing sentence + translation assets.
- It avoids blocking on tokenized dialogue examples.
- It creates a clean integration point for `lingo-curriculum-source/reports`.
- It supports reverse lookup later:
  - grammar -> which sources use it
  - pattern -> which sentences demonstrate it
  - connector -> which discourse contexts show it

## Next Step
If this shape looks right, the next artifact should be a normalized schema draft for:
- `knowledge_catalog.json`
- `source_knowledge_links.json`

That would let the app consume curriculum-source knowledge as a reusable library instead of treating each source as a standalone explanation bundle.
