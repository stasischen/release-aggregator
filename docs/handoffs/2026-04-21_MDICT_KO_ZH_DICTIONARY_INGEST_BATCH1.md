# Handoff: MDict Korean-Chinese Dictionary Ingest - Batch 1

- **Date**: 2026-04-21
- **Task ID**: `MDICT_KO_ZH_DICTIONARY_INGEST`
- **Current Machine**: `mac`
- **Status**: `in_progress`

## Purpose
Classify the current work into a small, reproducible pilot so another machine can continue without depending on this machine's memory-heavy context.

## Committed State
- `mac` owns `MDICT_KO_ZH_DICTIONARY_INGEST`.
- `YT_ATOM_TO_V2_CONTENT` is routed to `home`.
- `888` is released.
- The task index and machine status files have been updated to match the current routing.

## Open Suggestions
These are the ideas that should stay as suggestions until a worker confirms them in output:

1. Keep the pilot very small, ideally rank 1-50 only.
2. Treat HTML stripping and sense splitting as separate normalization steps.
3. Record provenance at record level before attempting any batch merge.
4. Keep the pilot output in a staging JSONL file before any full batch consolidation.

## Batch 1 Scope
### Input
- `content-ko/content/staging/nikl_naver_rebuild/naver_zh_tw.jsonl`

### Output
- `content-ko/content_v2/staging/dictionary/pilot_mdict.jsonl`

### What to do
1. Sample a small pilot subset from the staging source.
2. Normalize HTML noise and unstable sense delimiters.
3. Map the pilot into the V2 dictionary inventory shape.
4. Write the staging output in a reproducible form.
5. Keep review notes for anything ambiguous.

## Hard Gates
- Do not start the full batch until the pilot validates.
- Do not merge pilot output into the final inventory without review.
- Keep source, staging, and inventory paths separate.

## Worker Prompt
```text
You are the worker for MDICT_KO_ZH_DICTIONARY_INGEST Batch 1.

Read:
1. release-aggregator/docs/handoffs/2026-04-21_MDICT_KO_ZH_DICTIONARY_INGEST_BATCH1.md
2. release-aggregator/docs/tasks/MDICT_KO_ZH_DICTIONARY_INGEST_TASKS.json
3. release-aggregator/docs/tasks/MACHINE_STATUS.md
4. release-aggregator/docs/tasks/MDICT_KO_ZH_DICTIONARY_INGEST_PLAN.md

Execute only the pilot batch. Keep it small, reproducible, and reviewable.
If normalization rules are ambiguous, stop and record the ambiguity instead of guessing.
```
