# Backend/Content Artifact Inventory Report

**Date**: 2026-05-02
**Scope**: Read-only inventory — no files modified.
**Repos**: release-aggregator, lingo-frontend-web, content-pipeline, content-ko, core-schema

---

## 1. Artifact Inventory Table

| # | Artifact | Current Path (Frontend Expects) | Producer Repo/Script | Consumer (Frontend Page/Repository) | Required Fields | Current Status | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | `manifest.json` | `assets/content/production/manifest.json` | `release-aggregator/scripts/prg/assembler_prototype.py` (PRG pilot) OR `content-pipeline/scripts/sync_video_to_frontend.py` (video sync) | `LessonRegistryRepository` (l.21), `ConfigLoader` (l.37) | `files.study_discovery` (string), `lessons[].level_id`, `lessons[].path`, `lessons[].type` | **PARTIAL (staging only)** | Pilot output exists at `staging/prg_pilot/output_strict/manifest.json` with 3 entries. Not synced to frontend. All title/subtitle fields null. |
| 2 | `lesson_catalog.json` / `study_discovery.json` | `assets/content/production/lesson_catalog.json` | `assembler_prototype.py` (PRG) | `ConfigLoader` (l.68, via `files.study_discovery`) | `units[].id`, `units[].title`, `lessons[].lesson_id`, `lessons[].unit_id` | **PARTIAL (staging only)** | Pilot output at `staging/prg_pilot/output_strict/lesson_catalog.json`. Units have placeholder titles ("Unassigned"), all lesson fields null/empty. |
| 3 | `modular_lessons.json` | `assets/content/production/packages/ko/lessons/modular_lessons.json` | Not found in any pipeline script | `LessonRegistryRepository` (l.23) | `{"lessons": ["lesson_..."]}` (string array) | **MISSING** | No producer found. Frontend hardcodes this path at `lesson_registry_repository.dart:23`. |
| 4 | Modular lesson content | `assets/content/production/packages/ko/lessons/{id}/build/lesson_content.v1.json` | Not found | `LessonRegistryRepository._loadModularMetadata()` (l.127) | `unit.unit_id`, `unit.title_i18n`, `unit.theme_i18n` | **MISSING** | No modular lesson content files found in any repo. |
| 5 | Modular lesson seeds | `.../lessons/{id}/build/p1_seed.v1.json`, `p2_seed.v1.json` | Not found | `StudyContentLocator` (l.34-40) | (not read in repository layer directly) | **MISSING** | No producer found. |
| 6 | `video_metadata.json` | `assets/config/video_metadata.json` | `content-pipeline/scripts/sync_video_to_frontend.py` (l.207) | `VideoRepository` (l.43) | Array of `{id, title, channel, thumbnailUrl, duration, category, difficulty, tags, languageCode}` | **PARTIAL (producible, not synced)** | Script exists and can produce this. Content-ko has 30+ video core files. Not synced to frontend. |
| 7 | Video package JSON | `assets/content/production/packages/ko/video/{lessonId}.json` | `sync_video_to_frontend.py` (l.178-179) | `StudyContentLocator.corePath()` (l.11-12) | `metadata`, `nodes`, `turns` structure | **PARTIAL (producible, not synced)** | Content-ko has source files. Pipeline's `dist/staging/ko/core/video/` has 18 files. Not synced to frontend. |
| 8 | Dialogue core JSON | `assets/content/production/packages/ko/core/dialogue/{level}/{id}.json` | `content-pipeline/pipelines/build_ko_zh_tw.py` (l.51-60) | `StudyContentLocator.corePath()` (l.14-15) | `id`, `title`, `content[]` (dialogue_core schema) | **MISSING (frontend path)** | Pipeline builds to `dist/staging/ko/core/dialogue/`. Frontend expects different path: `packages/ko/core/dialogue/`. Build script doesn't place under `packages/`. See Section 6 gap #1. |
| 9 | Dialogue i18n JSON | `assets/content/production/packages/ko/i18n/{locale}/dialogue/{level}/{id}.json` | `build_ko_zh_tw.py` (l.63-70) | `StudyContentLocator.i18nPath()` (l.27) | `lesson_id`, `learner_lang`, `title`, `translations` | **MISSING (frontend path)** | Pipeline builds to `dist/staging/ko/zh_tw/dialogue/`. Frontend expects `packages/ko/i18n/zh_tw/dialogue/`. |
| 10 | Dictionary package manifest | `assets/content/production/packages/{lang}/manifest.json` | Not clearly produced by any single script | `DictionaryRepository` (l.12-13) | `lang`, `version`, `modules`, `files` (package.schema.json) | **MISSING** | No producer found. `sync_video_to_frontend.py` can update it for the video module (l.205-206), but no script generates the initial full package manifest. |
| 11 | Dictionary core | `assets/content/production/packages/{lang}/core/{dict_core_name}` (resolved via manifest) | Not found | `DictionaryRepository.loadBaseDictionary()` (l.18-32) | `atom_id`, `lemma_id`, `surface_forms`, `pos`, `senses`, `source_refs` (dictionary_core schema) | **MISSING** | Content-ko has `content/core/dictionary/index.json` and `index.csv` — NOT the V5 atom structure the frontend expects. No build script produces dictionary_core.json. |
| 12 | Dictionary i18n | `assets/content/production/packages/{lang}/i18n/{dict_i18n_name}` (resolved via manifest) | Not found | `DictionaryRepository.loadLanguagePack()` (l.46-65) | `atom_id`, `learner_lang`, `definitions` (dictionary_i18n schema) | **MISSING** | No build script produces dictionary i18n. Content-ko has no i18n directory for dictionary. |
| 13 | Lesson strings | `...packages/{lang}/i18n/{Strings_{locale}.json}` (resolved via manifest) | Not found | `DictionaryRepository.loadLessonStrings()` (l.78-110) | Map of string keys | **MISSING** | No producer found. |
| 14 | Chunk mapping | `...packages/{lang}/i18n/{mapping.json}` (resolved via manifest) | Not found | `DictionaryRepository.loadChunkMapping()` (l.113-136) | Map structure | **MISSING** | No producer found. |
| 15 | `grammar_index.json` | `assets/content/grammar/grammar_index.json` | Not found in any pipeline script | `GrammarNoteService` (l.23-24) | `Map<String, String>` (production ID → file path, e.g. `G-KO-*` → filename) | **MISSING** | No producer found. Grammar core files exist in content-ko with `fs_safe_id` naming (`ko__g__a1__...`), but no index maps them to `G-KO-*` production IDs. |
| 16 | Grammar note JSON | `assets/content/grammar/{fileName}` (resolved via index) | Not found | `GrammarNoteService._loadNoteFromFile()` (l.53-55) | `grammar_id` (canonical), `pattern`, `examples`, i18n fields | **MISSING (not in frontend path, not indexed)** | Content-ko has `content/core/grammar/*.json` with canonical data. Not produced to frontend path. |
| 17 | Learning library manifest | `assets/artifacts/learning_library/{target}/library_manifest.json` | `content-pipeline/pipelines/learning_library.py` | `ArtifactLearningLibraryDataSource` (l.162-163) | `lang`, `version`, `modules`, `files` (package.schema.json) | **PARTIAL (producible)** | Pipeline produces to `dist/artifacts/ko/manifest.json` (not `library_manifest.json`). Content exists. |
| 18 | Learning library core files | `assets/artifacts/learning_library/{target}/core/{file}.json` | `learning_library.py` | `ArtifactLearningLibraryDataSource` (l.40-57) | `sources_index`, `sentences`, `knowledge`, `topics`, `vocab_sets`, `links` | **PARTIAL (producible)** | Pipeline produces to `dist/artifacts/ko/core/`. Not synced to frontend. |
| 19 | Learning library i18n files | `assets/artifacts/learning_library/{target}/i18n/{support}/{file}.json` | `learning_library.py` | `ArtifactLearningLibraryDataSource` (l.87-101) | `sources`, `sentences`, `knowledge`, `topics`, `vocab_sets` | **PARTIAL (producible)** | Pipeline produces to `dist/artifacts/ko/i18n/zh_tw/`. Not synced to frontend. |
| 20 | `global_manifest.json` | n/a (Phase 1 pipeline output, consumed by PRG) | `release-aggregator/scripts/release.py` (l.216) | `assembler_prototype.py` (as candidate inventory, l.584) | `packages[].id`, `packages[].path`, `packages[].provenance` (manifest.schema.json) | **STALE** | Exists at `staging/v1.0.0/global_manifest.json` with 26 A1 dialogue packages. Built 2026-02-13. Not regenerated since. |
| 21 | `production_plan.json` | n/a (PRG output, build artifact) | `assembler_prototype.py` (l.495) | n/a (build artifact, not consumed at runtime) | Summary, gaps, allowlisted_lessons, packaged_artifacts | **PARTIAL** | Pilot output at `staging/prg_pilot/output_strict/production_plan.json`. 3 lessons, 0 gaps. |
| 22 | Release manifest (PRD seed) | `staging/prd.release_manifest.seed.json` | `scripts/prg/seed_release_manifest.py` | `assembler_prototype.py` (consumed as release manifest) | `entries[]` with `unit_id`, `lesson_id`, `release_status`, `content_type`, etc. | **STALE** | Seed script defaults read from frontend paths that don't exist (`lingo-frontend-web/assets/content/production/manifest.json`). |

---

## 2. Page Readiness Table

| Page/Screen | Required Artifacts | Artifact Status | Runtime Risk | Owner Repo |
|---|---|---|---|---|
| `/study` (Learn Home) | `manifest.json` (#1), `lesson_catalog.json` (#2) | PARTIAL (staging only, null fields) | **HIGH** — No manifest or catalog in frontend assets. `ConfigLoader.loadUnifiedManifest()` at `config_loader.dart:37` will throw on missing file. | release-aggregator (PRG) |
| `/study/catalog` (Course Catalog) | `manifest.json`, `lesson_catalog.json` | PARTIAL (staging only) | **HIGH** — Same dependency as Learn Home. Also requires `lessons[].title`, `lessons[].subtitle`, `lessons[].theme_tags` all currently null. | release-aggregator (PRG) |
| `/study/unit/:unitId` | `lesson_catalog.json` (#2) | PARTIAL (staging only, units have placeholder data) | **HIGH** — Unit titles are "Unassigned". No real unit data. | release-aggregator (PRG) |
| `/study/lesson-preview` | `manifest.json`, `lesson_catalog.json` | PARTIAL | **HIGH** — Lesson `title`, `subtitle`, `can_do`, `estimated_minutes`, `theme_tags`, `skill_tags` are all null. | release-aggregator (PRG) |
| `/study/modular-runtime/:lessonId` | `modular_lessons.json` (#3), modular lesson content (#4), modular seeds (#5) | MISSING | **CRITICAL** — No modular lessons exist. `LessonRegistryRepository` will silently fail (l.73-75) and return empty. | Unknown (no producer) |
| `/study/dictionary` | Dictionary package manifest (#10), core (#11), i18n (#12), strings (#13), mapping (#14) | MISSING | **CRITICAL** — `DictionaryRepository` path template `assets/content/production/packages/{lang}/manifest.json` has no file to load. All dictionary operations will throw `ResourceNotFoundException`. | content-pipeline |
| `/study/grammar-notes` | `grammar_index.json` (#15), grammar note JSONs (#16) | MISSING | **CRITICAL** — `GrammarNoteService` loads index from `assets/content/grammar/grammar_index.json`. File doesn't exist. `_idToPathMap` falls back to empty map (l.30). All lookups return null. | content-pipeline |
| `/video/player` | `video_metadata.json` (#6), video package JSON (#7), subtitles via `StudyContentLocator` | PARTIAL (producible) | **HIGH** — `VideoRepository._loadMetadata()` at `video_repository.dart:42` will throw on missing `video_metadata.json`. Cached as empty map (l.55-56). Video discovery returns empty. | content-pipeline (sync_video_to_frontend.py) |
| `/study/path` | `manifest.json`, `lesson_catalog.json` | PARTIAL | **HIGH** — Same core dependency gap. | release-aggregator (PRG) |
| Learning Library pages | Learning library manifest (#17), core (#18), i18n (#19) | PARTIAL (producible) | **MEDIUM** — Pipeline produces these; not synced to frontend. `ArtifactLearningLibraryDataSource` tries V5 manifest first, falls back to legacy (l.161-169). Both paths would fail. | content-pipeline |
| `/study/article` | Dialogue/article JSONs via `StudyContentLocator` | MISSING (frontend path) | **HIGH** — Pipeline builds dialogues but to a different directory structure than frontend expects. | content-pipeline |
| `/event/occurrence` | Via `EventRepository`, same manifest + content paths | PARTIAL | **HIGH** — Same dependency chain as study pages. | release-aggregator (PRG) |

---

## 3. Completeness Findings

### P0 — Frontend assets directory is completely empty

- **Evidence**: `Glob` search for `assets/**/*` in `lingo-frontend-web` returns zero results. The entire `assets/` directory tree does not exist.
- **Missing**: All 22 artifacts listed in Section 1.
- **Why it matters**: Every frontend repository, page, and data source will fail at runtime. There is no graceful degradation — many loaders have `try/catch` but they return empty data, rendering blank pages.
- **Required fix**: Either run the full pipeline to produce and sync all artifacts to `lingo-frontend-web/assets/`, or create a build/deploy target in the Makefile that does this.

### P0 — No modular lesson producer exists

- **Evidence**: `modular_lessons.json` is hardcoded in `lesson_registry_repository.dart:23`. No script in content-pipeline, release-aggregator, or content-ko produces this file. No modular lesson content files (`lesson_content.v1.json`, `p1_seed.v1.json`, `p2_seed.v1.json`) exist anywhere.
- **Missing**: Producer script, content source, build step.
- **Why it matters**: Modular runtime routes (`/study/modular-runtime/:lessonId`, `/study/modular-preview/:previewId`) have no data source. The `_loadModularMetadata()` method silently catches errors (l.145-148) but returns null, so these pages will always show empty.
- **Required fix**: Either (a) implement a modular lesson pipeline in content-pipeline, or (b) if modular lessons are not yet in scope, the frontend should not ship routes that depend on them.

### P0 — Dictionary build pipeline is missing

- **Evidence**: `content-pipeline/pipelines/build_ko_zh_tw.py` has stubs for dictionary copy (l.77-92) but content-ko has `content/core/dictionary/index.json` and `index.csv` — NOT the V5 atom structure (`atoms/*.json` files with `atom_id`, `senses`, `surface_forms`) that the frontend's `DictionaryRepository` expects. The core-schema defines `dictionary_core.schema.json` with required `atom_id` (`^[a-z]{2}:[a-z]+:.+$`), `senses[].sense_id`, etc. The existing `index.json`/`index.csv` don't match this schema.
- **Missing**: V5 atom JSON files for dictionary, dictionary i18n files, package manifest with core/i18n module entries, `Strings_{locale}.json`, `mapping.json`.
- **Why it matters**: DictionaryRepository methods (`loadBaseDictionary`, `loadLanguagePack`, `loadLessonStrings`, `loadChunkMapping`) all call `_requireManifestFile()` which throws `ResourceNotFoundException` when the manifest is missing or the file isn't listed. All dictionary surfaces (hub, overlay lookup, search) will be non-functional.
- **Required fix**: Build the dictionary V5 atom pipeline: source data → `dictionary_core.json` + `dictionary_i18n.json` → publish to `packages/{lang}/manifest.json`. The `build_ko_zh_tw.py` script appears to have the directory structure stubbed out but the actual transformation logic is missing.

### P1 — Grammar index not produced

- **Evidence**: `GrammarNoteService` at `grammar_note_service.dart:23-24` loads `assets/content/grammar/grammar_index.json` expecting a `Map<String, String>` where keys are production IDs like `G-KO-*` and values are file paths. Content-ko has `content/core/grammar/` with files using `fs_safe_id` naming (`ko__g__a1__l03__ability.json`), but no script generates the index mapping `G-KO-*` → file path.
- **Missing**: `grammar_index.json` producer, mapping from canonical `grammar_id` to production `G-KO-*` IDs, file copy to frontend assets.
- **Why it matters**: Grammar surfaces will always show empty. `isGrammarAvailable()` returns false for everything. `loadGrammarNote()` returns null.
- **Required fix**: Create a grammar build step that: (1) reads content-ko grammar JSONs, (2) maps canonical IDs to production `G-KO-*` IDs, (3) copies files to `assets/content/grammar/`, (4) generates `grammar_index.json`.

### P1 — Manifest ↔ lesson_catalog ID mismatch

- **Evidence**: PRG pilot's `manifest.json` uses `level_id` as the lesson key (e.g. `ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson`), while `lesson_catalog.json` uses `lesson_id` (same values). The `LessonRegistryRepository` at l.38 reads `jsonMap['lessons']` from the catalog and indexes by `metadata.lessonId` (derived from `json['lesson_id']`). At l.52 it reads `manifestMap['lessons']` and indexes by `metadata.lessonId` (derived from `json['level_id']`). This works for the pilot because both use the same string, but the field name difference (`level_id` vs `lesson_id`) is a latent risk.
- **Why it matters**: If any future content uses different IDs in manifest vs catalog, lessons will be duplicated or orphaned.
- **Required fix**: Standardize on `lesson_id` across both manifest.json and lesson_catalog.json. The `manifest.json` should use `lesson_id`, not `level_id`.

### P1 — Manifest files.study_discovery hardcodes a different path than what assembler_prototype writes

- **Evidence**: In `assembler_prototype.py:469`, the derived manifest writes `"files": {"study_discovery": study_discovery_path}` where the default is `"assets/content/production/lesson_catalog.json"` (l.534). But `ConfigLoader._resolveManifestFilePath()` at `config_loader.dart:101-114` reads `manifest['files']['study_discovery']` and loads it as a relative asset path. The `rootBundle.loadString()` call expects asset paths (without `assets/` prefix inside Flutter). If the path written is `assets/content/production/lesson_catalog.json`, Flutter's asset loader will double-prefix it to `assets/assets/content/production/lesson_catalog.json`, which won't resolve.
- **Why it matters**: Even if the file is synced to the right location, the path resolution would fail.
- **Required fix**: The `--study-discovery-path` default should be `content/production/lesson_catalog.json` (without the leading `assets/` since that's the Flutter asset bundle prefix), or the ConfigLoader should strip the `assets/` prefix before calling `loadString`.

### P2 — All pilot lesson catalog fields are null/placeholder

- **Evidence**: `staging/prg_pilot/output_strict/lesson_catalog.json` has:
  - `estimated_minutes: null` for all 3 lessons
  - `title: null`, `subtitle: null` for all 3 lessons
  - `theme_tags: []`, `skill_tags: []`, `status_flags: []` for all 3 lessons
  - Unit titles: `{"en": "Unassigned"}`, subtitles: `{"en": "Requires reconciliation"}`
  - Unit level: `"Unknown"`, order: `9999`
- **Why it matters**: The frontend `LessonMetadata.fromJson()` defaults `estimatedMinutes` to 5 and `titleI18n` to `{'zh_tw': normalizedId}` when null, so pages won't crash, but they'll show meaningless placeholder data.
- **Required fix**: Content authors need to provide unit metadata (titles, levels, order) and lesson metadata (titles, subtitles, themes, skills, estimated minutes, can-do) in the release manifest entries. The `pilot_allowlist.json` entries have no such fields.

### P2 — global_manifest.json is stale

- **Evidence**: `staging/v1.0.0/global_manifest.json` was built at `2026-02-13T18:37:11` and contains only 26 A1 dialogue packages. The content-pipeline has since built B2 dialogues and video files. The PRG assembler prototype consumed this in strict mode for the pilot.
- **Why it matters**: If the pipeline is re-run, any new content won't appear in the global manifest unless release.py is re-run. Phase 2 PRG depends on Phase 1 global_manifest.json as its candidate inventory.
- **Required fix**: Re-run `release.py` to regenerate `global_manifest.json` after each pipeline build.

### P3 — Learning library manifest filename mismatch

- **Evidence**: The frontend's `LearningLibraryArtifactPaths.manifestPath()` returns `assets/artifacts/learning_library/{target}/library_manifest.json` (l.8-9). The pipeline's `learning_library.py` outputs to `dist/artifacts/ko/manifest.json` (not `library_manifest.json`).
- **Why it matters**: The frontend tries V5 path first (`library_manifest.json`), falls back to legacy (`manifest.json`). The pipeline produces `manifest.json`, which the frontend would only find on the fallback path. Small but confusing.
- **Required fix**: Align filename: either rename pipeline output to `library_manifest.json` or change `LearningLibraryArtifactPaths.manifestPath()` to `manifest.json`.

### P3 — sync_video_to_frontend.py writes to wrong assets path

- **Evidence**: `sync_video_to_frontend.py:181` sets `production_manifest_path = frontend_repo / "assets" / "content" / "production" / "manifest.json"`. The `build_video_lesson_entry()` function at l.128 writes `"path": f"assets/content/production/packages/ko/video/core/{file.name}"`. This is a full asset path, not a relative path within the package.
- **Why it matters**: The `assembler_prototype.py` expects relative paths from the candidate root. If video sync writes the manifest with absolute asset paths, the assembler may fail path resolution.
- **Required fix**: Use consistent relative paths. Either all paths are relative to the package root, or all relative to the frontend assets root.

---

## 4. Manifest/Domain Architecture Findings

| Domain | Current Manifest | Producer | Consumer | Should Unify Under PRG/Global Manifest? | Reason |
|---|---|---|---|---|---|
| Lesson/Unit Registry | `assets/content/production/manifest.json` + `lesson_catalog.json` | PRG `assembler_prototype.py` | `LessonRegistryRepository`, `ConfigLoader`, `LearningProvider` | **YES** — Already owned by PRG | PRG is the designated assembler. These two files are derived from the same release manifest and candidate inventory. |
| Study Discovery | `lesson_catalog.json` (referenced via `manifest.json.files.study_discovery`) | PRG `assembler_prototype.py` | `ConfigLoader.loadStudyDiscovery()` | **YES** — Already owned by PRG | Correctly linked through `manifest.json.files.study_discovery`. The indirection is by design. |
| Modular Lessons | `modular_lessons.json` + `lesson_content.v1.json` per lesson | **NONE** | `LessonRegistryRepository` (hardcoded) | **DEFER** — Needs producer first | No producer exists. Before unifying, the modular content pipeline must exist. This may be a separate domain from standard lessons. |
| Video Metadata | `assets/config/video_metadata.json` | `sync_video_to_frontend.py` | `VideoRepository` | **NO** — Separate domain manifest | Video metadata is a content index (not a release manifest). It maps video IDs to metadata for discovery. Keep separate; link via lesson entries in the main manifest. |
| Video Package Content | `packages/ko/video/` JSON files | `sync_video_to_frontend.py` | `StudyContentLocator`, `VideoRepository` | **NO** — Package content | These are content payloads, not manifests. They're referenced by the main manifest's `lessons[].path` entries. |
| Dictionary | `packages/{lang}/manifest.json` | **NONE** (incomplete) | `DictionaryRepository` | **YES** — Should be a package manifest under PRG pipeline | The dictionary is a package module. Its manifest should follow `package.schema.json` and be produced as part of the build pipeline, then listed in the main manifest's package references. |
| Grammar | `grammar_index.json` + grammar note JSONs | **NONE** | `GrammarNoteService` | **DEFER** — Separate index | Grammar has its own ID system (`G-KO-*`) and resolution model. The index is a lookup map, not a release manifest. Keep separate but produce it as part of the build pipeline. |
| Learning Library | `library_manifest.json` + core/i18n files | `learning_library.py` | `ArtifactLearningLibraryDataSource` | **NO** — Separate artifact domain | Learning library is a graph-shaped knowledge base, not lesson content. Its manifest is a package-style manifest for artifact resolution. Keep separate. |
| Global Manifest (Phase 1) | `global_manifest.json` | `release.py` | `assembler_prototype.py` (Phase 2 PRG) | **YES** — Phase 1 is consumed by Phase 2 | This is the intended pipeline: Phase 1 aggregates raw pipeline dist into global_manifest, Phase 2 PRG consumes it to produce production artifacts. |

**Architecture assessment**: The split between Phase 1 (`global_manifest.json` by `release.py`) and Phase 2 (`manifest.json` + `lesson_catalog.json` by PRG) is intentional and documented. It is NOT causing runtime risk — the risk is that neither phase is being run. The actual runtime risk is:
1. **No pipeline run producing artifacts** (P0)
2. **Dictionary pipeline is missing entirely** (P0)
3. **Grammar index producer is missing** (P1)
4. **Modular lesson pipeline is missing** (P0)

---

## 5. Backend/Content Gap List

| # | Gap | Blocking Page(s) | Owner Repo | Suggested Next Action |
|---|---|---|---|---|
| G1 | No pipeline build has been run to produce frontend artifacts | ALL pages | content-pipeline + release-aggregator | Run `main.py` (UnifiedWorkflow) → `release.py` → `assembler_prototype.py` → sync to frontend. Create a `make deploy-frontend-assets` target. |
| G2 | Dictionary V5 atom pipeline does not exist | `/study/dictionary`, all overlay lookups | content-pipeline | Build dictionary transformation: content-ko source data → `dictionary_core.json` (V5 atoms) + `dictionary_i18n.json` + `Strings_{locale}.json` + `mapping.json` + package manifest. |
| G3 | Grammar index generator does not exist | `/study/grammar-notes`, all grammar note surfaces | content-pipeline | Build grammar step: content-ko grammar JSONs → map canonical IDs to `G-KO-*` → generate `grammar_index.json` → copy files to frontend. |
| G4 | Modular lesson pipeline does not exist | `/study/modular-runtime/:lessonId`, `/study/modular-preview/:previewId` | content-pipeline or new pipeline | Decide if modular lessons are in scope. If yes, build modular lesson pipeline. If no, remove modular routes from frontend. |
| G5 | `--study-discovery-path` default has wrong asset prefix | ALL study pages that load the catalog | release-aggregator (assembler_prototype.py) | Change default from `assets/content/production/lesson_catalog.json` to `content/production/lesson_catalog.json` (Flutter asset bundle doesn't use `assets/` prefix). |
| G6 | PRG pilot lesson/unit metadata is all null/placeholder | `/study/catalog`, `/study/unit/:unitId`, `/study/lesson-preview` | content-ko (authors) + release-aggregator (release manifest) | Content authors must provide unit/lesson metadata in release manifest entries. |
| G7 | `global_manifest.json` is stale (2026-02-13) | PRG assembler (indirect) | release-aggregator | Re-run `release.py` after each pipeline build to regenerate global_manifest. |
| G8 | Learning library manifest filename mismatch (`manifest.json` vs `library_manifest.json`) | Learning library pages | content-pipeline or lingo-frontend-web | Align filename in one repo. |
| G9 | Dialogue content built to wrong directory structure | `/study/article`, runtime content loading | content-pipeline (build_ko_zh_tw.py) | Pipeline outputs to `dist/staging/ko/core/dialogue/{level}/{id}.json` but frontend expects `packages/ko/core/dialogue/{level}/{id}.json`. The packaging step needs to restructure. |
| G10 | No dictionary i18n source data exists in content-ko | `/study/dictionary` | content-ko | Content authors need to create `content/i18n/{learner_lang}/dictionary/*.json` files with translations. |

---

## 6. Schema/Contract Drift

| # | Schema/Producer Says | Artifact Has | Frontend Expects | Resolution Needed |
|---|---|---|---|---|
| D1 | `package.schema.json` requires `lang`, `version`, `modules`, `files` | Learning library `manifest.json` has `lang: "ko"`, `version: "pipeline"`, `modules: ["core","i18n"]`, `files: {...}` | `PipelineManifest.fromJson()` at l.20-46 handles both `modules` as array or map. Accepts `files` with `{core: [...], i18n: {zh_tw: [...]}}`. | Works correctly. The `PipelineManifest` parser is flexible enough. No drift. |
| D2 | `manifest.schema.json` requires `version` and `packages` (Phase 1) | `global_manifest.json` has both fields | PRG consumes `packages` array; this is Phase 1→Phase 2 contract | No drift. The schema matches the artifact. |
| D3 | `dictionary_core.schema.json` requires `atom_id` (`^[a-z]{2}:[a-z]+:.+$`), `lemma_id`, `surface_forms`, `pos`, `senses`, `source_refs` | content-ko has `index.json`/`index.csv` (not V5 atoms) | `DictionaryRepository` loads from manifest-resolved path, expects V5 atom JSON | **DRIFT** — Content source doesn't match V5 schema. Need transformation pipeline from source data to V5 atoms. |
| D4 | `grammar_core.schema.json` requires `grammar_id` (`^[a-z]{2}:g:[^:]+:[^:]+:[^:]+$`) | Content-ko grammar files use `fs_safe_id` in filenames (`ko__g__a1__...`) but likely have `grammar_id` inside JSON | `GrammarNoteService` expects `grammar_index.json` with `G-KO-*` → file path mapping | **DRIFT** — Production ID format (`G-KO-*`) differs from canonical ID format (`ko:g:...`). Need mapping layer. |
| D5 | `assembler_prototype.py:469` writes `"files": {"study_discovery": "assets/content/production/lesson_catalog.json"}` | Artifact has `"files": {"study_discovery": "..."}` | `ConfigLoader._resolveManifestFilePath()` at l.101-114 reads `manifest['files']['study_discovery']` and passes it directly to `rootBundle.loadString()`. Flutter's `rootBundle` strips `assets/` prefix — but expects paths WITHOUT the prefix. | **DRIFT** — Path should be `content/production/lesson_catalog.json` not `assets/content/production/lesson_catalog.json`. See G5. |
| D6 | `sync_video_to_frontend.py:153` writes `"files": {"study_discovery": "assets/content/production/study_discovery.json"}` | Same drift as D5 | Same issue | Same resolution as D5. |
| D7 | `assembler_prototype.py` uses `level_id` as the lesson key in manifest output (l.312: `lesson["level_id"] = lesson.get("level_id") or lesson_id`) | `manifest.json` has `lessons[].level_id` | `LessonRegistryRepository` at l.52 reads `manifestMap['lessons']` and expects `level_id` (or `lesson_id` as fallback from `LessonMetadata.fromJson()` l.62: `json['lesson_id'] ?? json['id']`) | Works today because `LessonMetadata.fromJson()` falls back to `json['id']` which would match `level_id` only by chance. The field should be `lesson_id` for consistency with `lesson_catalog.json`. |
| D8 | `dictionary_core.schema.json` `pos` enum includes `"N"`, `"V"`, `"ADJ"`, etc. (project-internal tags) | No artifact exists to check | `DictionaryRepository` doesn't validate POS | Cannot assess yet — no dictionary artifact exists. |

---

## 7. Key Observations

### Facts (not inference)

1. The `assets/` directory in `lingo-frontend-web` is entirely empty — zero files.
2. The content-pipeline has been run at least once: `dist/` contains output from a prior run with 18 video files, B2/A2 dialogues, and learning library artifacts.
3. PRG has been run in pilot mode: `staging/prg_pilot/output_strict/` contains `manifest.json`, `lesson_catalog.json`, and `production_plan.json` with 3 lessons.
4. No script in any repo produces `modular_lessons.json` or modular lesson content files.
5. No script produces `grammar_index.json` or copies grammar note JSONs to the frontend path.
6. No script produces V5 dictionary atoms (`dictionary_core.json`, `dictionary_i18n.json`) or the dictionary package manifest.
7. Content-ko has 30+ video core files, grammar core files (with `fs_safe_id` naming), and learning library i18n translations — but no V5 dictionary atoms.
8. The handoff manifest schema (`handoff_manifest.schema.json`) defines a 5-stage pipeline but no handoff manifest exists in any repo. The pipeline's `main.py` also doesn't produce one.
9. `core-schema/ID_POLICY.md` defines canonical ID formats but content-ko grammar filenames use `fs_safe_id` (double-underscore), not canonical colon-separated IDs.

### Inference

1. The pipeline has never been run end-to-end to produce frontend assets. The pilot PRG run was a manual test using staging files.
2. The dictionary and grammar pipelines are design-phase artifacts — schemas exist, but implementation is incomplete.
3. Modular lessons appear to be a planned feature with frontend routes but no backend pipeline.
4. The "V5 overhaul" referenced in `build_ko_zh_tw.py` appears partially implemented — dialogues are built, but dictionary/grammar sections are stubs.

---

## 8. Critical Path to a Working Frontend

In priority order:

1. Run `content-pipeline/main.py` (UnifiedWorkflow) to build from content-ko source → dist
2. Run `release-aggregator/scripts/release.py` to aggregate dist → `global_manifest.json`
3. Run `release-aggregator/scripts/prg/assembler_prototype.py` with `--candidate-source global_manifest.json` → `manifest.json`, `lesson_catalog.json`
4. Run `content-pipeline/scripts/sync_video_to_frontend.py` → video files + `video_metadata.json`
5. Copy all produced artifacts to `lingo-frontend-web/assets/`
6. Fix `--study-discovery-path` default (G5)
7. Implement dictionary V5 pipeline (G2)
8. Implement grammar index generator (G3)
9. Decide on modular lessons (G4) — either build pipeline or remove frontend routes
