# TLG-022 Pattern Index Contract v1

## 1) Objective

Define a pattern-centric index (`pattern/frame alias -> lessons`) with cross-links to function/grammar/context indices.

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_022_PATTERN_INDEX_CONTRACT_SPEC.md`
- Schema: `docs/tasks/schemas/tlg022_pattern_index_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_pattern_index_v1.sample.json`

---

## 3) Data Model

### Root

- `index_id`, `version(v1)`, `target_lang`, `support_langs`, `generated_at`, `entries`

### Entry

- `pattern_id` (must match pattern library id)
- `frame`
- `aliases[]`
- `level`
- `lesson_refs[]`
- `function_refs[]`
- `grammar_refs[]`
- `context_refs[]`
- `transform_types[]`
- `repair_links[]`
- `teaching_hint.{zh_tw,en}`

### lesson_refs item

- `lesson_id`
- `role` enum: `primary | reinforce | review`
- `coverage_score` in `[0,1]`
- `evidence[]`

---

## 4) Checker Rules

### Blocker

- `ERR_PIDX_SCHEMA_INVALID`
- `ERR_PIDX_PATTERN_NOT_FOUND`
- `ERR_PIDX_BAD_COVERAGE_SCORE`
- `ERR_PIDX_MISSING_PRIMARY`

### Warning

- `WARN_PIDX_NO_FUNCTION_REF`
- `WARN_PIDX_NO_GRAMMAR_REF`
- `WARN_PIDX_NO_CONTEXT_REF`

---

## 5) DoD

1. Schema + ko sample committed.
2. Sample has >= 12 entries.
3. Schema validation passes.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-022` as `done`.
5. `TASK_INDEX.md` progress updated.
