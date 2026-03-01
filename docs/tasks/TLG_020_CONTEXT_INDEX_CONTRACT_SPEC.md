# TLG-020 Context/Scenario Index Contract v1

## 1) Objective

Define a scenario index (`context -> lessons`) for use-case discovery (travel/life/work), retrieval, and sequencing.

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_020_CONTEXT_INDEX_CONTRACT_SPEC.md`
- Schema: `docs/tasks/schemas/tlg020_context_index_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_context_index_v1.sample.json`

---

## 3) Data Model

### Root

- `index_id`, `version(v1)`, `target_lang`, `support_langs`, `generated_at`, `entries`

### Entry

- `context_id` (e.g. `CTX-KO-TRAVEL-ORDERING-CAFE`)
- `label_zh_tw`, `label_en`
- `domain` (e.g. `travel`)
- `subdomain`
- `level_range`
- `lesson_refs[]`
- `function_refs[]`
- `pattern_refs[]`
- `grammar_refs[]`
- `transfer_contexts[]`
- `task_outcomes[]`

### lesson_refs item

- `lesson_id`
- `role` enum: `primary | secondary | review`
- `coverage_score` in `[0,1]`
- `evidence[]`

---

## 4) Checker Rules

### Blocker

- `ERR_CIDX_SCHEMA_INVALID`
- `ERR_CIDX_MISSING_PRIMARY`
- `ERR_CIDX_BAD_COVERAGE_SCORE`
- `ERR_CIDX_DUP_CONTEXT_ID`

### Warning

- `WARN_CIDX_NO_TRANSFER_CONTEXT`
- `WARN_CIDX_NO_GRAMMAR_REFS`
- `WARN_CIDX_EN_STUB`

---

## 5) DoD

1. Schema + ko sample committed.
2. Sample has >= 10 entries.
3. Schema validation passes.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-020` as `done`.
5. `TASK_INDEX.md` progress updated.
