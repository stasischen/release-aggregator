# Dictionary Entry Drift Review Plan

## Goal

Audit Korean dictionary inventory rows for lexical drift before promoting
dictionary assets as a default frontend bridge output.

The current dictionary key model is:

```text
atom row = ko:{pos}:{lemma}
homonym = definitions.{locale}[].entry_no
polysemy = definitions.{locale}[].sense_id / sense_no
```

This task should not migrate atom IDs to homonym-specific keys such as
`ko:n:밤#1`. It should first verify whether the current rows correctly preserve
homonym, polysemy, origin, and source metadata.

## Scope

- `content-ko/content_v2/inventory/dictionary/manifest.json`
- `content-ko/content_v2/inventory/dictionary/**.jsonl`
- `content-pipeline/pipelines/learning_library.py`
- `content-pipeline/scripts/export_bridge_dictionary.py`
- Frontend runtime assets generated under `content-pipeline/dist/ko/packages/`

## Review Questions

1. Which atom rows contain multiple `entry_no` values, and are those true
   homonyms or incorrectly merged unrelated entries?
2. Which atom rows contain multiple senses under one `entry_no`, and are those
   true polysemy rather than homonym drift?
3. Which rows should have `metadata.hanja`, `origin_type`,
   `source_language`, or `source_word` but currently do not?
4. Which rows have contradictory `hanja`/origin values across senses or
   homonym entries that cannot be represented cleanly at row-level metadata?
5. Which `surface_forms` create same-surface cross-POS candidates, and does
   `mapping_v2.json` preserve all candidates without collapsing them?
6. Are `entry_no`, `sense_no`, and `sense_id` stable enough to support future
   lesson-level disambiguation?

## Acceptance Criteria

- Produce a drift inventory with counts and examples for:
  - cross-POS same surface candidates
  - same-row multi-`entry_no` homonyms
  - same-row multi-sense polysemy
  - missing Hanja/origin candidates
  - suspicious merged entries
- Do not edit dictionary inventory in the first pass.
- Recommend a batch remediation order and identify rows requiring human review.
- Confirm whether `mapping_v2.entry_refs` is sufficient for current frontend
  and future tokenizer/handoff disambiguation.

## Suggested First Command

```bash
cd /Users/ywchen/Dev/lingo/content-ko
python - <<'PY'
import json
from collections import defaultdict
from pathlib import Path

root = Path('.')
manifest = json.loads((root / 'content_v2/inventory/dictionary/manifest.json').read_text())
rows = []
for shard in manifest['shards'].values():
    path = root / shard['path']
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            rows.append(json.loads(line))

multi_entry = []
surface_pos = defaultdict(list)
for row in rows:
    defs = row.get('definitions', {}).get('zh_tw', [])
    entry_nos = {d.get('entry_no', 1) for d in defs if isinstance(d, dict)}
    if len(entry_nos) > 1:
        multi_entry.append(row)
    surfaces = set(row.get('surface_forms') or [])
    if row.get('lemma'):
        surfaces.add(row['lemma'])
    for surface in surfaces:
        surface_pos[(surface, row.get('pos'))].append(row)

print('rows', len(rows))
print('same surface+pos multi rows', sum(1 for v in surface_pos.values() if len(v) > 1))
print('same row multi entry_no', len(multi_entry))
PY
```

