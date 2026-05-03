# Frontend Asset Generation/Sync — Inspection Report

Date: 2026-05-03
Scope: `release-aggregator`, `content-pipeline`, `content-ko`, `lingo-frontend-web`
Goal: Find the smallest durable automation path to reproduce the frontend production assets that were manually repaired in `lingo-frontend-web`.

---

## 1. Verdict

The automation already exists but is **fragmented across three repos and partially broken**. Two scripts in `content-pipeline` can already reproduce most of the repaired assets. The main gap is that no single Makefile target runs them end-to-end, and several stale scripts create confusion. The fix is wiring, not writing new code.

---

## 2. Existing Reusable Scripts

| Script | Repo | Assets it already produces/copies | Notes |
|---|---|---|---|
| `pipelines/learning_library.py --v2` | content-pipeline | `dictionary_core.json`, `dict_ko_zh_tw.json`, `manifest.json` (package), learning_library artifacts under `artifacts/` | Reads from `content-ko/content_v2/inventory/dictionary/manifest.json`. Writes to `--out` dir. Key script. |
| `scripts/sync_video_to_frontend.py` | content-pipeline | `video/core/*.json`, `i18n/zh_tw/video/*.json`, `manifest.json` (package, video module), `manifest.json` (production, lessons list), `video_metadata.json` | Reads `content-ko/content/core/video/` + `content-ko/content/i18n/`. Directly writes into `lingo-frontend-web/assets/`. |
| `scripts/handoff/export_frontend_intake.py` | content-pipeline | `dictionary_core.json`, `dict_ko_zh_tw.json`, `Strings_zh_tw.json`, `mapping.json`, `manifest.json` (package) | Reads from release-aggregator staging handoffs. Writes to an output-root. |
| `scripts/ops/export_to_app.py` | content-ko | `dictionary_core.json`, `dict_ko_zh_tw.json`, `mapping.json`, dialogue yarn files, grammar notes, package manifest | Reads V2 inventory. Writes directly into `lingo-frontend-web/assets/`. Runs `aggregate_dictionary()` + `aggregate_dialogues()` + `sync_grammar()`. |
| `scripts/sync_learning_library.sh` | lingo-frontend-web | Learning library artifacts (`sources_index.json`, `sentences.json`, etc.) | Wrapper around `rsync` from `content-pipeline/dist/ko/` to `assets/artifacts/learning_library/ko/`. Functional. |
| `scripts/sync_content.sh` | lingo-frontend-web | Dialogue files under `packages/ko/dialogue/` | Reads from `release-aggregator/staging/`. Only covers dialogue. |
| `pipelines/build.py` | content-pipeline | Dialogue tokenized JSON, video core + i18n copies (to staging) | Reads `content-ko/content/core/dialogue/` + video. Writes to staging dir. Requires engine. |
| `main.py run --v2` | content-pipeline | Unified: runs verify, V2 export, packaging | The `--v2` flag delegates build to `learning_library.py --v2`. |

---

## 3. Stale / Duplicate / Unsafe Scripts

| Script | Repo | Problem |
|---|---|---|
| `tools/scripts/sync_manifest.py` | lingo-frontend-web | Scans `assets/content/{lang}/dialogue/*.json` — path no longer exists. Outputs to `assets/config/universal_manifest.json` (wrong target). Hardcoded lesson IDs for `ko_l0_001_hangul_1` etc. **STALE** |
| `scripts/tools/generate_zh_tw.py` | content-ko | Hardcoded Windows path (`e:\Githubs\lingo\...`). Writes directly to frontend's `dict_ko_zh_tw.json` with hardcoded translation map. **UNSAFE** |
| `scripts/tools/generate_en.py` | content-ko | Same Windows hardcode pattern. **UNSAFE** |
| `scripts/tools/generate_mapping_patch.py` | content-ko | References `proposed_core.json` (file not present in repo). Windows hardcoded path. **UNSAFE/STALE** |
| `scripts/tools/generate_dictionary_core.py` | content-ko | Generates individual atom files under `content/core/dictionary/atoms/`, NOT the consolidated `dictionary_core.json` the frontend needs. **MISLEADING NAME** |
| `scripts/tools/generate_dictionary_i18n.py` | content-ko | Same: individual i18n atom files, not the frontend payload. **MISLEADING NAME** |
| `scripts/build.sh` | content-pipeline | Runs `python3 scripts/build.py` — but `build.py` is in `pipelines/`, not `scripts/`. **BROKEN** |
| `Makefile` `sync-prod` target | content-ko | Runs `generate_dictionary_core.py` + `generate_dictionary_i18n.py` which produce atom files, not frontend payloads. **MISLEADING TARGET NAME** |
| `enrich_a1_atoms.py` | lingo-frontend-web | One-off repair script. **ARCHIVE** after automation is live. |
| `finalize_a1_assets.py` | lingo-frontend-web | One-off repair script. **ARCHIVE** after automation is live. |

---

## 4. Asset-to-Script Provenance Mapping

Each repaired asset and which existing script can regenerate it:

| Asset | Can be produced by |
|---|---|
| `assets/content/production/manifest.json` | `sync_video_to_frontend.py` (updates lessons), `export_to_app.py` (updates yarn entries) — **no single script builds it from scratch; it was manually composed** |
| `assets/content/production/lesson_catalog.json` | **No script found** — likely manually created |
| `assets/content/production/packages/ko/manifest.json` | `learning_library.py --v2` (writes dictionary + library modules), `sync_video_to_frontend.py` (adds video), `export_to_app.py` (adds yarn). **Merge needed.** |
| `packages/ko/core/dictionary_core.json` | `learning_library.py --v2` (as `{"atoms": [...]}`), `export_frontend_intake.py` (full dict), `export_to_app.py` (V2 inventory aggregation) — **format may differ between scripts** |
| `packages/ko/i18n/dict_ko_zh_tw.json` | `learning_library.py --v2` (as `{"atoms": [...]}`), `export_frontend_intake.py`, `export_to_app.py` |
| `packages/ko/i18n/Strings_zh_tw.json` | **Only** `export_frontend_intake.py` (from handoff content-translate stage) |
| `packages/ko/i18n/mapping.json` | `export_frontend_intake.py` (from tokenize stage), `export_to_app.py` (copies from content-ko source) |
| `assets/content/grammar/grammar_index.json` | **No script found** |
| `assets/content/grammar/notes/*.json` | `export_to_app.py` (sync_grammar — copies from `content-ko/content/i18n/zh_tw/grammar/`) |
| `packages/ko/video/core/*.json` | `sync_video_to_frontend.py`, `build.py` (process_videos) |
| `packages/ko/i18n/zh_tw/video/*.json` | `sync_video_to_frontend.py`, `build.py` |

---

## 5. Proposed Command Surface

### 5.1 content-pipeline/Makefile — targets to add

```makefile
sync-video-frontend:
	python3 scripts/sync_video_to_frontend.py

export-learning-library:
	python3 pipelines/learning_library.py \
	  --content-repo ../content-ko \
	  --lang zh_tw \
	  --out dist \
	  --v2

export-frontend-intake:
	python3 scripts/handoff/export_frontend_intake.py \
	  --run-id $(RUN_ID) \
	  --lang ko \
	  --ui-lang zh-TW
```

### 5.2 lingo-frontend-web — new Makefile

```makefile
.PHONY: sync-video sync-library validate-assets ci-preflight

sync-video:
	python3 ../content-pipeline/scripts/sync_video_to_frontend.py

sync-library:
	./scripts/sync_learning_library.sh

validate-assets:
	flutter test test/core/asset_integrity_test.dart
	flutter test test/features/learning_library/data/repositories/learning_library_artifact_verification_test.dart

ci-preflight:
	./scripts/ci_preflight.sh
```

---

## 6. Tests That Validate These Assets

### 6.1 In `lingo-frontend-web/test/`

| Test file | What it validates | Uses real assets? |
|---|---|---|
| `test/core/asset_integrity_test.dart` | production manifest, lesson catalog, package manifest, `dictionary_core.json`, `dict_ko_zh_tw.json`, `Strings_zh_tw.json`, `mapping.json`, grammar index + notes, video core + i18n | Yes |
| `test/features/learning_library/data/repositories/learning_library_artifact_verification_test.dart` | Learning library artifact graph integrity via `FileSystemAssetBundle` pointing to test fixtures | Fixtures |
| `test/features/learning_library/data/repositories/learning_library_content_repository_test.dart` | Content repository lookups | Yes (directory-level) |
| `test/features/learning_library/data/services/learning_library_lookup_test.dart` | Lookup service resolution | Fixtures |
| `test/features/learning_library/smoke_verification_test.dart` | Smoke verification | Fixtures |
| `test/features/dictionary/presentation/widgets/dictionary_content_golden_test.dart` | Dictionary rendering golden test | Yes |
| `test/content/content_validation_test.dart` | P0-P2 content validation | Mock data only |
| `test/test_helper.dart` | Sets up mock assets for test environments | N/A |

### 6.2 In `content-ko/tests/` and `scripts/tools/`

- `test_rules_engine.py`, `test_tokenizer_core.py`, `test_task5_ac.py` — engine quality
- `validate_dictionary_schema.py` — dictionary schema conformance

### 6.3 In `content-pipeline/`

- `tests/test_cloze_generator.py` — unit test
- `ci/smoke_test.sh` — CI smoke

---

## 7. Codex-Ready Tasks (Safest → Riskiest)

### T1: Add `sync-video-frontend` target to `content-pipeline/Makefile`

- **Risk**: None (script already works)
- **File**: `/Users/ywchen/Dev/lingo/content-pipeline/Makefile`
- **Change**: Add `.PHONY` target calling `scripts/sync_video_to_frontend.py`
- **Why first**: The video sync script is already proven — it writes directly to `lingo-frontend-web/assets/` and updates both manifest files. Zero risk.

### T2: Add `export-learning-library` target to `content-pipeline/Makefile`

- **Risk**: Low (script works, `--v2` flag already implemented)
- **File**: `/Users/ywchen/Dev/lingo/content-pipeline/Makefile`
- **Change**: Add target calling `learning_library.py --v2` with content-repo and out dir
- **Why second**: The V2 learning library export is the source of truth for `dictionary_core.json`, `dict_ko_zh_tw.json`, and manifest. However, the output format (`{"atoms": [...]}`) may differ from the manually repaired format — verify parity before declaring done.

### T3: Create `lingo-frontend-web/Makefile` with `sync-video`, `sync-library`, `validate-assets`, `ci-preflight`

- **Risk**: Low (wraps existing scripts and flutter test)
- **File**: `/Users/ywchen/Dev/lingo/lingo-frontend-web/Makefile` (new)
- **Change**: New file with the four targets
- **Why third**: This is the final wiring step in the frontend repo. The scripts it calls already exist and work.

### T4: Fix `content-pipeline/scripts/build.sh` or delete it

- **Risk**: None (it's already broken)
- **File**: `/Users/ywchen/Dev/lingo/content-pipeline/scripts/build.sh`
- **Change**: Either fix to call `pipelines/build.py` or delete
- **Why**: Currently points to `scripts/build.py` which doesn't exist.

### T5: Audit output parity: `learning_library.py --v2` vs manually repaired files

- **Risk**: Medium (discovery of format mismatches)
- **Action**: Run `learning_library.py --v2`, diff `dictionary_core.json` and `dict_ko_zh_tw.json` against the repaired versions. Document differences.
- **Why before T6-T9**: Must know whether the scripts produce byte-identical output or need adjustments.

### T6: Extend or replace `export_frontend_intake.py` to cover remaining gaps

- **Risk**: Medium (touches handoff pipeline, which may not be stable)
- **Gaps**: `lesson_catalog.json` (no script produces this), `grammar_index.json` (no script produces this), unified `manifest.json` (no single script builds it from scratch)
- **File**: `/Users/ywchen/Dev/lingo/content-pipeline/scripts/handoff/export_frontend_intake.py`
- **Why**: This script already produces `dictionary_core.json`, `dict_ko_zh_tw.json`, `Strings_zh_tw.json`, `mapping.json`, and package manifest. Adding grammar index generation and lesson catalog generation here consolidates the handoff.

### T7: Archive stale scripts in `content-ko/scripts/tools/` and `lingo-frontend-web/`

- **Risk**: Low (only affects scripts already identified as stale)
- **Files to archive**:
  - `content-ko/scripts/tools/generate_zh_tw.py`
  - `content-ko/scripts/tools/generate_en.py`
  - `content-ko/scripts/tools/generate_mapping_patch.py`
  - `lingo-frontend-web/tools/scripts/sync_manifest.py`
  - `lingo-frontend-web/enrich_a1_atoms.py`
  - `lingo-frontend-web/finalize_a1_assets.py`
- **Rename**: Add `.archived` suffix or move to an `archive/` directory.
- **Why after T5**: Parity audit confirms the replacement scripts work before retiring the old ones.

### T8: Consolidate `export_to_app.py` (content-ko) logic into `content-pipeline`

- **Risk**: Medium-High (cross-repo move, multiple asset types)
- **What to move**: `aggregate_dictionary()`, `aggregate_dialogues()`, `sync_grammar()` functions into `content-pipeline/scripts/handoff/export_frontend_intake.py` or a new module
- **Why late**: `export_to_app.py` writes directly into `lingo-frontend-web/assets/` from content-ko. Per the documented data flow, content-pipeline should own this step. But this is a cross-repo refactor — do it after T1-T7 prove the pipeline is stable.

### T9: Add `validate-assets` to CI (lingo-frontend-web GitHub Actions)

- **Risk**: Low (tests exist, just need CI wiring)
- **File**: `.github/workflows/ci.yml` in lingo-frontend-web
- **Change**: Add step to run `flutter test test/core/asset_integrity_test.dart`
- **Why last**: Tests exist and pass. This is just wiring the CI to catch regressions.

---

## 8. Do-Not-Touch List

These files must NOT be modified or deleted:

- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/manifest.json` — the repaired asset itself
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/lesson_catalog.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/manifest.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/core/dictionary_core.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/i18n/dict_ko_zh_tw.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/i18n/Strings_zh_tw.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/i18n/mapping.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/grammar/grammar_index.json` — repaired asset
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/grammar/notes/*.json` — repaired assets
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/video/core/*.json` — repaired assets
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/i18n/zh_tw/video/*.json` — repaired assets
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/test/core/asset_integrity_test.dart` — the validation gate
- `/Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py` — the core generation script (may need format adjustment, but do not restructure)
- `/Users/ywchen/Dev/lingo/content-pipeline/scripts/sync_video_to_frontend.py` — proven working sync script
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/manifest.json` — source of truth for dictionary inventory

---

## 9. Smallest Durable Automation Path

The chain that reproduces the widest set of repaired assets with the fewest script changes:

```
content-ko/content_v2/inventory/dictionary/manifest.json
    │
    ▼
content-pipeline/pipelines/learning_library.py --v2
    │  produces: dictionary_core.json, dict_ko_zh_tw.json, package manifest.json,
    │            + all learning_library artifacts
    ▼
content-pipeline/scripts/sync_video_to_frontend.py
    │  produces: video/core/*, video/i18n/zh_tw/*, updates both manifests
    ▼
lingo-frontend-web/scripts/sync_learning_library.sh
    │  copies: learning_library artifacts from dist/ to assets/artifacts/
    ▼
lingo-frontend-web: flutter test test/core/asset_integrity_test.dart
    │  validates: everything
```

**Missing from this chain** (needs T6): `Strings_zh_tw.json` (only `export_frontend_intake.py` via handoff), `grammar_index.json` (no script), `lesson_catalog.json` (no script), grammar notes (only `export_to_app.py`).

**Fallback for missing gaps**: `content-ko/scripts/ops/export_to_app.py` already handles grammar notes, yarn dialogues, and can be invoked as a standalone step until T8 merges it into content-pipeline.

---

## Appendix A: One-Way Data Flow (from RELEASE_ASSET_STRATEGY.md)

```
1. lllo (Raw Markdown/Yarn)
2. content-<lang> (Atomic Source)
3. content-pipeline (Build & Package)
4. release-aggregator (Release Orchestration)
5. lingo-frontend-web (Customer Intake)
```

---

## Appendix B: Current Makefile Targets (Existing)

### content-pipeline/Makefile
- `run` — Runs full unified pipeline
- `baseline-set` — Establish parity baseline
- `baseline-check` — Check against baseline
- `verify` — Mapping verification

### content-ko/Makefile
- `pipeline` — Run mapping pipeline
- `audit` — Audit token frequencies
- `unify` — Standardize dictionary filenames
- `sync-prod` — Generate Core/I18N skeletons (MISLEADING — produces atom files, not frontend)
- `validate-learning-library` — Validate learning library schema
- `validate-dictionary` — Validate dictionary schema
- `validate` — Both validations
- `validate-video-atoms` — Validate video atom schemas
- `cleanup` — Remove cache/staging

### release-aggregator/Makefile
- `gsd` — GSD protocol shim
- `sync-tasks` — Sync task JSONs
- `ingest-ko` — Unified Korean ingestion
- `check` — Dictionary/content quality gates
- `test-prg` — PRG tests
- `check-tlg` — TLG pattern gate
- (various TLG/Gemini targets)

### lingo-frontend-web
- **No Makefile exists**

---

## Appendix C: File Inventory

### Files read (evidence):

**content-pipeline:**
- `/Users/ywchen/Dev/lingo/content-pipeline/Makefile`
- `/Users/ywchen/Dev/lingo/content-pipeline/README.md`
- `/Users/ywchen/Dev/lingo/content-pipeline/main.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/pipelines/build.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/scripts/sync_video_to_frontend.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/scripts/handoff/export_frontend_intake.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/scripts/handoff/run_handoff_stage.py`
- `/Users/ywchen/Dev/lingo/content-pipeline/scripts/build.sh`

**content-ko:**
- `/Users/ywchen/Dev/lingo/content-ko/Makefile`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/generate_dictionary_core.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/generate_dictionary_i18n.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/generate_zh_tw.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/generate_mapping_patch.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/generate_en.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/tools/validate_dictionary_schema.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/export_to_app.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/build_unified_content_release_manifest.py`

**release-aggregator:**
- `/Users/ywchen/Dev/lingo/release-aggregator/Makefile`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/guides/RELEASE_ASSET_STRATEGY.md`

**lingo-frontend-web:**
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/scripts/sync_content.sh`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/scripts/sync_learning_library.sh`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/tools/scripts/sync_manifest.py`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/scripts/ci_preflight.sh`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/test/core/asset_integrity_test.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/test/content/content_validation_test.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/test/helpers/content_test_helper.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/test/features/learning_library/data/repositories/learning_library_artifact_verification_test.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/docs/operations/content_artifact_intake.md`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/docs/operations/asset_tracking_policy.md`
