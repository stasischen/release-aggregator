# AGG-GEN-016 Multilingual Curriculum Architecture Blueprint

## 1. Overview

This document defines the architecture for supporting multiple target languages and learner locales within the Lingourmet content ecosystem. The core principle is the separation of **Target Language Core** assets from **Learner Locale Pedagogy Overlays**.

## 2. Core vs. Overlay Separation

### 2.1 Target Language Core (TLC)
The TLC contains assets that are invariant regardless of the learner's native language.
- **Location**: `/data/courses/{target_lang}/{level}/{unit_id}/`
- **Contents**:
  - `dialogue.yarn`: Dialogue logic and branching.
  - `audio/`: Raw audio recordings in the target language.
  - `visuals/`: Image/video assets for the target language.
  - `manifest.json`: List of items, structure, and pointers to assets.

### 2.2 Learner Locale Pedagogy Overlay (LLPO)
The LLPO contains translations, explanations, and pedagogical strategies tailored to a specific learner group (e.g., Traditional Chinese speakers learning Korean).
- **Location**: `/data/courses/{target_lang}/locales/{learner_locale}/{level}/`
- **Contents**:
  - `{lesson_id}.md`: Human-readable pedagogical notes, cultural tips, and translations.
  - `{lesson_id}.csv`: Structured data for flashcards, matching, and retrieval exercises.
  - `local_overrides.json`: Locale-specific difficulty adjustments or alternative paths.

## 3. Directory Conventions (lllo alignment)

Content should follow the structure established in the `lllo` repository:

```text
lllo/data/courses/
  ├── ko/                      # Target Language: Korean
  │   ├── A1/                  # Standard CEFR Level
  │   │   ├── L01-Intro/       # Lesson ID
  │   │   │   └── dialogue.yarn
  │   ├── locales/             # Learner Overlays
  │   │   ├── zh-TW/           # Learner Locale: Traditional Chinese
  │   │   │   ├── A1/
  │   │   │   │   ├── L01-Intro.md
  │   │   │   │   └── L01.csv
  │   │   ├── en-US/           # Learner Locale: English (Future)
  │   │   │   └── ...
```

## 4. Multilingual Generation Flow

When a content candidate is generated, it contains both Core and Overlay information. The ingestion pipeline (Adapters) is responsible for partitioning this data.

1.  **Generation Brief**: Specifies `target_language` and `learner_locale`.
2.  **Candidate Payload**: Contains `foreign_preview` (Core) and `title_zh_tw`, `review_summary_zh_tw` (Overlay).
3.  **Acceptance**: Reviewer approves the candidate.
4.  **Catalog/Backlog Adapter**:
    - Writes Core logic to `content-{target_lang}` (e.g., `content-ko`).
    - Writes Overlay details to `lllo/data/courses/{target_lang}/locales/{learner_locale}/`.

## 5. Schema Support for Multilingualism

To support this architecture, candidates must explicitly tag their intended learner locale and provide structured links between concepts.

- **Mandatory Locale Tags**: Every candidate must define its `target_language` and primary `learner_locale`.
- **Resource Linking**: Candidates must explicitly list dependencies on existing lessons, grammar notes, or dictionary terms to allow the UI to bridge the Core and Overlay effectively.
