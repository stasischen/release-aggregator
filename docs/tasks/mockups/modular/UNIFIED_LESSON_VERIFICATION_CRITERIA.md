# Unified Lesson Verification Criteria (ULV)

This document outlines the heuristic evaluation and automated check criteria for the ULV runtime. These are intended for future pipeline use and for consistency among rendering modules.

## 1. Fixture Shape Checks
- **Primary Type Verification**:
    - `dialogue`: Must contain `payload.dialogue_turns` OR `payload.dialogue_scenes`.
    - `video`: Must specify `media_type: video` (Wait for production).
    - `article`: Must specify `media_type: text` (Wait for production).
- **Support Field Alignment**:
    - If `content_form` indicates patterns, `payload.pattern_lab` or `payload.lesson_support_module` must be present.
    - If `grammar` is requested in metadata, `payload.grammar_summary` or `payload.grammar_note` must be present.

## 2. State Transition Checks
- **Surface Resilience**:
    - Moving from `currentIndex=0` to `currentIndex=1` must correctly re-render the Primary Surface without horizontal scroll ghosts.
    - If the Support Panel is open at `index=0`, it must display appropriate content for `index=1` within < 200ms of the transition.
- **Anchor Sync**:
    - Selecting an element (`activePrimaryAnchor`) must not cause a layout shift or unexpected panel closure.

## 3. Missing-Data & Fail-Soft Checks
- **Reserved Slots**:
    - When a "Reserved" surface (e.g., `vocab`) is triggered, the UI must show a "Feature in Preview" or "Reserved Slot" message rather than an empty page.
- **Fatal Error Handling**:
    - If the `payload` is missing or is an invalid JSON shape, the runtime must invoke the **Data Inspector** component showing the raw error and the problematic node ID.

## 4. Contract Mismatch Reporting
- **In-Viewer UI**:
    - During mock testing, mismatches (e.g., a dialogue node with only grammar data) should trigger a subtle toast or banner: `Contract Mismatch: Expected dialogue data, found grammar summary`.
- **Validation Heuristics**:
    - `Warning`: Missing optional support field (e.g., `Notice` missing in a Grammar node).
    - `Error`: Missing mandatory primary field (e.g., `Dialogue turns` missing in a Dialogue node).
