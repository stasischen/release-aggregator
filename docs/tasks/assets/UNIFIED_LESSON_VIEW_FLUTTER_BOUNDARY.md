# Unified Lesson View: Flutter Transfer Boundary

This document defines the interface and responsibilities between the frozen **Unified Lesson View (ULV)** architecture and the **Flutter (Mobile/Web)** implementation.

## 1. Contract-Stable Before Flutter (Must Not Change)
These elements are core to the ULV architecture and must be preserved during the Flutter transfer. Any adaptation must occur within the Flutter Adapter layer.

- **Surface Taxonomy**: The distinction between Primary (Dialogue, Video, Article) and Support (Grammar, Pattern, Usage, Vocab) surfaces.
- **State Names & Semantics**: 
    - `currentIndex`: Global node navigation.
    - `activePrimaryAnchor`: The specific focus within a node.
    - `activeSupportType`: The currently active detail panel.
    - `teachingLocale` / `bilingualVisibility`: Global learner preferences.
- **Support Context Anchor**: The mechanism where selecting a primary element (anchor) filters or scrolls the support detail.
- **Fail-Soft Expectations**: Placeholders for reserved slots and raw data views for malformed payloads.
- **State Boundaries**: Clear separation between Ephemeral, Node-Scoped, and Session-Scoped state.

## 2. Flutter-Adaptable Concerns (Implementation Flexibility)
These details are local to the Flutter shell and do not affect the upstream contract.

- **Widget Composition**: How components are nested and modularized.
- **Layout Regions & Breakpoints**: Side-by-side vs. Overlay panels; Mobile vs. Desktop breakpoints.
- **UI Components**: Tab style, Drawer style, Bottom sheet vs. Side panel usage.
- **Animations & Transitions**: All micro-interactions and smooth state transitions.
- **State Management**: Choice of library (e.g., Bloc, Riverpod, Provider).
- **Renderer Internal Partitioning**: How a "Dialogue" is decomposed into individual line widgets.

## 3. Adapter Boundary Rules
The Flutter Adapter is the "translation layer" between the frozen JSON contract and the Flutter state models.

### 3.1 Allowed Actions
- **Legacy Resolution**: Resolve `translations_i18n` or legacy `zh_tw`/`en` keys into a single `resolvedTranslation` field.
- **Slot Normalization**: Map different payload shapes (e.g., `dialogue_turns` vs `dialogue_scenes`) into a uniform internal model.
- **Carrier Mapping**: Map specific mock fields (like `payload.what_to_notice_i18n`) into the frozen taxonomy roles (like `Usage` support).

### 3.2 Prohibited Actions (Hard Constraints)
- **Inventing Meaning**: Do not silently invent lesson logic not present in the source artifact.
- **Contract Expansion**: Do not add new mandatory requirements to the upstream build artifacts.
- **Reserved-Slot Stability**: Do not treat "Reserved" surfaces (Video/Article/Vocab) as having a stable *schema* until their specific task thread is opened.

---

## 4. Downstream Acceptance Criteria (READY for Transfer)
The following conditions must be met before beginning the `UNIFIED_LESSON_VIEW_FLUTTER_TRANSFER` implementation:

- **Documentation Parity**: `ULV-001` through `ULV-006` documents are consistent and cross-referenced.
- **Example Mapping**: At least 3 mock lessons (`lesson_01~03`) have a clear mapping path to the frozen runtime contract.
- **Boundary Clarity**: The transition between "Primary" and "Support" surfaces is unambiguous for all current content types.
- **Conflict-Free Contract**: No contradictions exist between the Interaction (Panel Flow) and State (Runtime Contract) specifications.
- **Heuristic Sufficiency**: Verification criteria are detailed enough to support a manual "Mock Review" of the Flutter implementation.

## 5. Remaining Gaps (Non-Blocking)
The following items are recognized gaps but do not block the start of the Flutter transfer:

- **Fixture Evidence**: Stable fixture examples for `video`, `article`, and `vocab` are still *Reserved*.
- **Anchor-to-Support Logic**: While the *semantics* are defined, the actual lookup implementation (e.g., metadata-driven or rule-driven) remains flexible.
- **Activity Surface Integration**: The specific placement of `practice_card` and `review_card` within the ULV shell is deferred to the Activity layer task.

## 6. Handoff Guidance for Flutter Transfer
- **Phase 1**: Implement the stable state models and the bare-bones Shell layout.
- **Phase 2**: Create the **Dialogue Adapter** first, as it is the most stable primary surface.
- **Phase 3**: Use the **Adapter** to mask legacy payload inconsistencies; do not request source-schema changes yet.
- **Phase 4**: Prioritize "Fail-Soft" rendering for reserved surfaces to ensure a crash-free experience during development.
