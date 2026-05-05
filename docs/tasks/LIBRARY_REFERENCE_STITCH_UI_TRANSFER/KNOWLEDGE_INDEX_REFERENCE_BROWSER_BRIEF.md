# Knowledge Index Reference Browser Brief

## Purpose

This brief scopes `lrsut-08` before implementation. It corrects the next
Knowledge Index redesign against the existing source-first architecture docs,
instead of introducing a new graph or treating Knowledge Lab as the app's main
learning path.

## Canonical Prior Art

Implementation must follow these existing documents:

- `docs/guides/LEARNING_SOURCE_MULTILAYER_ARCHITECTURE.md`
- `docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md`
- `docs/guides/KNOWLEDGE_LAB_CONTENTKO_ARCHITECTURE.md`
- `docs/handoffs/2026-04-16_KG_PIPELINE_006_COURSE_RESTRUCTURE_NOTES.md`
- `docs/tasks/LEARNING_LIBRARY_REFERENCE_UI_RESTRUCTURE/PRODUCT_IA_PLAN.md`

Do not rename the architecture. The existing terms are authoritative:

- `source`
- `sentence`
- `topic`
- `knowledge_item`
- `vocab_item`
- `Content-First Learning`
- `Knowledge-First Lab`

## Product Boundary

`Knowledge-First Lab` is a reference feature.

It is for:

- grammar / pattern / usage lookup
- example evidence browsing
- reverse lookup to source content
- reference-style review

It is not for:

- replacing Content-First Learning
- making video / article / dialogue secondary to grammar cards
- presenting source counts as a learner goal
- deciding lesson / practice flow
- restructuring lesson runtime data

`video`, `dialogue`, `article`, `story`, and `lesson` remain `source` types and
belong to Content-First Learning as primary learning surfaces. Knowledge Lab may
link back to them as related sources, but it must not become the main content
player or reader.

## Current Artifact Reality

Frontend artifact snapshot observed on 2026-05-05:

| Artifact | Count | Implication |
| :--- | ---: | :--- |
| Knowledge items | 218 | Enough for a reference catalog. |
| Knowledge i18n items | 218 | Enough for learner-language labels/details in current locale. |
| Knowledge items with `explanation_md` | 207 | Enough for detail pages and derived preview fallback. |
| Knowledge items with `example_sentence_refs` | 215 | Enough for example-first cards and detail evidence. |
| Median examples per knowledge item | 10 | Strong detail evidence; avoid showing this as primary card copy. |
| Sentences | 3346 | Strong evidence layer. |
| Sentence i18n translations | 3345 | Strong current-locale evidence. |
| Sentences with atoms | 3346 | Strong dictionary drilldown potential. |
| Sentences with knowledge refs | 1210 | Good but incomplete graph coverage. |
| Sources | 11 | Useful as related content, not enough to dominate reference UI. |
| Topics | 4 | Too sparse for topic-first Knowledge Lab IA. |

Design implication:

- Default catalog should be knowledge-item-first.
- Topics and vocab should be secondary/collapsed until graph density improves.
- Do not use counts as the primary learning decision surface.
- Do not expose artifact IDs, source IDs, package paths, or raw refs as body
  copy.

## Knowledge Index Role

The index is a reference browser for "I want to look up or compare a language
point."

A useful card should answer:

- What target-language form is this?
- What is the learner-language title?
- When would I use it?
- What is one representative example?
- What type/level/tag helps me filter it?

It should not primarily answer:

- How many examples exist?
- How many sources reference it?
- How many links are in the artifact graph?

Counts may be used for QA/debug or secondary affordances, but they should not be
the main visible hierarchy.

## Current Field Strategy

No new schema is required for the first frontend slice.

Use a view adapter in Flutter to derive a card model from the composed snapshot:

```text
KnowledgeReferenceCardView
  id
  targetSurface              <- KnowledgeItem.surface
  learnerTitle               <- current locale title field via domain getter/adapter
  learnerPreview             <- description/summary or first plain paragraph from explanation_md
  level                      <- metadata.level / DTO level
  kind                       <- metadata.kind / DTO kind
  subcategory                <- metadata.subcategory / DTO subcategory
  tags                       <- metadata.tags
  examplePreview             <- first resolved example_sentence_ref
  exampleTranslation         <- first resolved sentence i18n translation
```

This adapter must be centralized. Widgets must not parse markdown or inspect
raw DTO/i18n merge details directly.

## Schema Follow-Up

Longer term, avoid frontend markdown-derived preview logic. Align future content
work with the existing `KG Pipeline 006` direction:

- `teaching_blocks_{locale}` for structured pedagogical content inside a
  knowledge item
- `aliases_{locale}` for learner-facing search aliases
- `source_refs` for traceability back to content sources
- `example_sentence_refs` for evidence links

Potential future app-facing preview fields should be reviewed against
`KNOWLEDGE_SCHEMA_EXTENSION_PROPOSAL_V1.md` before adding anything new. Do not
introduce a separate `learning_preview` schema in this slice.

## UI Shape

### Header

- Search field.
- Brief reference-mode description.
- No count dashboard as the hero.

### Filter Rail / Chips

- Level.
- Kind.
- Subcategory.
- Tags or common functions when available.
- Topics only as a secondary/collapsed lane because current topic density is
  sparse.

### Result Cards

Each card should show:

- Target surface.
- Learner title.
- Short learner preview derived by adapter.
- One example sentence with translation when available.
- Level/kind/subcategory chips.
- Optional "related source" affordance as secondary metadata, not card headline.

### Secondary Sections

- Topic browser: collapsed or hidden when too sparse.
- Vocab teaching sets: collapsed; do not present as dictionary truth.
- Source reverse lookup: detail-level action, not index primary hierarchy.

## Route Rules

Keep current working routes during this slice:

```text
/library/knowledge-lab
/library/knowledge-lab/item/:knowledgeId
/library/knowledge-lab/topic/:topicId
```

Do not start route migration here. `lrsut-09` owns canonical route migration.

## Acceptance Criteria

1. Knowledge Lab home is visibly a reference browser, not a source/content
   learning home.
2. Default view lists knowledge items with learner-useful previews and example
   evidence.
3. Default view does not show an artifact/count dashboard as the main hero.
4. Topic and vocab lanes are secondary/collapsed or hidden when sparse.
5. Cards do not expose raw IDs, source IDs, atom IDs, package paths, or unresolved
   sentence refs.
6. Widgets do not parse raw markdown directly; preview derivation is centralized
   in a view adapter/controller layer.
7. Tapping a card opens `KnowledgeItemDetailScreen` through
   `/library/knowledge-lab/item/:knowledgeId`.
8. Dark mode is covered by a targeted widget smoke test.
9. Search/filter tests prove the UI filters by learner title, target surface,
   kind/subcategory, and does not fall back to technical IDs as visible copy.

## Out Of Scope

- Lesson runtime contract.
- Practice / speaking / listening / reading / writing activity schema.
- Content pipeline edits.
- `content-ko` edits.
- Dictionary source of truth changes.
- Route migration.
- New schema fields without reviewing existing KG Pipeline 006 proposal first.

