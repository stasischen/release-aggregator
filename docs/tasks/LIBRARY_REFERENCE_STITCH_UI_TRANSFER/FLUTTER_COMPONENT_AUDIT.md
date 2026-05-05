# Flutter Component Audit

Date: 2026-05-05

Scope:

- `lingo-frontend-web`
- Knowledge Lab index/detail
- Sentence detail
- Dictionary content/detail panel
- Video player learning overlay

This audit completes `lrsut-02` and prepares `lrsut-03`.

## Summary

The frontend already has enough artifact-backed data aggregation to support the
Stitch-inspired Library reference UI. The main gap is not repository/data
availability; it is presentation structure.

Current state:

- Knowledge detail can resolve inline sentence refs and dedupe bottom examples.
- Sentence detail can show target sentence, learner translation, atoms, source,
  knowledge, and topics.
- Dictionary content can resolve atom/component meanings, homograph candidates,
  and example sentences through Learning Library lookup.
- Video player can render subtitles, atom clusters, dictionary panel, and
  full-screen subtitle overlay.

Blocking UI gap:

- Each page currently owns its own cards, surface colors, text hierarchy,
  evidence chips, and navigation affordances.
- Several widgets still hardcode Material colors directly instead of using a
  Library semantic token layer.
- Stitch layouts cannot be transferred safely until shared Library reference
  components exist.

## Real Artifact Fields Available

### Knowledge Detail

Frontend aggregate: `LearningLibraryLookup.getKnowledgeDetail`.

Usable fields:

- `KnowledgeItem.id`
- `KnowledgeItem.kind`
- `KnowledgeItem.titleZhTw`
- `KnowledgeItem.surface`
- `KnowledgeItem.summaryZhTw`
- `KnowledgeItem.explanation`
- `KnowledgeItem.explanationMd`
- `KnowledgeItem.usageNotes`
- `KnowledgeItem.usageNotesMd`
- `KnowledgeItem.exampleBank`
- `KnowledgeItem.topicRefs`
- `KnowledgeItem.metadata`
- related `Topic`
- related `Sentence`
- related `Source`

Allowed Stitch sections:

- Hero: `surface`, `titleZhTw`, `summaryZhTw`, `kind`, `metadata.level`.
- Core meaning: `explanationMd` / `explanation` / `summaryZhTw`.
- Semantic example rows: markdown tables containing sentence refs resolved
  through related `Sentence`.
- Usage scenarios: `usageNotesMd` / `usageNotes`.
- Related resources: related sentences, topics, sources.

Reject / adapt:

- Stitch-invented featured images, counts, labels, and fake examples.
- Raw `kg.*`, `ex.*`, or `src.*` IDs as visible body text.

### Sentence Detail

Frontend aggregate: `LearningLibraryLookup.getSentenceDetail`.

Usable fields:

- `Sentence.id`
- `Sentence.sourceId`
- `Sentence.surfaceKo`
- `Sentence.translationZhTw`
- `Sentence.translation`
- `Sentence.startMs`
- `Sentence.endMs`
- `Sentence.knowledgeRefs`
- `Sentence.vocabRefs`
- `Sentence.topicRefs`
- `Sentence.atoms`
- related `Source`
- related `KnowledgeItem`
- related `Topic`
- related `VocabItem`

Allowed Stitch sections:

- Sentence hero: target sentence and learner translation.
- Token breakdown: `Sentence.atoms`.
- Related knowledge: related `KnowledgeItem`.
- Source moment: related `Source`, `startMs`, `endMs`.
- Similar/evidence sentences: should be added later through lookup/search, not
  invented.

Reject / adapt:

- Korean-specific labels as component contracts. Use target/learner language
  concepts.
- Any raw atom ID as primary learner-facing text.

### Dictionary Detail

Frontend source: `DictionaryContent`.

Usable fields:

- `DictionaryInventoryEntry.id`
- `term`
- `lemma`
- `meaning`
- `description`
- `literal`
- `origin`
- `pos`
- `type`
- `tags`
- `grammarRefs`
- `senses`
- `DictionaryFormatter.getComponents`
- `DictionaryFormatter.getComponentsBySurface`
- `LearningLibraryLookup.getDictionaryExamples`

Allowed Stitch sections:

- Headword and learner meaning.
- Homograph selector using candidate lookups.
- Sense groups using Korean dictionary style labels such as `{word} 1`,
  `{word} 2`, not `Entry 1`.
- Morphology/component breakdown.
- Example sentence evidence.
- Related knowledge through grammar refs / example match knowledge.

Reject / adapt:

- Technical POS compositions such as `v+e`, `n+p`, resolver IDs, or composite
  atom IDs as primary labels.
- Hardcoded missing-copy strings such as `No definition`, `[no meaning]`, or
  `[MISSING ID]`.

### Video Player

Frontend source: `VideoPlayerScreen` with:

- `LingoVideoPlayer`
- `LingoSubtitleList`
- `ImmersiveSubtitleOverlay`
- `LingoDictionaryPanel`
- `videoPlayerControllerProvider`

Usable fields:

- `VideoMetadata.title`
- `VideoMetadata.languageCode`
- subtitle `SubtitleLine.id`
- subtitle text and translated text
- subtitle segments / atom clusters
- selected cluster dictionary lookup
- player full-screen state

Allowed Stitch sections:

- Player region.
- Current subtitle focus card.
- Transcript list.
- Selected token dictionary panel.
- Support/knowledge anchor actions.

Reject / adapt:

- Duplicate dictionary surfaces for the same selected token.
- Treating video accent as error red.
- Route-driven player state sync before the player overlay contract is stable.

## Existing Widget Inventory

### Keep As Data/Behavior Sources

| Existing widget/service | Keep reason |
| :--- | :--- |
| `LearningLibraryLookup` | Already provides detail aggregates and relationship lookup. |
| `KnowledgeInlineResolver` | Prevents raw sentence IDs from leaking into prose. |
| `KnowledgeItemParser` | Preserves module structure from content markdown. |
| `DictionaryContent` | Has dictionary resolution, candidates, components, examples. |
| `VideoPlayerScreen` controller stack | Has playback, subtitles, selected cluster, full-screen state. |

### Refactor Behind Shared Components

| Existing widget | Issue | Target component |
| :--- | :--- | :--- |
| `KnowledgeReaderScaffold` | Knowledge-specific naming but useful shell pattern. | `LibraryReferenceScaffold` |
| `LibrarySearchBar` | Reusable but needs tokenized surfaces. | keep/rename later |
| `LibraryFilterGroup` | Reusable but visually dense. | `LibraryFilterRail` / `LibraryChipFilterGroup` |
| `KnowledgeItemCard` | Good content shape, needs evidence counts and tokens. | `KnowledgeReferenceCard` |
| `KnowledgeModuleCard` | Has hardcoded green/blue/orange/purple/teal colors. | `KnowledgeModuleSection` using `LibraryReferenceColors` |
| Inline sentence/table widgets inside `KnowledgeModuleCard` | Behavior is correct but private to Knowledge. | `InlineExampleGroup`, `SemanticExampleTable` |
| Sentence atom `ActionChip` list | Too weak for sentence microscope. | `TokenBreakdownTile` / `TokenBreakdownGrid` |
| Source/knowledge cards in `SentenceDetailScreen` | Duplicated card patterns. | `SourceMomentCard`, `RelatedKnowledgeCard` |
| `_DictionaryCandidateSelector` and component rows | Good logic but presentation tied to popup. | `DictionaryHomographTabs`, `DictionaryComponentRow` |
| `LingoDictionaryPanel` | Correct function, needs non-duplicated panel contract. | `ReferenceDictionaryPanel` |
| Subtitle list/current overlay | Good playback linkage, needs current focus card. | `VideoSubtitleFocusCard`, `TranscriptLineTile` |

## Hardcoded Color Risks Found

These should be retired during `lrsut-03` before page rewrites:

- `KnowledgeModuleCard` uses `Colors.green/blue/orange/purple/teal` directly.
- `KnowledgeModuleCard` uses `Colors.black.withValues(alpha: 0.02)` for shadow.
- `VideoPlayerScreen` intentionally uses black player chrome, but surrounding
  panels must use tokenized Library surfaces.
- `DictionaryContent` fallback warning uses direct orange and direct fallback
  copy in at least one branch.

Rule:

Player chrome may stay black. Learning/reference panels around it must use
`LibraryReferenceColors`.

## Component Boundaries For lrsut-03

Create these first, before redesigning pages:

| Component | Inputs | Used by |
| :--- | :--- | :--- |
| `LibraryReferenceColors` | light/dark token values | all Library reference surfaces |
| `LibraryReferenceScaffold` | title, subtitle, actions, body | Knowledge, Sentence, Dictionary, Video support panes |
| `LibrarySectionCard` | title, icon, accent role, child | all pages |
| `EvidenceChip` | evidence type, label, count, selected | index/detail evidence counts |
| `EvidenceCountRow` | counts for knowledge/sentence/dictionary/video/source | cards and heroes |
| `TargetTextBlock` | target text, optional pronunciation | sentence, dictionary, knowledge |
| `LearnerTranslationBlock` | learner-language copy, optional missing state | sentence/example cards |
| `InlineExampleGroup` | title, sentences, onTap | knowledge prose and detail pages |
| `SemanticExampleTable` | headers, rows, resolved sentences | knowledge detail |
| `TokenBreakdownTile` | atom text, pos label, meaning, selected, onTap | sentence/video/dictionary |
| `RelatedKnowledgeCard` | knowledge item, evidence counts, onTap | sentence/detail/source |
| `SourceMomentCard` | source, start/end, onTap | sentence/video |
| `DictionarySenseCard` | headword, sense index, meaning, examples | dictionary |
| `ReferenceDictionaryPanel` | selected cluster/entry, close, examples toggle | video/sentence overlays |
| `VideoSubtitleFocusCard` | current subtitle, translation, tokens | video |

## Implementation Order Adjustment

Recommended `lrsut-03` order:

1. Add `LibraryReferenceColors` and register it in `AppTheme`.
2. Add small stateless shared components with no repository reads.
3. Move Knowledge inline example/table private widgets into shared components.
4. Refactor Sentence detail to use shared components first, because it has the
   clearest data shape and exercises target/learner/token/source/knowledge.
5. Refactor Knowledge detail after Sentence components are stable.
6. Refactor Dictionary and Video panels after token/detail card behavior is
   reusable.

## Non-Goals

- Do not change lesson data format.
- Do not change `content-ko`.
- Do not change `content-pipeline`.
- Do not migrate routes during component extraction.
- Do not adopt Stitch-generated copy, counts, images, or navigation labels.

## Acceptance Gates For lrsut-03

- Shared components compile in both light and dark themes.
- No new raw artifact IDs appear in widget-visible text.
- No page-level light-only hardcoded surfaces.
- No duplicate dictionary popup/panel for one selected token.
- Missing localized content uses localized UI strings.

