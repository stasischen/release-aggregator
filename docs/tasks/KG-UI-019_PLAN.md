# Plan: Dictionary-to-Grammar Deep Linking UI (kg-ui-019)

This plan outlines the design and implementation phases for providing learners with immediate access to detailed grammar explanations from dictionary entries.

## User Review Required

> [!IMPORTANT]
> **Design Decisions for Discussion**:
> 1.  **Label**: Using "文法詳解" (Grammar Detail) to clearly differentiate from example sentences.
> 2.  **Web UI**: Implementing as a Right-side Drawer. We need to ensure it doesn't conflict with existing navigation elements.
> 3.  **Loading State**: Overlay will open immediately with a skeleton/loading state rather than waiting for data.

## Proposed Changes

### [release-aggregator](file:///c:/githubs/release-aggregator)

#### [NEW] [KG-UI-019_PLAN.md](file:///c:/githubs/release-aggregator/docs/tasks/KG-UI-019_PLAN.md)
- Formalize the design discussion and implementation steps.

#### [NEW] [KG-UI-019_TASKS.json](file:///c:/githubs/release-aggregator/docs/tasks/KG-UI-019_TASKS.json)
- Task tracking for frontend implementation (Note: AI will only discuss/plan, not execute frontend code).

#### [MODIFY] [MACHINE_STATUS.md](file:///c:/githubs/release-aggregator/docs/tasks/MACHINE_STATUS.md)
- Ensure status is correctly reflected as `in_progress`.

---

## Implementation Phases (Design & Coordination)

### Phase 1: Logic & Data Mapping
- [ ] Confirm `dict_grammar_mapping.json` format and initial data.
- [ ] Define the exact heuristic-to-manual resolution logic for `DictionaryResolver`.

### Phase 2: UI Design (Mockup/Logic)
- [ ] **Entry Point**: Define the visual style of the "文法詳解" chip in `DictionaryMeaningSection`.
- [ ] **Overlay**: Design the `GrammarDetailOverlay` components for both Mobile (Bottom Sheet) and Web (Drawer).
- [ ] **Multi-Link Support**: Define the UI behavior when a sense has multiple `grammar_refs`.

### Phase 3: Fail-soft & Error Handling
- [ ] Document specific UI states for: "Asset Not Found", "Network Error", and "Partial Resolution".

---

## Verification Plan

### Manual Verification
- Review design documents and mapping samples.
- Verify that `MACHINE_STATUS.md` and `local.json` are correctly updated.
