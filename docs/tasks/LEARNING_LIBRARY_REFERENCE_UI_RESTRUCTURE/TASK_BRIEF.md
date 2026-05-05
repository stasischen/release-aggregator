# Task Brief

## Metadata

- Task ID: LEARNING_LIBRARY_REFERENCE_UI_RESTRUCTURE
- Owner: release-aggregator control tower
- Target repo: `lingo-frontend-web`
- Read-only context repos: `release-aggregator`, `content-ko`
- Status: in_progress
- DeepSeek routing: flash -> pro
- Created: 2026-05-05

## Goal

Redesign Knowledge Lab, Sentence Bank, and Dictionary lookup from artifact-backed
prototype pages into one coherent education-app reference system.

This task continues `LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF`; it does not invent
a new content schema. The target is product behavior:

- learners can browse hundreds of knowledge items without a cluttered mixed list
- a knowledge item can teach through its example sentences
- a dictionary entry can show example sentences that use that word/atom/lemma
- selecting a topic/knowledge/sentence/source/dictionary entry opens a stable, useful detail surface
- Sentence Bank becomes the evidence/search layer under Knowledge Bank and Dictionary, not a competing primary product
- content gaps are visible as scoped unavailable states, not broken navigation

## Current Problem

The current frontend technically loads v2 Learning Library artifacts, but the UI still
behaves like a prototype inventory screen.

Observed issues:

1. Knowledge Lab and Sentence Bank each place too many unrelated controls and result
   types into one long page.
2. Overview cards and list items do not establish a clear "choose index -> inspect detail
   -> jump to related example/source" flow.
3. Detail routes can feel like they return to the same page because legacy `/study/...`
   redirects are still used inside Library screens and detail context is not visually
   preserved.
4. Knowledge Lab has 218 knowledge items but only 4 topics, 8 vocab sets, and 5 links in
   the current frontend artifact set, so the topic/vocab-first UI exposes staging
   sparsity instead of guiding learners.
5. Sentence Bank has 3346 sentences, but many are in `shared_bank` instead of a user-facing
   source, so the source-first list hides a large part of the example bank.
6. Dictionary lookup and sentence lookup are disconnected even though learners naturally
   expect "look up a word -> see examples using it".
7. Current acceptance did not require "tap opens useful detail" smoke tests across
   Knowledge Lab, Sentence Bank, and Dictionary example lookup.
8. Dark-mode and dense-list layout gates are not explicit enough for these reference pages.

## Prior Art To Preserve

Read before implementation:

- `docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md`
- `docs/guides/LEARNING_SOURCE_MULTILAYER_ARCHITECTURE.md`
- `docs/tasks/assets/LLCM_005G_CORE_I18N_PACK_EMISSION_SPEC.md`
- `docs/tasks/assets/LLCM_005H_FRONTEND_COMPOSITION_INTAKE_SPEC.md`
- `docs/tasks/LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/UI_ACCEPTANCE_MATRIX.md`
- `docs/tasks/LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/HANDOFF_SUMMARY.md`

Keep these decisions:

- Do not merge Content-First Learning and Knowledge-First Lab into one screen.
- Do not make `vocab_sets` a second dictionary truth.
- Do not make Sentence Bank a second standalone learning product.
- Do not make Dictionary own example-sentence truth; it should consume the shared sentence graph.
- Do not move merge logic into screens; screens read composed snapshot only.
- Do not change lesson runtime data format.
- Do not edit `content-ko` or `content-pipeline` in this task.

## Product Direction

### Knowledge Bank

Knowledge Bank is the primary reference and study-planning surface. It replaces the idea
of two parallel top-level products called "Knowledge Lab" and "Sentence Bank".

Primary flow:

```text
Knowledge Bank home
  -> index rail/category lane
  -> focused result list
  -> detail reader
  -> sentence evidence / sources / dictionary drilldown
```

Home must not show every result type at once. It should provide clear modes:

- Grammar and endings
- Patterns and usage
- Topics
- Vocab teaching sets
- Recently/featured items if available

### Sentence Evidence Layer

Sentence Bank becomes the example evidence layer for Knowledge Bank and Dictionary. It may
still have a search route, but it is not a parallel conceptual product.

Primary flow:

```text
Sentence search
  -> search/filters
  -> sentence result list as primary
  -> sentence detail with atom breakdown
  -> source / knowledge / dictionary related actions
```

Source browsing remains available, but it should not hide `shared_bank` examples. For an
education app, sentence search and sentence quality are more important than making every
example belong to a video card.

### Dictionary Example Layer

Dictionary should answer two learner questions:

```text
What does this word/atom mean?
Where have I seen it used?
```

Dictionary detail should therefore include an example-sentence section when the composed
Learning Library snapshot has matching atoms, vocab refs, or sentence surfaces.

Dictionary remains lexical truth. Sentence examples remain Learning Library evidence.

## Acceptance Criteria

1. Knowledge Bank home has a clear master-detail information architecture and does not mix
   all topics/items/vocab into one long page by default.
2. Knowledge Bank item/topic/vocab taps open details that visibly differ from the home page
   and render real artifact fields.
3. Sentence search prioritizes example lookup and can show `shared_bank` examples.
4. Sentence detail can show atom breakdown, dictionary drilldown, related knowledge, related
   topics, and source context without crashing or duplicating overlays.
5. Dictionary detail can show related example sentences for matched atom/lemma/surface refs
   without becoming a second sentence store.
6. Legacy `/study/knowledge-lab...` and `/study/sentence-bank...` redirects may remain for
   compatibility, but Library UI should navigate with canonical `/library/...` routes.
7. Empty or sparse groups are hidden, collapsed, or marked as unavailable; they must not
   look like broken product choices.
8. Dark mode smoke tests cover home and detail surfaces for Knowledge Bank, sentence detail,
   and dictionary example sections.
9. Targeted widget tests prove that selecting an item/sentence/source/dictionary example
   opens detail content instead of silently returning to the same home view.

## Out Of Scope

- Lesson runtime data format.
- `content-ko` edits.
- `content-pipeline` edits.
- Dictionary `mapping_v2` origin cache removal.
- Replacing the whole app shell or bottom navigation.
