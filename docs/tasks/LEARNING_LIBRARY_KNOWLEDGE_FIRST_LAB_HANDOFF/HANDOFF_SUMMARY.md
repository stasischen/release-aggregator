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
- Added `FRONTEND_UI_IMPLEMENTATION_PACKET.md` for the first Knowledge-First Lab index-first UI slice.
- Completed `ll-klab-handoff-04`: `lingo-frontend-web` now maps canonical vocab/topic/source/sentence relationships into the runtime snapshot and exposes an index-first Knowledge Lab learning-map UI with vocab detail routing.

## Current Decisions

- `LLCM-008` is the correct predecessor for this task.
- Knowledge-First Lab should use the existing shared graph and a separate product UI from Content-First Learning.
- `vocab_sets` remains a teaching selection layer, not dictionary truth.
- Gemini should not modify frontend code for this task.
- Codex owns task tracking, decision synthesis, and frontend implementation review.

## Important Context

- `FRONTEND_V2_INTAKE_COMPLETION` did not include dictionary, grammar, or learning-library in its resolver slice.
- Existing frontend artifact mode is necessary but not sufficient for Knowledge Lab product completeness.
- Artifact naming drift around `vocab_sets` has been resolved by final contract alignment, not compatibility fallback.
- Current frontend artifacts use canonical core files only: `sources_index.json`, `sentences.json`, `knowledge.json`, `topics.json`, `vocab_sets.json`, and `links.json`.
- `core/vocab_sets.json` and `core/links.json` are non-empty and emitted links have no dangling refs in the regenerated artifact set.

## Verification

- `flutter test test/features/learning_library/data/mappers/learning_library_mapper_test.dart test/features/learning_library/data/services/learning_library_lookup_test.dart test/features/learning_library/presentation/screens/knowledge_lab_home_screen_test.dart test/features/learning_library/presentation/screens/vocab_detail_screen_test.dart`
- `flutter test test/features/learning_library/data/sources/artifact_learning_library_data_source_test.dart test/features/learning_library/data/repositories/learning_library_content_repository_test.dart test/core/asset_integrity_test.dart`
- `flutter analyze lib/features/learning_library lib/core/router/app_router.dart test/features/learning_library/data/mappers/learning_library_mapper_test.dart test/features/learning_library/data/services/learning_library_lookup_test.dart test/features/learning_library/presentation/screens/knowledge_lab_home_screen_test.dart`
- `git diff --check`

## Next Steps

1. Start a follow-up task for richer education flows: source/sentence drilldown from the learning-map overview cards, guided “what to study next”, and progress-aware sequencing.
2. Keep lesson runtime work separate from this completed Learning Library handoff.
3. Use content enrichment tasks for increasing source/topic density; do not treat UI as a replacement for curriculum sequencing.

## Do Not Redo / Do Not Change

- Do not redesign the multi-layer content architecture.
- Do not change lesson runtime format.
- Do not remove `mapping_v2` origin cache.
- Do not make Learning Library vocab sets a second dictionary truth.
- Do not edit `content-ko` or `content-pipeline` without a dedicated follow-up task.
