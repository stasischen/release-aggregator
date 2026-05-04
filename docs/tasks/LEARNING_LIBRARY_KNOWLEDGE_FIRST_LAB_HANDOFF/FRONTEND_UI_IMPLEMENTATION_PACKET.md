# Frontend UI Implementation Packet

## Objective

Implement the first Knowledge-First Lab product UI slice against canonical Learning
Library artifacts.

## Scope

Target repo: `/Users/ywchen/Dev/lingo/lingo-frontend-web`

Approved files/modules:

- `lib/features/learning_library/data/mappers/**`
- `lib/features/learning_library/data/services/**`
- `lib/features/learning_library/presentation/screens/**`
- `lib/features/learning_library/presentation/controllers/**`
- `lib/core/router/app_router.dart`
- targeted tests under `test/features/learning_library/**`

## Required Behavior

1. Artifact composition must preserve `vocab_sets`, `topic_refs`, `source_refs`, and link-derived refs in the runtime snapshot.
2. Knowledge Lab home must expose index-first counts/entry points for knowledge, topics, vocab, sources, and sentences.
3. Knowledge Lab home must show vocab entries when artifact vocab sets exist.
4. Vocab detail route must exist under Knowledge Lab and show teaching-selection relationships.
5. UI must read the composed snapshot only; screens must not merge core/i18n packs.

## Out Of Scope

- Lesson runtime format.
- `content-ko` edits.
- `content-pipeline` edits.
- Dictionary mapping cache removal.
- Broad visual redesign beyond this Knowledge Lab slice.

## Validation

Run targeted tests:

- `flutter test test/features/learning_library/data/mappers/learning_library_mapper_test.dart test/features/learning_library/data/services/learning_library_lookup_test.dart`
- `flutter test test/features/learning_library/presentation/screens/knowledge_lab_home_screen_test.dart test/features/learning_library/presentation/screens/vocab_detail_screen_test.dart`
- `flutter test test/features/learning_library/data/sources/artifact_learning_library_data_source_test.dart test/features/learning_library/data/repositories/learning_library_content_repository_test.dart`
- `flutter analyze` on changed Dart files.
