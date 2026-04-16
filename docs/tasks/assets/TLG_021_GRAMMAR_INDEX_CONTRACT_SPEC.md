# TLG-021 Grammar Topic Index Contract v1

## 1) Objective

Define a machine-readable grammar index contract for:

- learner navigation (`我想學某文法 -> 哪些課可學`)
- generator retrieval (`grammar goal -> candidate lessons/patterns`)
- gate validation (`core/support/review role consistency`)

This contract is language-agnostic at schema level, with language-specific values in each index file (v1 sample uses Korean `ko`).

---

## 2) Output Artifacts

- Spec: `docs/tasks/TLG_021_GRAMMAR_INDEX_CONTRACT_SPEC.md`
- Schema: `docs/tasks/schemas/tlg021_grammar_index_v1.schema.json`
- Sample data: `docs/tasks/indexes/ko_grammar_index_v1.sample.json`

---

## 3) Data Model

### 3.1 Root

- `index_id` (string, required): e.g. `KO-GRAMMAR-INDEX-V1`
- `version` (string, required): fixed `v1`
- `target_lang` (string, required): ISO-ish code, e.g. `ko`
- `support_langs` (array<string>, required): default `["zh_tw","en"]`
- `generated_at` (string, required): `YYYY-MM-DD`
- `entries` (array<object>, required, min 1)

### 3.2 Entry

- `grammar_id` (string, required): `G-{LANG}-{SLUG}`, e.g. `G-KO-COPULA-IEYO-YEYO`
- `label_ko` (string, required for `ko`)
- `label_zh_tw` (string, required)
- `label_en` (string, required; stub allowed in v1 if not empty)
- `category` (enum, required): `morphology | syntax | pragmatic | discourse`
- `level_range` (object, required): `{ "min": "A1..C2", "max": "A1..C2" }`, `min <= max`
- `aliases` (array<string>, required): user-search aliases
- `lesson_refs` (array<object>, required, min 1)
- `pattern_refs` (array<string>, required): `pattern_id` list (can be empty if planned)
- `function_refs` (array<string>, required): `function_id` list (can be empty if planned)
- `prerequisite_grammar_ids` (array<string>, required)
- `related_grammar_ids` (array<string>, required)
- `teaching_hint` (object, required): `{ "zh_tw": string, "en": string }`
- `common_confusions` (array<object>, required)

### 3.3 lesson_refs item

- `lesson_id` (string, required): e.g. `KO-A1-L01`
- `role` (enum, required): `core | support | review`
- `coverage_score` (number, required): `0.0 .. 1.0`
- `evidence` (array<string>, required): source pointers, e.g. `grammar_notes:L01-G2`

### 3.4 common_confusions item

- `confusion_id` (string, required)
- `description_zh_tw` (string, required)
- `repair_strategy_id` (string, optional): should resolve in repair registry if provided

---

## 4) Mapping Rules

### 4.1 To TLG-004 Pattern Library

- `pattern_refs[]` must resolve to existing `pattern_id` in `ko_survival_pattern_library_v1.json`.
- At least one `core` lesson of each grammar entry should map to at least one pattern with matching usage intent.

### 4.2 To TLG-019/020/022

- `function_refs[]` can be used as join key to function index (TLG-019).
- grammar index is joinable with context/pattern index via `lesson_id` and `pattern_refs`.

### 4.3 To TLG-005/006

- Generator retrieval priority: `core > support > review`.
- Gate checks must verify:
  - missing `core` for high-frequency A1/A2 grammar => blocker
  - `coverage_score` outside range => blocker
  - duplicate `(grammar_id, lesson_id, role)` => blocker

---

## 5) Checker Rules

### Blocker

- `ERR_GIDX_SCHEMA_INVALID`: schema validation failed
- `ERR_GIDX_MISSING_CORE`: entry has no `core` lesson
- `ERR_GIDX_BAD_COVERAGE_SCORE`: score not in `[0,1]`
- `ERR_GIDX_INVALID_LEVEL_RANGE`: min CEFR above max CEFR
- `ERR_GIDX_PATTERN_NOT_FOUND`: unknown `pattern_id` in `pattern_refs`

### Warning

- `WARN_GIDX_EMPTY_FUNCTION_REFS`: no function mapping yet
- `WARN_GIDX_EN_STUB`: `label_en` or `teaching_hint.en` is too generic
- `WARN_GIDX_NO_REVIEW_ROLE`: no `review` mapping yet

---

## 6) Definition of Done (TLG-021 v1)

1. `tlg021_grammar_index_v1.schema.json` committed.
2. At least one `ko` sample index committed with >= 12 grammar entries.
3. All sample entries pass schema validation.
4. Sample entries include `core/support/review` role coverage (not required for every entry, but present in dataset).
5. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-021` as `done`.
6. `TASK_INDEX.md` progress updated.

---

## 7) Acceptance Commands

```bash
jq empty /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/indexes/ko_grammar_index_v1.sample.json

python3 - <<'PY'
import json, pathlib
from jsonschema import validate
root = pathlib.Path("/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks")
schema = json.loads((root/"schemas/tlg021_grammar_index_v1.schema.json").read_text())
data = json.loads((root/"indexes/ko_grammar_index_v1.sample.json").read_text())
validate(instance=data, schema=schema)
print("tlg021 schema validation: OK")
PY
```
