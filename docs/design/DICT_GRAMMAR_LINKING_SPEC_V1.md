# Design Specification: Dictionary-to-Grammar Deep Linking (V1)

## 1. Overview
This specification defines the mechanism for linking dictionary entries (atoms, particles, endings) directly to detailed grammar explanations in the Knowledge Lab. The goal is to provide learners with "Immediate Knowledge" (Definitions) and "Deep Knowledge" (Grammar) in a seamless, non-intrusive flow.

## 2. Design Principles
*   **Progressive Disclosure**: Keep dictionary primary view simple; hide complex grammar details behind a "View Details" action.
*   **Context Preservation**: Use non-disruptive UI (Bottom Sheets / Side Drawers) instead of full-screen navigation where possible to maintain the reading flow.
*   **ID-Federation**: Use canonical `grammar_id` as the source of truth for linking.

## 3. Data Architecture

### 3.1 Schema Update (Dictionary Core)
The `senses` array in each dictionary entry now supports an optional `grammar_refs` field (array of strings), consistent with the system-wide convention (`knowledge_refs[]`, `source_refs[]`, `token_refs[]`).

```json
// core-schema/schemas/dictionary_core.schema.json → senses.items.properties
{
  "grammar_refs": {
    "type": "array",
    "items": { "type": "string" },
    "description": "Optional IDs of grammar points in the knowledge lab (e.g. ko:g:a1:l01:...)"
  }
}
```

### 3.2 Cardinality & Naming Convention

> [!IMPORTANT]
> **Decision: `grammar_refs[]` (plural array)**
> This aligns with all existing cross-reference fields in the project:
> - `knowledge_refs[]` in example sentences
> - `source_refs[]` in dictionary core
> - `token_refs[]` in grammar core
>
> Using a singular `grammar_ref: string` would create naming and type fragmentation across the schema, resolver, and UI layers.

**Rationale**: A single dictionary sense (e.g., the particle `-에서`) may legitimately link to multiple grammar points (e.g., location usage + comparison usage). Adopting the array form from the start avoids a future migration.

**UI Behavior**: When `grammar_refs` contains multiple IDs, the UI renders them as a list of links. The first item may be visually emphasized as the "primary" link.

### 3.3 Ingestion Authority & Reporting

> [!CAUTION]
> Heuristic matching MUST NOT directly produce published `grammar_refs`. All heuristic outputs are **candidates only** and require human review before publication.

**Authority Hierarchy** (highest priority first):
1. **Manual mapping table** (`scripts/data/dict_grammar_mapping.json`): Curated by content producers. Always wins.
2. **Heuristic candidates**: Auto-generated suggestions based on surface form matching. Written to a **staging report**, never directly into production assets.
3. **Empty (no link)**: If neither source provides a mapping, the field is omitted. No guessing.

**Conflict Resolution**: If manual mapping and heuristic disagree, manual mapping wins silently. The heuristic conflict is logged to the build report for awareness.

**Build Report Requirements**: Every dictionary build that processes `grammar_refs` MUST output:
- `resolved_count`: Number of senses with at least one confirmed `grammar_refs` link.
- `unresolved_candidates`: Senses where heuristic found a candidate but no manual mapping exists.
- `ambiguous_candidates`: Senses where heuristic found ≥2 candidates with similar confidence.
- `conflict_overrides`: Cases where manual mapping overrode a heuristic suggestion.

## 4. Frontend Implementation

### 4.1 Resolution Logic
*   **`DictionaryResolver`**: Must parse and expose `grammar_refs` (as `List<String>`) in the sense data model.
*   **ID Resolution**: Resolution goes through `GrammarNoteService` (existing), NOT through direct path construction. The resolver uses the grammar manifest index to locate the asset file. This decouples the dictionary from the grammar asset storage structure.

```
grammar_id → GrammarNoteService.loadNote(id) → GrammarNote
                  ↑ uses grammar_manifest.json internally
```

### 4.2 UI Components
*   **Entry Point**: A "文法詳解" chip/button in `DictionaryMeaningSection`.
*   **Visibility Rule**: Rendered if and only if at least one `grammar_refs` ID successfully resolves via the grammar manifest (see §4.3 for details).
*   **Preferred Display Mode**:
    *   **Mobile**: Persistent Bottom Sheet.
    *   **Web/Tablet**: Right-side Drawer.
*   **Content**: Render the specific `GrammarNote` markdown content within this overlay.

### 4.3 Runtime Fail-soft Behavior

> [!WARNING]
> The dictionary overlay must never crash or show a broken state due to grammar linking issues. All failure modes must degrade gracefully.

| State | UI Behavior |
|---|---|
| `grammar_refs` is empty or absent | No grammar link button shown. No placeholder. |
| `grammar_refs` present, asset loads successfully | Show "文法詳解" chip → opens overlay with content |
| `grammar_refs` present, asset not found in manifest | Hide the grammar link button silently. Log warning. |
| `grammar_refs` present, asset found but load fails (network/parse) | Show "文法詳解" chip → overlay shows inline error: "無法載入文法內容，請稍後再試" with retry button |
| Multiple `grammar_refs`, some resolve and some fail | Show links only for successfully resolved items |

**Entry Point Visibility Rule**: The "文法詳解" button is rendered if and only if at least one `grammar_refs` ID successfully resolves via the grammar manifest. Resolution check happens at build time of the dictionary widget, not on tap.

## 5. User Review & Feedback
> [!IMPORTANT]
> **Resolved Items**:
> 1. ~~Should we support multiple grammar links per sense?~~ → **Yes, `grammar_refs[]` adopted.**
> 2. ~~Singular or plural naming?~~ → **Plural, consistent with system convention.**
>
> **Open Items**:
> 1. Is the "文法詳解" label clear enough for learners? Alternative: "查看用法"
> 2. Does the "Side Drawer" approach fit our current Web UI layout constraints?
> 3. Final confirmation on the manual mapping table format (`dict_grammar_mapping.json`).

## 6. Implementation Phases

### Phase 1: Foundation (Current)
- [x] Update `dictionary_core.schema.json` with `grammar_refs[]`.
- [ ] Create initial `dict_grammar_mapping.json` with manually curated entries.
- [ ] Update Python build scripts with authority hierarchy and build report.

### Phase 2: Frontend UI
- [ ] Update `DictionaryResolver` to parse `grammar_refs`.
- [ ] Update `DictionaryMeaningSection` UI with entry point visibility rule.
- [ ] Implement `GrammarDetailOverlay` (Bottom Sheet/Drawer) with all fail-soft states.

### Phase 3: Integration & Verification
- [ ] End-to-end test: dictionary sense → grammar overlay renders correctly.
- [ ] Verify fail-soft: broken grammar_id → button hidden, no crash.
- [ ] Build report output validation.
