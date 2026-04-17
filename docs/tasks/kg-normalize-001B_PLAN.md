# Implementation Plan - kg-normalize-001B

This task involves normalization and hardening of Knowledge Lab items, specifically focusing on modifier clarity, adverb categorization, and rescuing connectors from a polluted backup.

## User Review Required

> [!IMPORTANT]
> **ID Allocation**: I will be using IDs `ex.ko.s.001157` through `ex.ko.s.001166` for the rescued connector examples, as the current library ends at `001156`.
> **Content Reconstruction**: Since the Core Korean sentences were missing from the backup files for `geuraeseo` and `geurigo` examples, I have reconstructed them based on the backup translations and common pedagogical patterns found in the KI explanations.

## Proposed Changes

### 1. Modifier Surface De-duplication (Task A)

Modify the `surface` and `title` fields to distinguish between verb and adjective modifiers using the same `ㄴ/은` form.

#### [MODIFY] [kg.grammar.modifier.v_eun.json](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/knowledge/grammar/modifier/kg.grammar.modifier.v_eun.json)
- `surface`: `"ㄴ/은 + 名詞"` -> `"動詞 + ㄴ/은 + 名詞 (過去)"`
- `title`: `"動詞 ㄴ/은 + 名詞"` -> `"動詞 + ㄴ/은 + 名詞 (過去)"`

#### [MODIFY] [kg.grammar.modifier.adj_noun.json](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/knowledge/grammar/modifier/kg.grammar.modifier.adj_noun.json)
- `surface`: `"ㄴ/은 + 名詞"` -> `"形容詞 + ㄴ/은 + 名詞 (現在)"`
- `title`: `"形容詞 ㄴ/은 + 名詞"` -> `"形容詞 + ㄴ/은 + 名詞 (現在)"`

---

### 2. A1 Adverbs Tags Enrichment (Task B)

Add functional tags (`time`, `degree`) to beginner adverbs that are currently missing them.

#### [MODIFY] [Adverb KIs](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/knowledge/grammar/adverb/)
- **Time** (`time`): `akka`, `geumbang`, `najunge`, `ittaga`, `got`, `jamsi_hu`, `mak`, `eolleun`, `dangjang`
- **Degree** (`degree`): `yakgan`, `kkwae`
- Ensure all have `grammar` and `adverb` tags.

---

### 3. Pilot Connector Rescue & Reconstruction (Task C)

Rescue `그래서` and `그리고` from `runs/backup/polluted_kg_lab/`, convert to V5 format, and reconstruct their example sentences.

#### [NEW] [kg.connector.cause.geuraeseo.json](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/knowledge/cause/kg.connector.cause.geuraeseo.json)
#### [NEW] [kg.connector.sequence.geurigo.json](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/knowledge/sequence/kg.connector.sequence.geurigo.json)
- Convert from backup, ensuring `id`, `kind`, `subcategory`, `level`, `surface`, `tags`.
- Update `example_sentence_refs` to use new `ex.ko.s.XXXXXX` IDs.

#### [NEW] [Example Sentences (10 files)](file:///f:/Githubs/lingo/content-ko/content/core/learning_library/example_sentence/)
- Create `ex.ko.s.001157` to `ex.ko.s.001166`.
- Each file will have `ko`, `level`, `tags`, `knowledge_refs`, and `provenance`.

#### [NEW] [I18n KI and Examples](file:///f:/Githubs/lingo/content-ko/content/i18n/zh_tw/learning_library/)
- Create I18n counterparts for KIs and examples, using the flattened V5 schema (no `_zh_tw` suffixes).

---

### 4. Machine Status Update

#### [NEW] [local.json](file:///f:/Githubs/lingo/release-aggregator/docs/tasks/machines/local.json)
- Initialize the machine claim file.

#### [MODIFY] [MACHINE_STATUS.md](file:///f:/Githubs/lingo/release-aggregator/docs/tasks/MACHINE_STATUS.md)
- Ensure 888's status is correctly reflected.

## Verification Plan

### Automated Tests
- Run `python scripts/validate_learning_library_schema.py` (if it exists) to verify the new/modified files.
- Verify that `ko` and `translation` fields are used correctly (no `_zh_tw` left).

### Manual Verification
- Double check the Korean sentences for accuracy and pedagogical value.
