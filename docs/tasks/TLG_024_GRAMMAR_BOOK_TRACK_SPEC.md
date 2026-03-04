# TLG-024 Grammar Book Track Spec v1

## 1) Objective

Define a dedicated grammar-focused curriculum track that reuses legacy KO grammar assets while staying compatible with TLG index layers and viewer contracts.

This track is **not** the survival primary spine. It is a structured grammar reference/learning path, similar to a grammar textbook.

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_024_GRAMMAR_BOOK_TRACK_SPEC.md`
- Schema: `docs/tasks/schemas/tlg024_grammar_book_track_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_grammar_book_track_a1_l01_l10_v1.json`
- Cross-link map: `docs/tasks/indexes/ko_survival_grammar_crosslink_a1_v1.json`

---

## 3) Data Model

### Root

- `track_id`, `version`, `target_lang`, `support_langs`, `level`, `generated_at`
- `source_refs`:
  - legacy dialogue source
  - legacy grammar source
  - lllo curriculum map source
- `chapters[]`

### chapter item

- `chapter_id`: e.g. `KO-A1-GBOOK-CH01`
- `title_zh_tw`, `title_en`
- `lesson_ids[]`

### lesson item

- `lesson_id`: e.g. `KO-A1-GB-L01`
- `sequence_no`
- `delivery_mode`: fixed `dialogue_first`
- `legacy_ref`:
  - `lllo_directory_name` (e.g. `L01-N-ieyo-Identification`)
  - `content_ko_lesson_id` (e.g. `A1-01`)
- `anchor_dialogue`:
  - `source_segment_id` (e.g. `A1-01-D1`)
  - `line_window` (e.g. `1-8`)
  - `teaching_goal_zh_tw`
- `content_integration`:
  - `micro_text_theme` (same lesson theme, short reading/notice/message)
  - `communicative_task` (what learner does after grammar explanation)
  - `activation_prompt_zh_tw` (guided production prompt)
- `grammar_focus_id` (TLG-021 grammar id)
- `grammar_subpoints[]`
- `teaching_structure`:
  - `form`
  - `meaning`
  - `use`
  - `minimal_pair`
  - `common_errors`
- `example_sources[]` (legacy dialogue segment ids)
- `practice_blueprint[]` (recognize/fill/transform/build)
- `bridge_to_survival[]` (survival lesson ids)

---

## 4) Curriculum Policy

1. Grammar book track follows grammar progression, not scenario mission progression.
2. Every grammar lesson must link to at least one survival lesson.
3. Every grammar lesson must define form/meaning/use and a confusion repair hook.
4. Legacy dialogue is used as example bank, not as fixed lesson structure.
5. Every grammar lesson starts with an anchor dialogue (`delivery_mode=dialogue_first`).
6. Every grammar lesson must include content integration to avoid isolated rule memorization.

---

## 5) Checker Rules

### Blocker

- `ERR_GBOOK_SCHEMA_INVALID`
- `ERR_GBOOK_DUP_SEQUENCE`
- `ERR_GBOOK_MISSING_FMU` (missing form/meaning/use)
- `ERR_GBOOK_NO_SURVIVAL_BRIDGE`
- `ERR_GBOOK_EMPTY_PRACTICE_BLUEPRINT`

### Warning

- `WARN_GBOOK_NO_MINIMAL_PAIR`
- `WARN_GBOOK_WEAK_EXAMPLE_SOURCE`

---

## 6) DoD

1. TLG-024 spec + schema + sample + cross-link file committed.
2. A1 first 10 grammar-book lessons included.
3. Each lesson has non-empty bridge_to_survival.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` includes `TLG-024` = `done`.
5. `TASK_INDEX.md` progress updated.
