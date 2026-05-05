# Library Reference Stitch UI Transfer

## Goal

Transfer the Google Stitch reference designs into production Flutter Library
surfaces without regressing content correctness, multilingual readiness, or
light/dark mode readability.

The first design inventory lives in:

```text
/Users/ywchen/Dev/lingo/lingo-frontend-web/docs/stitch_designs
```

Current Stitch pages:

- `knowledge index.html`
- `knowledge detail.html`
- `sentence detail.html`
- `dictionary detail.html`
- `video player.html`

Theme/token transfer plan:

- [THEME_TOKEN_PLAN.md](THEME_TOKEN_PLAN.md)

Flutter component audit:

- [FLUTTER_COMPONENT_AUDIT.md](FLUTTER_COMPONENT_AUDIT.md)

Knowledge index reference-browser implementation brief:

- [KNOWLEDGE_INDEX_REFERENCE_BROWSER_BRIEF.md](KNOWLEDGE_INDEX_REFERENCE_BROWSER_BRIEF.md)

Architecture authority for the Knowledge index slice:

- `docs/guides/LEARNING_SOURCE_MULTILAYER_ARCHITECTURE.md`
- `docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md`
- `docs/guides/KNOWLEDGE_LAB_CONTENTKO_ARCHITECTURE.md`
- `docs/handoffs/2026-04-16_KG_PIPELINE_006_COURSE_RESTRUCTURE_NOTES.md`

## Product Boundary

This task covers the Library/reference learning product line:

- Knowledge Lab index and detail
- Sentence detail and sentence evidence surfaces
- Dictionary entry detail
- Video player learning overlay
- Shared reference components used by these pages

This task does not change lesson data format, `content-ko`, or
`content-pipeline` contracts unless a separate content brief is approved.

Knowledge Lab is a `Knowledge-First Lab` reference feature under the existing
Learning Source Multi-Layer Architecture. It must not be treated as the primary
Content-First Learning surface. Video, dialogue, article, story, and lesson
remain `source` types; Knowledge Lab may reverse-link to them, but should not
replace source-first content experiences.

## Implementation Authority

Stitch mockups are visual references, not product or content contracts. They may
invent content, route labels, hierarchy, examples, counts, images, or
interactions that do not match the real app.

When transferring a mockup, implementation authority is:

1. Real exported frontend artifacts and current repository contracts.
2. Teaching correctness and learner comprehension.
3. Smooth user flow across Knowledge, Sentences, Dictionary, and Video.
4. Existing app navigation and platform conventions.
5. Stitch visual direction.

If Stitch conflicts with real content or teaching flow, adapt or reject the
mockup detail. Do not force real data into an invented visual slot just because
the mockup contains it.

Every implementation slice must answer:

- Which real artifact fields power each visible section?
- What happens when an optional field is missing?
- Does the presentation help the learner understand the language point, or just
  mirror the mockup?
- Does the interaction path let the learner continue naturally to sentence,
  dictionary, source, or video context?
- Are labels and examples grounded in real content rather than placeholder
  sample data?

## Non-Negotiable Content Rules

User-facing UI must render educational content, not artifact mechanics.

- Artifact IDs such as `ex.ko.s.000002`, `kg.grammar.*`, `src.ko.*`, atom IDs,
  and package paths must not appear as body copy.
- Sentence refs must resolve to target-language sentence plus learner-language
  translation, or to a localized missing-content placeholder.
- Knowledge explanations must preserve prose meaning. Reference markers must not
  be inserted into prose in ways that read like natural language content.
- Tables containing example refs must render as semantic educational rows, not
  raw markdown tables with unresolved refs.
- Example lists must avoid duplication: examples rendered inline in the
  explanation should not reappear in the bottom related-examples section.
- Single-example groups should not show a numeric badge. Multi-example groups
  may show compact numbering.
- Dictionary displays must not expose raw technical POS compositions such as
  `v+e`, `n+p`, or resolver IDs as primary labels.
- Missing localized content must use localized UI strings, never hardcoded
  English fallbacks such as `[no meaning]`, `No definition`, or raw IDs.
- Stitch-invented examples, counts, levels, images, and labels must not replace
  artifact-backed content.
- Visual placeholders are acceptable only in empty/loading/error states and must
  be explicitly labeled as UI states, not content.

## Multilingual Readiness Rules

Use Korean and Traditional Chinese as current sample data only. The UI contract
must support many target languages and many learner UI languages.

- Labels should say target language / learner language conceptually, even when
  Korean samples are shown.
- Token breakdown must be optional and generic. Do not assume every language has
  Korean-style particles, endings, honorifics, or 받침 rules.
- Pronunciation or romanization lines must be optional.
- Layouts must tolerate long translations, non-Latin scripts, and right-to-left
  future languages where feasible.
- Route and component names may keep current app names, but user copy should not
  imply the product is Korean-only.

## Light / Dark Mode Rules

Stitch Tailwind palettes are reference only. Flutter implementation must derive
colors from app `ThemeData` / `ColorScheme`.

Required token layer:

- `LibrarySurface`
- `LibrarySurfaceRaised`
- `LibrarySurfaceInset`
- `LibraryBorder`
- `LibraryPrimaryText`
- `LibrarySecondaryText`
- `LibraryAccent`
- `LibraryAccentContainer`
- `EvidenceChipColor`
- `ExampleCardColor`
- `TokenChipColor`

Implementation may model these as helper methods/extensions rather than a new
design-token framework, but no page should hardcode light-only backgrounds.

Preferred implementation shape is a Library-specific Flutter
`ThemeExtension` such as `LibraryReferenceColors`, registered alongside the
existing app `SemanticColors`. This keeps Knowledge/Sentence/Dictionary/Video
tokens out of unrelated app surfaces.

## Accepted Design Direction

From Stitch, keep:

- Knowledge index cards with target form, learner title, short usage preview,
  level/kind/subcategory tags, and one resolved example sentence when available.
- Knowledge detail structure: hero, core meaning, semantic form/example rows,
  usage scenarios, comparison, related resources.
- Sentence microscope structure: sentence hero, token breakdown, related
  knowledge, source moment, similar sentences.
- Dictionary entry structure: homograph/sense groups, morphology, examples,
  related knowledge.
- Video player structure: current subtitle focus card, transcript, selected
  token dictionary panel.

## Rejected / Must Adapt

- Do not adopt Stitch bottom nav labels such as `Index`, `Analytics`,
  `Workbench`, or `Account`.
- Keep app navigation as `Home / Study / Library / Practice / Profile`.
- Do not depend on Stitch external generated image URLs.
- Do not copy Stitch Tailwind colors directly.
- Replace Korean-only copy such as `Atom Breakdown` with generic/localized copy
  such as `字詞拆解 / Token Breakdown`.
- Replace `N4 LEVEL` style labels with app artifact levels such as A1/A2 unless
  the content artifact explicitly provides JLPT-like levels for another target
  language.
- Do not use artifact counts, source counts, or example counts as the primary
  Knowledge index hero. Counts are QA/secondary metadata, not the learner's main
  decision signal.
- Do not rename the existing architecture into a new graph. Use `source`,
  `sentence`, `topic`, `knowledge_item`, `vocab_item`, `Content-First Learning`,
  and `Knowledge-First Lab` consistently.

## Route Policy

Short-term implementation should preserve current working routes:

```text
/library/knowledge-lab
/library/knowledge-lab/item/:knowledgeId
/library/knowledge-lab/topic/:topicId
/library/sentence-bank
/library/sentence-bank/sentence/:sentenceId
/library/sentence-bank/source/:sourceId
/library/dictionary
/study/video/player
```

Future canonical routes should be introduced with redirects after the UI is
stable:

```text
/library/knowledge
/library/knowledge/item/:knowledgeId
/library/knowledge/topic/:topicId
/library/sentences
/library/sentences/:sentenceId
/library/sentences/source/:sourceId
/library/dictionary/entry/:entryId
/library/videos/:videoId
```

## Component Plan

Shared components should be extracted before large page rewrites:

- `LibraryReferenceScaffold`
- `LibraryTopBar`
- `LibrarySearchBar`
- `EvidenceChip`
- `EvidenceCountRow`
- `TargetTextBlock`
- `LearnerTranslationBlock`
- `InlineExampleGroup`
- `SemanticExampleTable`
- `TokenBreakdownTile`
- `RelatedKnowledgeCard`
- `SourceMomentCard`
- `DictionarySenseCard`
- `VideoSubtitleFocusCard`

## Implementation Order

1. Sentence detail shared components and smoke coverage.
2. Knowledge detail renderer cleanup using semantic examples/tables.
3. Dictionary entry detail redesign.
4. Video player subtitle focus and dictionary panel redesign.
5. Knowledge index reference-browser redesign using
   [KNOWLEDGE_INDEX_REFERENCE_BROWSER_BRIEF.md](KNOWLEDGE_INDEX_REFERENCE_BROWSER_BRIEF.md).
6. Canonical route migration brief.

## Validation Gates

Before a slice is accepted:

- Search rendered widget tests for raw IDs in visible text.
- Verify light and dark theme rendering for the changed page.
- Verify sentence refs resolve to target sentence and learner translation.
- Verify bottom related examples do not duplicate inline examples.
- Verify dictionary detail uses homograph labels like `보다 1`, not `Entry 1`.
- Verify no Stitch external URLs are copied into production widgets.
- Run targeted Flutter tests and `flutter analyze` on touched files.
