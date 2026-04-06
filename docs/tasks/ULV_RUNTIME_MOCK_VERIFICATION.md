# ULV Runtime Mock Verification Guide

## Goal

Verify that the **Unified Lesson View (ULV)** runtime contract is correctly implemented and capable of handling real content from both modular lessons and the Knowledge Lab. This serves as the final gate before Flutter implementation.

## Verification Scope

### 1. Primary Content Verification

- **Dialogue**: Use `A1-01.json`. Verify that the renderer handles `dialogue_turns` and `resolvedTranslation` correctly.
- **Video**: Use a lesson with a video slot. Verify the `ready` / `not_available` state handling.
- **Article**: Verify structured text rendering and emphasis states.

> [!WARNING]
> During ULV_RUNTIME_MOCK_VERIFICATION, you must ensure that all fixtures for video and article rendering are real source-build artifacts and not just reserved-slot placeholders or hand-authored stubs.

### 2. Support Detail Verification

- **Knowledge Lab Mapping**: Use actual grammar points linked from `A1-01`.
- **Surface Accuracy**: Verify that `pattern`, `grammar`, and `usage` surfaces match the expected `core+i18n` layout.
- **Vocab Reserved Slot**: Verify that accessing a vocab panel (reserved) results in a clean "Not available" or empty-state display without crashing.

### 3. Interaction & State Coordination

- **Anchor Activation**: Selecting a word with a knowledge-link must activate the correct support panel.
- **Panel Selection**: Switching between Support (Details) and Primary (Content) panels must not reset content state.
- **Pattern Lab Persistence**: Selections made in the Pattern Lab must persist while the lesson is active.

### 4. Fail-Soft & Legacy Coverage

- **Legacy Fallback**: Verify that `zh_tw` / `en` fields are resolved as a fallback to `translations_i18n`.
- **Missing Metadata**: Verify that nodes missing optional metadata do not crash the renderer.
- **Activity Co-existence**: Ensure that `practice_card` and `review_card` rendered via the modular viewer do not overlap or conflict with the ULV shell boundaries.

## Completion Criteria

Completion of this task is a mandatory prerequisite for starting **UNIFIED_LESSON_VIEW_FLUTTER_TRANSFER**.
