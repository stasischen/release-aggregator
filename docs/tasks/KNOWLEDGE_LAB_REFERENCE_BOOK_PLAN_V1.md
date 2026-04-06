# Knowledge Lab Reference Book Plan V1

## Goal

Pivot the Knowledge Lab from lesson-specific enrichment to a comprehensive **"Reference Book"** model. The goal is to ingest high-frequency Korean grammar, patterns, and connectors from `lingo-curriculum-source` to create a browseable manual for learners, adhering strictly to the existing `core/i18n` artifact contract.

## 1. Source Inventory Summary

### Grammar-style (High Value)

- `youtube_beginner_grammar`: 141 core items from Clean MD.
- `youtube_connective_endings`: 112 intermediate/advanced endings from Clean MD.

### Connector-style (High Value)

- `youtube_connectors`: 113 causal/contrastive items from Clean MD.

### Pattern-style (High Value)

- `ko_survival_pattern_library_v1.json`: 188 functional patterns (Structured JSON).

### Topic/Usage (Reference Layer)

- `topic_taxonomy_v1.json`, `can_do_catalog_v1.json`: Browse/Retrieval grouping.

## 2. Canonical Mapping (Core + i18n Contract)

All ingestion MUST map to the following established fields:

- **Core (`core.json`)**: `id`, `kind`, `subcategory`, `level`, `surface`, `tags`.
- **i18n (`i18n/{support}/knowledge.json`)**: `id`, `title_zh_tw`, `summary_zh_tw`, `explanation_md_zh_tw`, `usage_notes_zh_tw`, `example_bank`.

**Provenance Data (media_id, source_order)**: Relegated to `source_refs` or internal mapping notes; NOT added to the JSON schema.

## 3. ID Strategy

Adopt strict semantic slugs: `kg.{kind}.{subcategory}.{slug}`.

- Example: `kg.grammar.ending.sumndia` (Retract numerical indexing from source).

## 4. Wave Plan

| Wave | Name | Scope | Risk |
| :--- | :--- | :--- | :--- |
| **Wave 0** | Foundation | Inventory, Canonical Mapping, Taxonomy alignment | Low |
| **Wave 1** | Batch 001 | 35-40 essential items (High-value, Low-risk) | Low |
| **Wave 2** | Beginner Grammar | 141 items from `youtube_beginner_grammar` | Med |
| **Wave 3** | Core Connectors | 113 items from `youtube_connectors` | Med |
| **Wave 4** | Survival Patterns | 180+ items from `survival_pattern_library` | High |
| **Wave 5** | Adv. Endings | 112 items from `connective_endings` | High |

## 5. Batch 001 Proposal (35-40 items)

| Type | Count | Scope |
| :--- | :--- | :--- |
| **Grammar** | 15 | Basic Particles (`이가`, `은는`, `을를`), Copula (`입니다`, `이에요`). |
| **Connector** | 12 | Top Connectors (`그리고`, `그래서`, `그런데`, `하지만`). |
| **Pattern** | 10 | Essential Survival Patterns (Greeting, Self-Intro). |

## 6. Guardrails / Non-Goals

- **NO** modifications to existing `core+i18n` JSON pack contract.
- **NO** changes to frontend intake `CompositionIntakeSpec`.
- **NO** schema changes for `media_id` or `source_order`.
- **DEFER** B1+ segmentation and advanced endings to later waves.
