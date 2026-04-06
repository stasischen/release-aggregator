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
- **Display States**:
    - `listening_emphasis`: Target text at full opacity; translation at low opacity or hidden.
    - `reading_emphasis`: Target and translation both at full opacity.
    - `bilingual_visibility`: Boolean flag for the entire surface.

### 1.2 Video Surface (Slot)
- **Purpose**: Media-based listening and situation immersion.
- **Minimum Runtime Requirements**:
    - `media_type`: `video`.
    - `availability_state`: `ready` | `not_available` | `loading`.
- **Media Availability State**:
    - `ready`: Video player visible; source loaded.
    - `not_available`: Fallback UI (e.g., "Video currently in production").
- **Optional Slots**:
    - `subtitle_sync`: Aligned sentence nodes for the current timestamp.

### 1.3 Article Surface (Slot)
- **Purpose**: Narrative text comprehension.
- **Minimum Runtime Requirements**:
    - `body_i18n`: Localized markdown/text string.
- **Display States**:
    - `standard`: Full body visibility.
    - `focus_highlight`: Selection-based sentence highlighting.

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
    - Handle `pending` or `missing_data` state gracefully.
    - Minimum slot for `term_id` and `definition_i18n`.

---

## 3. Global Fail-Soft Rules

1. **Missing Support Panel**: If a node requests a support view (e.g., `grammar`) but the payload is empty, the UI should simply not render the "Details" tab or show a "No additional details available" notice.
2. **Unsupported Primary Content**: If `content_form` is unknown, the ULV must render a **Data Inspection Panel** showing the raw JSON payload to avoid a silent crash.
3. **Locale Mismatch**: Always prioritize `teachingLocale` -> `zh_tw` -> `en` resolution order.
