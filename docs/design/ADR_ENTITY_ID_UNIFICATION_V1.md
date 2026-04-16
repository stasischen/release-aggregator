# ADR 001: Knowledge and Pattern Entity ID Unification

## Status
**Proposed** (2026-04-16)

## Context
There is currently a divergence in ID naming conventions for Knowledge (Grammar, Expressions, etc.) and Pattern entities between the content library and the distribution/index layer:
- **Index Layer (GID)**: Uses coded identifiers like `G-KO-COPULA-IEYO-YEYO`. This is used by the Dictionary and Frontend for stable deep linking.
- **Content Layer (SID)**: Uses path-based identifiers like `kg.grammar.copula.present_polite_ieyo`. This is used by the Knowledge Lab and ingestion scripts for logical organization.

Without unification, the Canonical Sentence Graph cannot reliably link example sentences to both content sources and distribution indexes.

## Decision
We will adopt a **Dual-ID Registry** strategy:

1.  **Global ID (GID)**:
    *   **Format**: `[Type]-[Language]-[Family]-[Slug]` (e.g., `G-KO-COPULA-IEYO-YEYO`, `P-KO-SURVIVAL-001`).
    *   **Purpose**: Immutable primary key for cross-repo linking and user-facing features.
    *   **Source of Truth**: Distribution Indexes in `release-aggregator/docs/tasks/indexes/`.

2.  **Source ID (SID)**:
    *   **Format**: Dot-notated path (e.g., `kg.grammar.copula.present_polite_ieyo`).
    *   **Purpose**: Logical path for filesystem organization and content-ko repository management.
    *   **Source of Truth**: `content-ko` filesystem structure.

3.  **Mapping Requirement**:
    *   Every primary index (Grammar, Pattern, Topic) **MUST** include a `source_id` field in its metadata to map the GID to the SID.
    *   Example sentences stored in the Sentence Bank **MUST** prioritize GIDs in their `knowledge_refs[]`.

## Consequences
- **Pros**: Maintains stability for the frontend while allowing the content team to reorganize files as needed.
- **Cons**: Requires index maintenance to ensure mapping remains correct.
- **Next Steps**: Update `ko_grammar_index` and `ko_pattern_index` samples to include `source_id` fields.
