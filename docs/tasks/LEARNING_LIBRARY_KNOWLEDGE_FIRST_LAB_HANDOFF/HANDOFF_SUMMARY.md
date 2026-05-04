# Handoff Summary

## Completed

- Created active task packet for `LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF`.
- Reframed the work as a continuation of existing LLCM / multi-layer planning, not a new schema effort.
- Reconciled the archived LLCM task state by marking the artifact migration as `done_with_active_followup` and promoting `LLCM-008` to this active follow-up task.
- Assigned Gemini to read-only content/artifact inventory only.
- Kept frontend code changes out of scope until the task artifact exists and the inventory is reviewed.
- Added `UI_ACCEPTANCE_MATRIX.md` for Knowledge-First Lab product acceptance.
- Reviewed Gemini inventory and marked `ll-klab-handoff-02` completed.
- Added `ARTIFACT_CONTRACT_FIX_PROMPT.md` for the next artifact emission contract slice.
- Completed `ll-klab-handoff-05`: `content-pipeline` now emits final LLCM-005G canonical files, frontend assets were regenerated, and frontend loader fallback was removed.

## Current Decisions

- `LLCM-008` is the correct predecessor for this task.
- Knowledge-First Lab should use the existing shared graph and a separate product UI from Content-First Learning.
- `vocab_sets` remains a teaching selection layer, not dictionary truth.
- Gemini should not modify frontend code for this task.
- Codex owns task tracking, decision synthesis, and narrow frontend implementation after review.

## Important Context

- `FRONTEND_V2_INTAKE_COMPLETION` did not include dictionary, grammar, or learning-library in its resolver slice.
- Existing frontend artifact mode is necessary but not sufficient for Knowledge Lab product completeness.
- Artifact naming drift around `vocab_sets` has been resolved by final contract alignment, not compatibility fallback.
- Current frontend artifacts use canonical core files only: `sources_index.json`, `sentences.json`, `knowledge.json`, `topics.json`, `vocab_sets.json`, and `links.json`.
- `core/vocab_sets.json` and `core/links.json` are non-empty and emitted links have no dangling refs in the regenerated artifact set.

## Next Steps

1. Prepare the first frontend Knowledge Lab index-first implementation packet.
2. Implement the first UI slice against the canonical Learning Library artifacts.
3. Add product smoke tests for index-first Knowledge Lab home/detail/reverse lookup.

## Do Not Redo / Do Not Change

- Do not redesign the multi-layer content architecture.
- Do not change lesson runtime format.
- Do not remove `mapping_v2` origin cache.
- Do not make Learning Library vocab sets a second dictionary truth.
- Do not edit `content-ko` or `content-pipeline` without a dedicated follow-up task.
