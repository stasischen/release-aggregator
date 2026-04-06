# Unified Lesson Runtime Contract

This document defines the technical contract for the **Unified Lesson View (ULV)** runtime. All renderers and adapters must adhere to these field requirements and state logic.

## 1. Primary Content Surface Contracts

### 1.1 Dialogue Surface
- **Purpose**: Interactive conversation display.
- **Mandatory Fields**:
    - `dialogue_turns`: Array of `Turn` objects (Legacy flat structure).
    - **OR** `dialogue_scenes`: Array of `Scene` objects (Modern grouped structure).
- **Turn Object**:
    - `speaker`: `A` or `B`.
    - `text`: Target language string (Korean).
    - `translations_i18n`: I18n object for the learner's language.
    - **OR** `zh_tw` / `en`: Legacy resolved translation keys (Acceptable for runtime resolution).
- **Runtime Responsibility**:
    - The **Adapter** is responsible for resolving either `translations_i18n` or legacy keys into a unified `resolvedTranslation` field for the renderer.
    - `listening_emphasis`: Target text at full opacity; translation at low opacity or hidden.
    - `reading_emphasis`: Target and translation both at full opacity.
    - `bilingual_visibility`: Boolean flag for the entire surface.

### 1.2 Video Surface (Slot Boundary)
- **Purpose**: Media-based listening and situation immersion.
- **Runtime Responsibility**:
    - The runtime (Adapter + Renderer boundary) must handle the availability of a media slot.
    - If `video` is requested, the system must resolve the appropriate playback capability or fallback.
- **Minimum Requirements**:
    - Handle `ready` | `not_available` | `loading` states.
- **Optional**:
    - Support for subtitle synchronization if provided by the payload.

### 1.3 Article Surface (Slot Boundary)
- **Purpose**: Narrative text comprehension.
- **Runtime Responsibility**:
    - The runtime must handle the resolution of a structured text body into a scrollable or paginated article view.
- **Minimum Requirements**:
    - Handle text emphasis states (e.g., standard vs. focus).

---

## 2. Support Detail Surface Contracts

### 2.1 Grammar Support
- **Source**: `grammar_summary`, `grammar_note`.
- **Contract**:
    - `sections`: Array of `{ title_i18n, explanation_md_i18n, points_i18n }`.
- **Fail-Soft**: If `sections` is empty, check for `points_i18n` (Legacy fallback).

### 2.2 Pattern Support
- **Source**: `pattern_lab`, `pattern_builder_demos`.
- **Contract**:
    - `builder_id`: Unique identifier for state persistence.
    - `controls`: List of `control_id`, `label_i18n`, and `options`.
    - `templates`: `register_templates` (Korean) and `translation_templates` (Glosses).
- **Persistence**: Selections in the Pattern Lab MUST be node-scoped persistent (won't reset when switching to a support panel and back).

### 2.3 Usage Support
- **Source**: `what_to_notice_i18n`, `lesson_support_module`.
- **Contract**:
    - `items`: Array of `{ target, explain_i18n }`.
- **Display**: Render as a bulleted list or "Notice" card.

### 2.4 Vocab Support (Slot)
- **Reserved Status**: No current upstream schema.
- **Runtime Requirement**:
    - Handle `pending` or `missing_data` state gracefully at the adapter/renderer boundary.

---

## 3. Global Fail-Soft Rules

1. **Missing Support Panel**: If a node requests a support view (e.g., `grammar`) but the payload is empty, the UI should simply not render the "Details" tab or show a "No additional details available" notice.
2. **Unsupported Primary Content**: If `content_form` is unknown, the ULV must render a **Data Inspection Panel** showing the raw JSON payload to avoid a silent crash.
3. **Locale Mismatch**: Always prioritize `teachingLocale` -> `zh_tw` -> `en` resolution order.
