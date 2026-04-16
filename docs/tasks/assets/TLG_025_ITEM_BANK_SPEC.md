# TLG-025 Item Bank Spec v1

## 1) Objective

Define a reusable item bank contract so course nodes can be converted into quiz-style review sets (like a question bank).

This unlocks:

- lesson-based review
- grammar-targeted review
- weak-point review
- mock test assembly

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_025_ITEM_BANK_SPEC.md`
- Schema: `docs/tasks/schemas/tlg025_item_bank_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_item_bank_a1_gb_l01_v1.json`
- Script: `scripts/tlg025_generate_item_bank_from_unit.py`

---

## 3) Data Model

### Root

- `bank_id`, `version`, `target_lang`, `support_langs`, `level`, `generated_at`
- `source_unit_id` (e.g. `A1-GB-L01-LEGACY`)
- `items[]`

### item

- `item_id`
- `item_type` enum:
  - `mcq_meaning`
  - `cloze`
  - `transform`
  - `retrieval`
- `skill` enum: `reading | listening | grammar | speaking | writing`
- `difficulty_tier` enum: `L1 | L2 | L3`
- `prompt_zh_tw`
- `prompt_ko` (optional)
- `choices` (for MCQ/Cloze)
- `answer_key`
- `explanation_zh_tw`
- `linked_refs`:
  - `lesson_id`
  - `node_id`
  - `grammar_ids[]`
  - `pattern_ids[]`
  - `function_ids[]`
- `tags[]`
- `review_policy`:
  - `initial_interval_days`
  - `wrong_interval_days`
  - `correct_fast_interval_days`

---

## 4) Generation Rules

1. At least 60% of items should be directly grounded in source unit content.
2. Every item must carry `linked_refs` for traceability.
3. Grammar lesson item banks must include at least:
   - one `mcq_meaning`
   - one `cloze`
   - one `transform` or `retrieval`

---

## 5) Checker Rules

### Blocker

- `ERR_IBANK_SCHEMA_INVALID`
- `ERR_IBANK_DUP_ITEM_ID`
- `ERR_IBANK_EMPTY_ITEMS`
- `ERR_IBANK_MISSING_LINKED_REFS`
- `ERR_IBANK_NO_ANSWER_KEY`

### Warning

- `WARN_IBANK_LOW_SOURCE_GROUNDED_RATIO`
- `WARN_IBANK_SINGLE_TYPE_ONLY`
- `WARN_IBANK_MISSING_GRM_COVERAGE`

---

## 6) DoD

1. TLG-025 spec/schema/sample/script committed.
2. Sample has >= 20 items.
3. Sample passes schema validation.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` includes `TLG-025` as done.
5. `TASK_INDEX.md` progress updated.
