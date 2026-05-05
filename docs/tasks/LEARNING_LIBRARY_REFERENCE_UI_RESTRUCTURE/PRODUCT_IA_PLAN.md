# Product IA Plan

## Diagnosis

The prior `LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF` task correctly fixed artifact
composition and created the first index-first frontend slice. Its weakness was that it
accepted "can load and list artifact data" as sufficient UI progress.

That is not enough for an education app. A learner needs:

- a clear starting intention
- a focused list
- a detail reader that explains why the item matters
- examples, dictionary lookup, and source context
- predictable drilldown and back behavior

## Current Artifact Reality

Frontend artifact snapshot on 2026-05-05:

| Layer | Count | Product Implication |
| :--- | ---: | :--- |
| Sources | 11 | Enough for a source lane, not enough as the only Sentence Bank entry. |
| Sentences | 3346 | Strong enough to make Sentence Bank sentence-first. |
| Knowledge items | 218 | Strong enough for Knowledge Lab primary catalog. |
| Topics | 4 | Too sparse to be a primary product mode yet. |
| Vocab sets | 8 | Too sparse to be a primary product mode yet. |
| Links | 5 | Too sparse to promise rich graph navigation globally. |

Design implication:

- Knowledge Bank should lead with knowledge items grouped by kind/subcategory/level.
- Topic and vocab lanes should be secondary and hidden/collapsed when sparse.
- Sentence search should be an evidence layer under Knowledge Bank and Dictionary, not a
  competing primary product.
- `shared_bank` examples need a first-class "Example Bank" source context or source-less
  detail layout.

## Unified Reference Model

The product model should be:

```text
Knowledge Bank
  -> grammar / pattern / usage item
    -> explanation
    -> 10 example sentences
      -> atom dictionary lookup
      -> source context

Dictionary
  -> word / atom / lemma detail
    -> meanings and homographs
    -> example sentences using this atom/lemma/surface
      -> related knowledge items
      -> source context

Sentence Search
  -> example sentence result
    -> related knowledge item
    -> atom dictionary lookup
    -> source context
```

Knowledge is the teaching unit. Sentences are evidence and practice material. Dictionary is
lexical lookup. Source is real-world context.

## Knowledge Bank Redesign

### Home Layout

Use a three-zone layout.

1. Hero summary:
   - artifact counts
   - selected mode
   - one primary search field

2. Mode rail:
   - `All`
   - `Grammar`
   - `Endings`
   - `Patterns`
   - `Usage`
   - `Topics` only if count is meaningful
   - `Vocab Sets` only if count is meaningful

3. Focused results:
   - one result type at a time by default
   - grouped sections only inside the selected mode
   - compact cards with surface, title, level, kind, short summary, example count

Do not render topic cards, knowledge cards, and vocab chips all on the same default page.

### Detail Layout

Knowledge item detail should read like a compact grammar book entry:

1. Header:
   - Korean surface
   - localized title
   - kind/subcategory/level chips

2. Explanation:
   - `explanationMd`/`explanation`
   - `usageNotesMd`/`usageNotes`

3. Example bank:
   - sentence cards with Korean, translation, atom chips
   - dictionary popup from atoms

4. Related:
   - related topics if present
   - related sources if present
   - fallback text when graph density is not available

### Route Rules

- UI inside Library uses canonical `/library/knowledge-lab/...` routes.
- Legacy `/study/knowledge-lab/...` redirects may remain for deep-link compatibility.
- Detail screens must have distinct app bar/title/body structure so they do not feel like
  the home screen re-rendered.

## Sentence Evidence Redesign

### Home Layout

Sentence Search should be sentence-first and can live inside Knowledge Bank as a tab or
sub-route. It does not need equal top-level weight next to Knowledge Bank.

1. Hero/search:
   - "Search Korean, translation, atom surface, or source title"
   - count of matching sentences

2. Filter row:
   - level
   - source type
   - source selection
   - knowledge kind if related refs exist

3. Results:
   - primary sentence list
   - each card shows Korean sentence, translation, source label, atom count, related
     knowledge count

4. Source lane:
   - collapsed "Browse by source" section
   - source cards are secondary, not the default main result

### Detail Layout

Sentence detail should be a learning unit:

1. Main sentence:
   - Korean
   - translation
   - TTS action if available

2. Atom breakdown:
   - consistent token chips
   - dictionary detail opens in one bottom sheet only

3. Knowledge used:
   - related grammar/pattern cards
   - opens Knowledge Lab detail

4. Source context:
   - if source exists: link to source detail
   - if source is `shared_bank`: show "Example Bank" context and do not show broken source

5. Related examples:
   - other sentences with same knowledge refs where available

## Data Handling Rules

- Do not read raw `content-ko` paths from UI.
- Do not merge core/i18n in screens.
- Treat sparse topic/vocab/link density as content maturity, not UI failure.
- Show unavailable states through localized UI strings, not hardcoded debug labels.
- Dictionary example lookup must read the composed Learning Library snapshot and dictionary
  lookup results; it must not create a duplicate sentence model inside dictionary assets.
- Matching priority for dictionary examples:
  1. exact atom id / dictionary atom ref when available
  2. component atom id inside composite atom ids
  3. lemma/surface fallback
  4. plain sentence surface search as a weak fallback

## Implementation Slices

### Slice A: Navigation Cleanup

- Replace internal `/study/knowledge-lab...` pushes with `/library/knowledge-lab...`.
- Replace internal `/study/sentence-bank...` pushes with `/library/sentence-bank...`.
- Add tests that tapping a result renders detail-specific content.

### Slice B: Knowledge Bank Focused Catalog

- Add catalog mode state to `KnowledgeLabPageController`.
- Default mode: knowledge items.
- Secondary modes: topics/vocab only when enough data exists.
- Replace the mixed default `ListView` with focused sections.

### Slice C: Sentence Evidence Layer

- Default result list is sentences, including `shared_bank`.
- Source browser becomes a collapsed/secondary section.
- Sentence detail handles source-less/shared_bank examples cleanly.

### Slice D: Dictionary Example Integration

- Add a dictionary-detail example sentence section.
- Match examples by atom id, component atom id, lemma/surface fallback.
- Example cards link to sentence detail and related knowledge detail.
- The section is hidden or shows a scoped unavailable state when no composed snapshot exists.

### Slice E: Detail Surface Hardening

- Ensure Knowledge Item, Topic, Vocab, Sentence, and Source details render useful data.
- Add dark-mode smoke tests.
- Add sparse graph fallback tests.

### Slice F: Content Follow-Up

Prepare a read-only content inventory for:

- why frontend artifact has only 4 topics while knowledge has 218 items
- whether 8 vocab sets are expected or an emission gap
- whether links should be generated from knowledge/example refs
- how to represent `shared_bank` as a product source context
- whether dictionary inventory should expose stable `example_sentence_refs`, or whether
  frontend matching should remain derived from sentence atoms for now

Gemini can do this content-side inventory. Gemini should not edit frontend code.
