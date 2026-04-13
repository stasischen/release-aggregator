# Design Specification: Dictionary-to-Grammar Deep Linking (V1)

## 1. Overview
This specification defines the mechanism for linking dictionary entries (atoms, particles, endings) directly to detailed grammar explanations in the Knowledge Lab. The goal is to provide learners with "Immediate Knowledge" (Definitions) and "Deep Knowledge" (Grammar) in a seamless, non-intrusive flow.

## 2. Design Principles
*   **Progressive Disclosure**: Keep dictionary primary view simple; hide complex grammar details behind a "View Details" action.
*   **Context Preservation**: Use non-disruptive UI (Bottom Sheets / Side Drawers) instead of full-screen navigation where possible to maintain the reading flow.
*   **ID-Federation**: Use canonical `grammar_id` as the source of truth for linking.

## 3. Data Architecture

### 3.1 Schema Update (Dictionary Core)
The `senses` array in each dictionary entry now supports an optional `grammar_ref` field.

```json
// core-schema/schemas/dictionary_core.schema.json
{
  "properties": {
    "senses": {
      "items": {
        "properties": {
          "grammar_ref": {
            "type": "string",
            "description": "Optional ID of a grammar point (e.g., ko:g:a1:l01:n-이에요-예요)"
          }
        }
      }
    }
  }
}
```

### 3.2 Data Ingestion
*   The `content-pipeline` will be updated to inject valid `grammar_id`s into the dictionary assets during the build process, based on a mapping table or heuristic matching.

## 4. Frontend Implementation

### 4.1 Resolution Logic
*   **`DictionaryResolver`**: Must parse and expose `grammar_ref` in the `DictionaryEntry` model.
*   **ID Mapping**: The app must resolve a `grammar_id` to its corresponding Lesson Asset (e.g., `ko:g:a1:l01:...` -> `assets/content/grammar/ko__g__a1__l01__...json`).

### 4.2 UI Components
*   **Entry Point**: A "View Grammar Details" (文法詳解) button in the `DictionaryMeaningSection`.
*   **Display Mode**: 
    *   **Mobile**: Persistent Bottom Sheet.
    *   **Web/Tablet**: Right-side Drawer.
*   **Content**: Render the specific `GrammarNote` markdown content within this overlay.

## 5. User Review & Feedback
> [!IMPORTANT]
> **Review Items**:
> 1. Is the "Grammar Details" button label clear enough for learners?
> 2. Should we support multiple grammar links per sense? (Currently restricted to one).
> 3. Does the "Side Drawer" approach fit our current Web UI layout constraints?

## 6. Implementation Phases

### Phase 1: Foundation (Current)
- [x] Update `dictionary_core.schema.json` with `grammar_ref`.
- [ ] Update Python build scripts to test data injection.

### Phase 2: Frontend UI
- [ ] Update `DictionaryMeaningSection` UI.
- [ ] Implement `GrammarDetailOverlay` (Bottom Sheet/Drawer).

### Phase 3: Integration
- [ ] Implement deep-linking logic from ID to Asset loading.
- [ ] Final verification with live data.
