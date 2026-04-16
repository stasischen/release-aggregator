# TLG-023 Dual-Track Course Map Spec v1

## 1) Goal

Define a unified map that supports:

- `functional` lessons (task-first outcomes)
- `grammar` lessons (form-first consolidation)

Both tracks share the same pattern/function/grammar/context indices and output the same viewer node contract.

---

## 2) Artifacts

- Spec: `docs/tasks/TLG_023_DUAL_TRACK_COURSE_MAP_SPEC.md`
- Schema: `docs/tasks/schemas/tlg023_course_track_map_v1.schema.json`
- Sample: `docs/tasks/indexes/ko_course_track_map_v1.sample.json`

---

## 3) Data Model

### Root fields

- `map_id` (string): e.g. `KO-A1-DUAL-TRACK-MAP-V1`
- `version` (string): fixed `v1`
- `target_lang` (string): e.g. `ko`
- `support_langs` (array<string>)
- `level` (string): e.g. `A1`
- `generated_at` (YYYY-MM-DD)
- `maintenance_note` (object): sync policy and markdown regeneration command
- `lessons` (array)

### Lesson object

- `lesson_id` (string): stable unit/lesson key
- `sequence_no` (integer >=1): global sequence
- `track_type` (enum): `functional | grammar`
- `title_zh_tw`, `title_en`
- `primary_objective_id` (string): key in function or grammar index
- `secondary_objective_ids` (array<string>)
- `context_ids` (array<string>)
- `pattern_ids` (array<string>)
- `grammar_ids` (array<string>)
- `function_ids` (array<string>)
- `prerequisites` (array<string>): lesson_id list
- `bridge_to_track` (object): cross-track navigation
- `node_profile` (object): expected viewer node composition

### bridge_to_track

- `recommended_next_functional_lesson_id` (nullable string)
- `recommended_next_grammar_lesson_id` (nullable string)
- `bridge_note_zh_tw` (string)
- `bridge_note_en` (string)

### node_profile

- `required_node_types` (array<string>): e.g. `L1,P1,P2,P5,R1`
- `max_nodes` (integer)
- `min_nodes` (integer)
- `must_include_anchor` (boolean): dialogue/text anchor required

---

## 4) Sequencing Policy

1. Functional spine first: learners gain immediate communicative ability.
2. Grammar lessons inserted as:
   - `unlock` (before functional bottleneck), or
   - `stabilize` (after repeated functional errors).
3. Every grammar lesson must point back to at least one functional lesson via `bridge_to_track`.
4. No isolated grammar-only chain longer than 2 lessons in A1/A2.

---

## 5) Checker Rules

### Blocker

- `ERR_TMAP_SCHEMA_INVALID`
- `ERR_TMAP_DUP_SEQUENCE_NO`
- `ERR_TMAP_TRACK_INVALID`
- `ERR_TMAP_MISSING_BRIDGE`
- `ERR_TMAP_NODE_PROFILE_INVALID` (`min_nodes > max_nodes` or empty required nodes)

### Warning

- `WARN_TMAP_NO_SECONDARY_OBJECTIVE`
- `WARN_TMAP_MISSING_CROSS_INDEX_REF`
- `WARN_TMAP_DENSE_GRAMMAR_CLUSTER` (>2 consecutive grammar lessons)

---

## 6) DoD

1. `tlg023_course_track_map_v1.schema.json` committed.
2. `ko_course_track_map_v1.sample.json` includes first 10 lessons with mixed `functional/grammar`.
3. Sample passes schema validation.
4. `TARGET_LANG_COURSE_FACTORY_TASKS.json` includes `TLG-023` and marks it `done`.
5. `TASK_INDEX.md` progress updated.

---

## 7) Acceptance Commands

```bash
jq empty /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/indexes/ko_course_track_map_v1.sample.json
jq empty /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/schemas/tlg023_course_track_map_v1.schema.json

python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/tlg023_course_track_codec.py \
  json-to-md \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/indexes/ko_course_track_map_v1.sample.json \
  --output /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/indexes/ko_course_track_map_v1.sample.md

python3 - <<'PY'
import json, pathlib
from jsonschema import validate
root = pathlib.Path('/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks')
schema = json.loads((root/'schemas/tlg023_course_track_map_v1.schema.json').read_text())
data = json.loads((root/'indexes/ko_course_track_map_v1.sample.json').read_text())
validate(instance=data, schema=schema)
print('tlg023 schema validation: OK')
PY
```
