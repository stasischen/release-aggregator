# Frontend Artifact Contract Verification

Date: 2026-05-02
Scope: local verification of `lingo-frontend-web/assets` against frontend loaders and current PRG/release contracts.

## Correction To Prior Inventory

The frontend `assets/` directory is **not empty**.

Observed files include:

- `assets/content/production/manifest.json`
- `assets/content/production/packages/ko/manifest.json`
- `assets/content/production/packages/ko/core/dictionary_core.json`
- `assets/content/production/packages/ko/i18n/dict_ko_zh_tw.json`
- `assets/content/production/packages/ko/lessons/modular_lessons.json`
- `assets/config/video_metadata.json`
- `assets/artifacts/learning_library/ko/library_manifest.json`

Therefore, the correct assessment is not "all frontend assets are missing." The correct assessment is:

> Frontend assets exist, but several production contracts point to the wrong artifact shape, omit required manifest entries, or are incomplete for active routes.

## Verified Loader Contracts

| Loader | Required Asset | Contract |
| :--- | :--- | :--- |
| `ConfigLoader.loadUnifiedManifest()` | `assets/content/production/manifest.json` | JSON object with `files.study_discovery` and optional `lessons[]` |
| `ConfigLoader.loadStudyDiscovery()` | value of `manifest.files.study_discovery` | JSON object with `lessons[]` and `units[]` |
| `LessonRegistryRepository.getAllLessons()` | `manifest.files.study_discovery`, `manifest.lessons[]`, `packages/ko/lessons/modular_lessons.json` | Lesson metadata must expose `lesson_id` or compatible IDs |
| `DictionaryRepository` | `packages/{lang}/manifest.json` | `filesFor("core")` must include `dictionary_core.json`; `filesFor("i18n")` must include `dict_ko_zh_tw.json`, `mapping.json`, `Strings_zh_tw.json` |
| `VideoRepository` | `assets/config/video_metadata.json`; package video JSON via `StudyContentLocator` | metadata IDs must map to registry video lesson IDs and video package files |
| `GrammarNoteService` | `assets/content/grammar/grammar_index.json` | map of grammar ID to grammar note JSON path |
| `ArtifactLearningLibraryDataSource` | `assets/artifacts/learning_library/ko/library_manifest.json` | manifest with `files` for core/i18n learning-library artifacts |

## Verification Results

| Check | Status | Evidence |
| :--- | :--- | :--- |
| Production manifest exists | PASS | `lingo-frontend-web/assets/content/production/manifest.json` |
| `files.study_discovery` exists | PASS | value is `assets/artifacts/learning_library/ko/core/sources_index.json` |
| `study_discovery` target exists | PASS | target file exists |
| `study_discovery` has `lessons[]` | FAIL | target is `sources_index.json`, not lesson catalog |
| `study_discovery` has `units[]` | FAIL | target is `sources_index.json`, not lesson catalog |
| Production manifest has lesson entries | FAIL | `lessons` is empty |
| `assets/content/production/lesson_catalog.json` exists | FAIL | file missing |
| Dictionary package manifest exists | PASS | `packages/ko/manifest.json` exists |
| Dictionary core file exists | PASS | `packages/ko/core/dictionary_core.json` exists |
| Dictionary i18n file exists | PASS | `packages/ko/i18n/dict_ko_zh_tw.json` exists |
| Dictionary manifest exposes `core` module | FAIL | manifest nests files under `modules.dictionary.core`, while frontend asks for `filesFor("core")` |
| Dictionary manifest exposes `i18n` module | FAIL | manifest nests files under `modules.dictionary.i18n`, while frontend asks for `filesFor("i18n")` |
| `mapping.json` exists | FAIL | missing |
| `Strings_zh_tw.json` exists | FAIL | missing |
| `modular_lessons.json` exists | PASS | file exists with 3 IDs |
| Listed modular lesson content exists | PASS | first listed IDs have `lesson_content.v1.json` |
| `video_metadata.json` exists | PASS | 29 entries |
| Video package JSON exists under production packages | FAIL | no `assets/content/production/packages/ko/video/**/*.json` found |
| `grammar_index.json` exists | FAIL | missing |
| Learning library manifest exists | PASS | `assets/artifacts/learning_library/ko/library_manifest.json` |
| Learning library manifest has files | PASS | `files` object exists |

## Corrected Findings

### P0: Study discovery points to the wrong artifact shape

`assets/content/production/manifest.json` contains:

```json
{
  "lang": "ko",
  "files": {
    "study_discovery": "assets/artifacts/learning_library/ko/core/sources_index.json"
  },
  "lessons": []
}
```

`ConfigLoader.loadStudyDiscovery()` and `LessonRegistryRepository.getAllLessons()` expect the target file to contain `lessons[]` and `units[]`.
The current target is a learning-library source index, so study catalog/path pages cannot build a real lesson registry from this manifest.

Required fix:

- Generate or sync a real `lesson_catalog.json`.
- Set `files.study_discovery` to that catalog path.
- Populate `manifest.lessons[]` with PRG lesson entries or rely on catalog-backed discovery consistently.

### P1: Dictionary files exist but package manifest shape does not match the frontend repository

The frontend `DictionaryRepository` calls:

- `filesFor("core")` for `dictionary_core.json`
- `filesFor("i18n")` for `dict_ko_zh_tw.json`, `mapping.json`, and `Strings_zh_tw.json`

Current `packages/ko/manifest.json` uses:

```json
{
  "modules": {
    "dictionary": {
      "core": "dictionary_core.json",
      "i18n": "dict_ko_zh_tw.json"
    }
  }
}
```

`PipelineManifest.fromJson()` treats that as module `dictionary`, not as top-level `core` / `i18n`.
So the existing core/i18n files are not discoverable through the current repository contract.

Required fix:

- Either reshape the package manifest to expose top-level `core` and `i18n` file lists, or update `DictionaryRepository` to request the `dictionary` module shape.
- Add or intentionally de-scope `mapping.json` and `Strings_zh_tw.json`.

### P1: Video metadata exists, but video package payloads are absent from production packages

`assets/config/video_metadata.json` exists and has 29 entries.
No `assets/content/production/packages/ko/video/**/*.json` files were found.

`VideoRepository.loadSubtitles()` resolves package paths through `StudyContentLocator`, so video discovery/playback can find metadata but fail to load actual subtitle/content payloads.

Required fix:

- Run or repair video package sync so metadata IDs have matching package JSON files.
- Confirm path conventions between `sync_video_to_frontend.py`, `StudyContentLocator`, and PRG manifest entries.

### P1: Grammar index is missing

`assets/content/grammar/grammar_index.json` does not exist.
Grammar pages will not resolve grammar notes until a grammar index and note sync/generator exists.

Required fix:

- Generate `grammar_index.json`.
- Copy or transform grammar note JSONs into the frontend grammar asset path.

### P2: Modular lesson registry exists and is not a total blocker

Contrary to the prior inventory, `packages/ko/lessons/modular_lessons.json` exists and is non-empty.
The listed sample lesson content files also exist.

Remaining risk:

- Need a producer/sync ownership check before treating this as complete.
- The registry is hardcoded to `ko` in `LessonRegistryRepository`.

### P2: Learning library assets are present

`assets/artifacts/learning_library/ko/library_manifest.json` exists and has a `files` object.
This domain should not be folded into PRG until a concrete runtime risk is shown.

## Architecture Implications

1. PRG promotion should remain paused, but not because all assets are missing.
2. The immediate learning-app blocker is the production manifest/study-discovery contract.
3. Dictionary is a manifest-shape and missing-sidecar problem, not a total absence of dictionary files.
4. Grammar remains a true missing-producer gap.
5. Video has metadata but lacks package payloads in the expected production path.
6. Learning library appears closer to complete and should remain a separate domain manifest.

## Recommended Next Implementation Order

1. Fix PRG/default frontend catalog path contract:
   - PRG should emit `files.study_discovery` to the actual frontend-loadable catalog path.
   - Sync or place `lesson_catalog.json` where frontend expects it.

2. Repair production `manifest.json`:
   - replace the learning-library `sources_index.json` pointer with lesson catalog/study discovery.
   - decide whether `manifest.lessons[]` should be PRG-owned or catalog-only.

3. Repair dictionary package manifest compatibility:
   - expose `core` and `i18n` files in the shape `DictionaryRepository` can load, or update the frontend repository contract.
   - decide on `mapping.json` and `Strings_zh_tw.json` scope.

4. Add grammar index producer/sync.

5. Repair video package payload sync.

6. Only after these contract issues are addressed, revisit PRG promotion naming and command surface.
