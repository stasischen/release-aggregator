# Unified Lesson Verification Criteria (ULV)

This document outlines the heuristic evaluation and automated check criteria for the ULV runtime. These are intended for future pipeline use and for consistency among rendering modules.

## 1. Fixture Shape Checks
- **Primary Type Verification**:
    - `dialogue`: Must contain `payload.dialogue_turns` OR `payload.dialogue_scenes` (or be resolvable by the adapter).
    - `video`: Must be resolvable into a media playback slot at the runtime boundary.
    - `article`: Must be resolvable into a structured text slot at the runtime boundary.
- **Support Field Alignment**:
    - If `content_form` indicates patterns, `payload.pattern_lab` or `payload.lesson_support_module` must be present.
    - If `grammar` is requested in metadata, `payload.grammar_summary` or `payload.grammar_note` must be present.

## 2. State Transition Checks
- **Surface Resilience**:
    - Moving from `currentIndex=0` to `currentIndex=1` must correctly re-render the Primary Surface without horizontal scroll ghosts.
    - If the Support Panel is open at `index=0`, it must display appropriate content for `index=1` without perceptible delay.
- **Anchor Sync**:
    - Selecting an element (`activePrimaryAnchor`) must not cause a layout shift or unexpected panel closure.

## 3. Missing-Data & Fail-Soft Checks
- **Reserved Slots**:
    - When a "Reserved" surface (e.g., `vocab`) is triggered, the UI must show a "Feature in Preview" or "Reserved Slot" message rather than an empty page.
- **Fatal Error Handling**:
    - If the `payload` is missing or is an invalid JSON shape, the runtime must surface a contract-violation alert or diagnostic view showing the raw error and the problematic node ID.

## 4. Contract Mismatch Reporting
- **In-Viewer UI**:
    - During mock testing, mismatches (e.g., a dialogue node with only grammar data) should trigger a subtle toast or banner: `Contract Mismatch: Expected dialogue data, found grammar summary`.
- **Validation Heuristics**:
    - `Warning`: Missing optional support field (e.g., `Notice` missing in a Grammar node).
    - `Error`: Missing mandatory primary field (e.g., `Dialogue turns` missing in a Dialogue node).

## 5. Staging Recovery Gate (Dialogue/Video)
These criteria are specific to the `LEARNING_LIBRARY_CONTENTKO_MIGRATION` (LLCM) tasks for recovering legacy content into the new unified build artifacts.

- **Staging Intake Minimums**:
    - [ ] **Visibility**: Unit must appear in `fixtures.json` and load in the map.
    - [ ] **Bilingual Display**: Korean source + `zh_tw` translation must both load for all turns.
    - [ ] **Failure Resilience**: Missing `dialogue_atoms.json` MUST NOT crash the viewer; it should fall back to full-text turns.
    - [ ] **Video Atoms**: If atoms exist in `content/core/video_atoms/`, they must be visible in the viewer as interactive chips.
- **Accepted Mismatches (Deferred)**:
    - **Dialogue Atom Lack**: It is currently **ACCEPTED** that Dialogue artifacts lack word-level segmentation in Staging.
    - **Volume Differential**: It is **ACCEPTED** that Artifact Mode contains more turns than the original Prototype Seed.
