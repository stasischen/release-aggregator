# Unified Lesson View Architecture (ULV)

## Overview

The **Unified Lesson View (ULV)** defines a stable information architecture (IA) for the lesson runtime. It sits above the `MODULAR_VIEWER_REFACTOR` base, providing a consistent contract for primary learning content and its associated support details.

This architecture ensures that regardless of the specific content type (e.g., a dialogue or a video), the learner interacts with a predictable interface consisting of a **Primary Surface** and an optional **Support Detail Panel**.

## 1. Runtime Surface Taxonomy

We distinguish between the main learning carrier and the supplemental linguistic data.

### 1.1 Primary Content Surface
The "Hero" area of the lesson node. Only one primary surface is active at a time.

| Surface | Purpose | Mock Mapping (`content_form`) |
| :--- | :--- | :--- |
| **Dialogue** | Conversation-based immersion and input. | `dialogue` |
| **Video** | Video-based listening and situation immersion. | *Reserved* |
| **Article** | Text-based reading and comprehension. | *Reserved* |

### 1.2 Support Detail Surface
Supplemental panels providing deeper insight into the primary content. These are usually triggered by a selection (anchor) in the primary surface.

| Surface | Purpose | Mock Mapping (`content_form` / payload) |
| :--- | :--- | :--- |
| **Grammar** | Rule explanations and conjugation details. | `grammar_summary`, `grammar_note` |
| **Pattern** | Interactive sentence structures and builders. | `pattern_lab`, `pattern_builder_demos` |
| **Usage** | Nuance, social context, and "what to notice". | `what_to_notice_i18n`, `lesson_support_module` |
| **Vocab** | Individual word definitions and glosses. | *Reserved* |

---

## 2. Selection & Navigation State

The ULV runtime maintains a clear separation between the *surface content* and the *interaction state*.

### 2.1 Navigation State
Tracks the learner's position and global preferences within the lesson.

- `currentIndex`: The integer index of the active node in the lesson sequence.
- `teachingLocale`: The active learner-facing language (e.g., `zh_tw`, `en`).
- `bilingualVisibility`: Boolean flag to show/hide translations.

### 2.2 Selection State (Interaction)
Tracks the active focus within a node.

- `selectedNodeId`: Persistent ID of the current step.
- `activePrimaryAnchor`: The specific element selected in the primary surface (e.g., `sentence_01`, `timestamp_12.5`).
- `activeSupportType`: The type of support panel currently expanded (e.g., `grammar`, `usage`).

---

## 3. Out-of-Scope Activity Surfaces

The following `content_form` types are considered **Activity Surfaces**. They coexist with the ULV runtime but are not governed by the Primary/Support coordination logic defined here:
- `practice_card` (Chunk assembly, response builder, etc.)
- `review_card` (Flashcards, retrieval, etc.)

---

## 4. Mapping Strategy

| Mock Source Field | ULV IA Role | Integration Rule |
| :--- | :--- | :--- |
| `learning_role` | Meta-data for Navigation | Used for sidebar categorization and stage labels. |
| `payload.what_to_notice_i18n` | **Usage** Support | Maps to the top-level or bottom-docked Usage Support panel. |
| `payload.lesson_support_module`| **Usage** Support | Maps to a dedicated Support Detail view. |
| `payload.pattern_builder_demo` | **Pattern** Support | Triggers Pattern Lab renderer in the Support Detail Panel. |

## 6. Implementation Boundary
83: 
84: The ULV defines the *what* and the *why* of the lesson architecture. The transition to the Flutter implementation is governed by the **Flutter Transfer Boundary**.
85: 
86: ### 6.1 Flutter Shell vs. Runtime Contract
87: - **Runtime Contract (Frozen)**: Core information architecture, state names, and taxonomy that must remain stable.
88: - **Flutter Shell (Flexible)**: Implementation-specific details like widget composition, layout regions, and state management choices.
89: 
90: For detailed rules on adapter resolution, acceptance criteria, and remaining gaps, see the [Unified Lesson View: Flutter Transfer Boundary](UNIFIED_LESSON_VIEW_FLUTTER_BOUNDARY.md) document.
91: 
92: ---
93: 
94: ## 7. Metadata Boundaries
95: 
96: ### 7.1 Primary Metadata
97: Every node in the ULV runtime must resolve:
98: 
99: - `displayTitle`: Localized title for the current step.
100: - `displaySummary`: Localized "goal" of the step.
101: - `displayExpected`: Localized "expected output" description.
102: 
103: ### 7.2 Missing-Data Behavior
104: If a primary surface is requested but the payload is malformed or missing mandatory fields:
105: 
106: - **Fail-Soft**: Render a "Content Not Available" placeholder with a raw data preview for debugging.
107: - **Support Fallback**: If a specific support panel (e.g., `vocab`) is triggered but no data is available for the current anchor, display a "No additional details for this selection" message.
