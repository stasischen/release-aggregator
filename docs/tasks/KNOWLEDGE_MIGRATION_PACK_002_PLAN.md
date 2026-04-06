# Knowledge Migration Pack 002 Plan

## Goal

Plan and execute the second bounded knowledge migration pack for Korean learning-library content.
This pack focuses on **Core Particles** and **Basic Connectors** that were identified as high-value for A1 learners but were not included in the first prototype pack.

---

## Pack 002 Scope

### 1. Core Particles (Grammar > Particle)

| Canonical ID | Surface | Source Report | Notes |
| :--- | :--- | :--- | :--- |
| `kg.grammar.particle.object` | `~을/를` | `youtube_beginner_grammar/006_受詞助詞 을測試.md` | Basic object marker. |
| `kg.grammar.particle.at_time_place` | `~에` | `007_場所助詞 에.md`, `020_時間名詞에在時 시간 명사 에.md` | Merge both usage (Time & Place) into one canonical item. |
| `kg.grammar.particle.at_place_action` | `~에서` | `008_動作發生的場所 에서.md` | Place of action/origin. |
| `kg.grammar.particle.also` | `~도` | `012_也還 도.md` | Inclusive particle. |
| `kg.grammar.particle.and_with_hago` | `~하고` | `011_並列一起 하고.md` | Colloquial "and/with". |

### 2. Basic Connectors (Connector)

| Canonical ID | Surface | Category | Source Report |
| :--- | :--- | :--- | :--- |
| `kg.connector.sequence.geurigo` | `그리고` | `sequence` | `youtube_connectors/113_...그리고-然後-並且.md` |
| `kg.connector.cause.geuraeseo` | `그래서` | `cause` | `youtube_connectors/112_...그래서-所以-因此.md` |
| `kg.connector.contrast.hajiman` | `하지만` | `contrast` | `youtube_connectors/099_...하지만-但是-不過.md` |
| `kg.connector.conversion.geureonde` | `그런데` | `conversion` | `youtube_connectors/097_...그런데-但是-不過.md` |
| `kg.connector.condition.geureomyeon` | `그러면` | `condition` | `youtube_connectors/087_...그러則話.md` |

---

## Normalization Strategy

1.  **ID Standards**: Use `kg.<family>.<subcategory>.<slug>` format.
2.  **Merging**: `~壓` for time and place will be merged into a single `kg.grammar.particle.at_time_place` to avoid duplication of the core concept.
3.  **Title/Summary**: Rewrite source titles to remove emojis and numbering (e.g., `006_受詞助詞 을를` -> `受詞助詞 (~을/를)`).
4.  **Example Cleanup**: Select 3-5 best examples from reports, checking for OCR issues in the source MD.

---

## Cleanup Tasks (Duplicate/ID Audit)

1.  Audit existing `content-ko` knowledge items for naming consistency.
    - Rename `kg.beginner.present.copula` -> `kg.grammar.copula.present_polite_informal`? Or keep as is if stable.
    - Rename `kg.beginner.honorific.ssi` -> `kg.grammar.honorific.suffix_ssi`?
2.  Standardize `kind` and `subcategory` according to the new taxonomy.

---

## Tasks

- [x] Create core JSON files in `content-ko/content/core/learning_library/knowledge/...`
- [x] Create i18n JSON files in `content-ko/content/i18n/zh_tw/learning_library/knowledge/...`
- [x] Perform naming and path cleanup (standardized to `kg.<kind>.<subcategory>.<slug>.json`, singular suffixes, and directory normalization).
- [ ] Update links if relevant (verified existing links work with new IDs)
- [x] Verify content integrity (no mixed-script or OCR issues detected)
- [x] Verify build artifacts after migration (renaming and ID updates consolidated)
