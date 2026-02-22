# Handoff: B1 Korean Audit Batch 2 (B1-06 to B1-10)

## Context

- **Topic**: Wave-1-B1-Audit (Batch 2)
- **Status**: Manual surgery completed and synced.
- **Goal**: Standardize B1 lessons to V5 protocol for atomic decomposition and POS accuracy.

## Accomplishments (Commit: 3648499)

- Completed manual surgery for `B1-06`, `B1-07`, `B1-08`, `B1-09`, and `B1-10`.
- **Standardization Highlights**:
  - Aux verb `싶다` -> `ko:vx:싶다`.
  - Hypothetical `-ㄴ다면` corrected from `온다 + 면` to `오다 + ㄴ다면`.
  - Proper nouns tagged and markers separated (`서진 + 이는` etc.).
  - Necessity/Suitability patterns standardized.
- Gold standard `.jsonl` files generated and synced to `content/gold_standards/dialogue/B1/`.
- Successfully rebased and pushed to `origin main` in `content-ko`.

## Infrastructure

- **Scripts**: `scripts/review/orchestrator.py` (apply phase).
- **Heuristics**: `scripts/review/fix_surgery.py` (indirectly via manual review alignment).

## Remaining Tasks

- [ ] **Wave-1-B1-Audit Batch 3**: Lessons B1-11 to B1-15.
- [ ] **Validation Run**: Perform a full `ko_data_pipeline.py` run on the entire B1 directory to ensure no dictionary gaps.

## Next Agent Instructions

Run the following to start the next batch:

```bash
# In e:\Githubs\lingo\content-ko
python scripts/review/orchestrator.py draft --lesson B1-11
```

Check `STATE.md` in `content-ko` for the latest progress history.
