# Knowledge Lab Viewer Refactor Plan

## Goal

Align the **Knowledge Lab Viewer** with the **Unified Lesson View (ULV)** runtime contract to ensure consistent support-detail rendering (Grammar, Pattern, Usage, Vocab) across all lesson types.

## Technical Alignment

### 1. Support Detail Surface Coverage

- **Grammar Support**: Adopt `sections` with `title_i18n` and `explanation_md_i18n`. Ensure fallback to legacy `points_i18n` is implemented at the adapter layer.
- **Pattern Support**: Ensure `builder_id` scoped state persistence. Selections MUST NOT reset when switching between support panels.
- **Usage Support**: Render `items` as concise "Notice" cards or bulleted sets.
- **Vocab Support**: Implement **Reserved Slot** handling. Since there is no active upstream schema, the viewer must show a clean "Not available" or "Reserved" state rather than crashing.

### 2. Panel & Interaction Coordination

- Align with the ULV navigation contract: `primary/support panel coordination`.
- Selection states in the Knowledge Lab MUST sync with the ULV shell's `activePrimaryAnchor` and `activeSupportType` states.

### 3. Fail-Soft Rules

- **Missing Data**: Show a dedicated "No additional details available" notice for nodes with empty knowledge payloads.
- **Malformed Payloads**: Render a "Data Inspection" view (raw JSON) if the `content_form` is unrecognized.

## Verification

- **Real Content Test**: Validate with real `A1-01` components (e.g., Grammar point `kg.grammar.ending.sumndia`).
- **Interaction Test**: Verify that selecting a pattern in Pattern Lab persists correctly across panel switches.
