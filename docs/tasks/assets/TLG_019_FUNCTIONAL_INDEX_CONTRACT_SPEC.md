# TLG-019 Functional Outcome Index Contract v1

## 1) Objective

Define an index from communicative function (`can_do`) to lessons for:

- learner goal navigation
- generator filtering
- cross-index joins with grammar/context/pattern

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_019_FUNCTIONAL_INDEX_CONTRACT_SPEC.md`
- Schema: `docs/tasks/schemas/tlg019_functional_index_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_functional_index_v1.sample.json`

---

## 3) Data Model

### Root

- `index_id`, `version(v1)`, `target_lang`, `support_langs`, `generated_at`, `entries`

### Entry

- `function_id` (e.g. `F-REQUEST`)
- `label_zh_tw`, `label_en`
- `can_do_zh_tw`, `can_do_en`
- `level_range` (`A1..C2`)
- `lesson_refs[]`
- `pattern_refs[]`
- `grammar_refs[]`
- `context_tags[]`
- `prerequisite_function_ids[]`
- `teaching_hint.{zh_tw,en}`

### lesson_refs item

- `lesson_id`
- `role` enum: `core | support | review`
- `coverage_score` in `[0,1]`
- `evidence[]`

---

## 4) Checker Rules

### Blocker

- `ERR_FIDX_SCHEMA_INVALID`
- `ERR_FIDX_MISSING_CORE`
- `ERR_FIDX_BAD_COVERAGE_SCORE`
- `ERR_FIDX_DUP_LESSON_ROLE`

### Warning

- `WARN_FIDX_NO_PATTERN_REFS`
- `WARN_FIDX_NO_GRAMMAR_REFS`
- `WARN_FIDX_EN_STUB`

---

## 5) DoD

1. Schema + ko sample committed.
2. Sample has >= 10 entries.
3. Schema validation passes.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-019` as `done`.
5. `TASK_INDEX.md` progress updated.
