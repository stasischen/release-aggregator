# Handoff Summary

## Status
Completed implementation. Pending human review / commit.

## Known Root Cause
- Video: atomized source data exists, but frontend runtime video package is generated from payloads with empty `content`, so subtitle parser falls back to generated atoms.
- Sentence Bank: artifact contains atoms, but frontend DTO/domain mapping drops them before UI.

## Current Plan
1. Fixed video sync bridge and atom coverage gate.
2. Preserved sentence-bank atoms and exposed atom UI.
3. Added regression coverage across both paths.

## Implemented Changes
- `content-pipeline/scripts/sync_video_to_frontend.py` merges `content/core/video_atoms/{videoId}_atoms.json` into runtime video core payloads under `turn.content.atoms`.
- Frontend video runtime assets were regenerated through the release-aggregator bridge; 29 files now have 3487/3487 atomized turns.
- `LearningLibrarySentenceDto` and `Sentence` now retain `List<LingoAtom> atoms`.
- Learning Library mapper carries sentence atoms from artifact DTOs into domain models.
- Sentence detail UI shows a `字詞拆解` section and opens existing `DictionaryContent` for atom drilldown.
- `DictionaryContent` now defaults to theme `onSurface` when `textColor` is not supplied, fixing dark-mode dictionary detail readability.

## Validation
- `python3 -m unittest tests/test_sync_video_to_frontend.py -v`
- `python3 -m py_compile scripts/sync_video_to_frontend.py`
- `make sync-frontend-assets`
- `flutter test test/core/asset_integrity_test.dart test/features/learning_library/data/dto/artifact_parsing_test.dart test/features/learning_library/presentation/screens/sentence_detail_screen_test.dart test/features/dictionary/presentation/widgets/dictionary_content_candidate_selector_test.dart`
- `flutter analyze lib/features/dictionary/presentation/widgets/dictionary_content.dart lib/features/learning_library/data/dto/learning_library_sentences_dto.dart lib/features/learning_library/domain/models/sentence.dart lib/features/learning_library/data/mappers/learning_library_mapper.dart lib/features/learning_library/presentation/screens/sentence_detail_screen.dart test/core/asset_integrity_test.dart test/features/learning_library/data/dto/artifact_parsing_test.dart test/features/learning_library/presentation/screens/sentence_detail_screen_test.dart test/features/dictionary/presentation/widgets/dictionary_content_candidate_selector_test.dart`
- `make validate-frontend-assets`

## Follow-Up Notes
- This bridges the existing complete 29/29 `video_atoms` sidecars into frontend runtime packages. It does not claim `content_v2/inventory/content_assets/video` is complete; that inventory still appears partial in this checkout.
- Tail review may still affect individual atom quality, but the frontend no longer sees zero atoms for shipped video or sentence-bank assets.
