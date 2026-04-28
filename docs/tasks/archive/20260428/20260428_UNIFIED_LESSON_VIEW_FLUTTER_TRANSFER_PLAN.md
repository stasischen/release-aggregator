# Implementation Plan - Unified Lesson View Flutter Transfer (ULVFT)

This plan outlines the transfer of the frozen **Unified Lesson View (ULV)** contract into the Flutter frontend. It ensures a stable, predictable learning interface across different content types while maintaining a clear separation between primary content and support details.

## User Review Required

> [!IMPORTANT]
> The Shell design adopts a **Master-Detail** layout for wide screens (Web/Desktop/Tablet) and an **Overlay/Drawer** layout for narrow screens (Mobile). This ensures that support details can be viewed side-by-side with primary content when space permits.

> [!WARNING]
> We will prioritize **Dialogue** as the primary surface. **Video** and **Article** surfaces will initially use "Fail-Soft" placeholders until their specific schema threads are finalized.

## Proposed Changes

### 1. Flutter Shell Definition (ULVFT-001)

#### [MODIFY] [modular_lesson_runtime_shell.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/modular_lesson_runtime_shell.dart)
- Refactor to support **Master-Detail** layout.
- Define explicit regions: `PrimaryContentRegion`, `SupportDetailRegion`, `NavigationRegion`.
- Implement responsive switching between Side-Panel and Drawer/BottomSheet.

### 2. State & Data Models (ULVFT-002)

#### [MODIFY] [ulv_models.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/domain/models/ulv_models.dart)
- Ensure alignment with ULV contract fields: `activePrimaryAnchor`, `activeSupportType`, `activeSupportId`.
- Implement `SupportSurfaceType` enum if missing or incomplete.

#### [MODIFY] [modular_runtime_provider.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/providers/modular_runtime_provider.dart)
- Update `ModularSessionState` to strictly follow ULV semantics.
- Refine `selectAnchor` and `setSupportTarget` logic to ensure stability (already partially tested in `modular_runtime_stability_test.dart`).

### 3. Adapters & Renderers (ULVFT-003 & ULVFT-004)

#### [NEW] `lib/features/study/presentation/widgets/ulv/ulv_primary_surface_adapter.dart`
- A dispatcher widget that selects the correct renderer based on `contentForm`.

#### [NEW] `lib/features/study/presentation/widgets/ulv/ulv_support_surface_adapter.dart`
- A dispatcher widget that selects the correct support panel based on `activeSupportType`.

#### [MODIFY] Existing Renderers
- Update `ulv_dialogue_renderer.dart`, `ulv_grammar_renderer.dart`, etc., to use standard anchor/selection callbacks.

### 4. Integration & Mock Wiring (ULVFT-005)

#### [MODIFY] [modular_lesson_runtime_screen.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/screens/modular_lesson_runtime_screen.dart)
- Wire the new Shell and Adapters into the main runtime screen.

## Verification Plan

### Automated Tests
- **State Stability**: Run `modular_runtime_stability_test.dart` to ensure selection state logic is sound.
- **Layout Test**: Create `modular_lesson_runtime_shell_test.dart` to verify responsive layout (Side-Panel vs. Drawer).
- **Adapter Test**: Verify correct renderer dispatching for different `contentForm` types.

### Manual Verification
- Verify side-by-side layout on Web by triggering a support panel (e.g., tap a word/grammar point).
- Verify drawer/overlay layout on Mobile resolution.
- Verify "Fail-Soft" placeholders for unimplemented surfaces.
