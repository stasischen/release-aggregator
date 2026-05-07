# Sources IA Brief

## Goal

Define a durable route and product boundary for source content before article
and dialogue viewers are added.

Sources are the primary learning material learners consume and inspect:

- video
- article
- dialogue

Library reference surfaces explain and index source content:

- knowledge
- sentences
- dictionary

Do not put source content under `/library`. The Library should remain a
reference layer, not a mixed content browser.

## Canonical Route Shape

Use typed source routes first:

```text
/sources
/sources/videos
/sources/videos/:videoId
/sources/articles
/sources/articles/:articleId
/sources/dialogues
/sources/dialogues/:dialogueId
```

Defer generic route aliases such as:

```text
/sources/:sourceType/:sourceId
```

until all source ids and source type names are stable across frontend runtime
artifacts. Typed routes are more explicit, easier to test, and less likely to
hide bad source ids behind a permissive router.

## Product Meaning

| Route family | Meaning | User expectation |
| --- | --- | --- |
| `/sources/*` | Consume and inspect real language content | Watch/read/listen, inspect transcript, tap words, open related knowledge. |
| `/library/knowledge*` | Understand reusable grammar/usage concepts | Search concepts, read explanations, inspect examples. |
| `/library/sentences*` | Inspect sentence examples and source evidence | Search sentences, break down chunks, open source context. |
| `/library/dictionary*` | Resolve words/atoms/entries | Search words, compare homographs, inspect senses/components/examples. |
| `/study*` | Guided learning/session flow | Follow lesson/path/practice sequence. |

## Navigation Rules

- Home/Study may recommend a source, but the URL remains `/sources/*`.
- Library may link to a source as evidence, but should not own source browsing
  routes.
- Sentence detail source evidence should link to the matching `/sources/*`
  viewer when a source viewer exists.
- Modular lesson runtime may embed source renderers directly; do not route out
  to `/sources/*` unless the learner intentionally opens source context.

## Source Viewer Contract

Each source viewer should expose the same learning operations where applicable:

- source title and metadata
- target-language content
- learner-language translation/i18n when available
- sentence/turn navigation
- atom or chunk breakdown
- dictionary lookup panel
- related knowledge links
- source position/deep link support

Do not expose:

- raw atom ids
- internal lesson ids
- pipeline terms
- technical POS composition fields
- unlocalized fallback strings

## Implementation Order

1. Video: already implemented as `/sources/videos*`.
2. Article: add `/sources/articles*` only after deciding whether the existing
   article viewer can render production article source artifacts without lesson
   runtime assumptions.
3. Dialogue: add `/sources/dialogues*` after confirming dialogue source ids and
   turn ids are emitted in the same source inventory as video/article.
4. Source hub: add `/sources` only when at least two source types have usable
   browse screens. Until then, direct links to `/sources/videos` are enough.

## Tests

For each source type:

- route smoke: list route resolves
- route smoke: detail route resolves from path param only
- no route requires `state.extra`
- source evidence links use `/sources/*`
- no production link uses old `/study/<source>` or `/library/<source>` routes

## Non-Goals

- Do not change content schema in this frontend UI task.
- Do not merge Study lesson runtime with Sources.
- Do not add generic `/sources/:sourceType/:sourceId` before typed routes are
  proven.
- Do not make Library a content source browser.
