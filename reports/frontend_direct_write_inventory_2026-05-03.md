# Frontend Direct-Write Inventory — 2026-05-03

Goal: catalog every script, Makefile target, and documented command that writes into `lingo-frontend-web/assets` or `assets/content/production` (from any of the four repos). Each entry is assessed for whether it is a direct write, whether the release-aggregator staging bridge (`sync_frontend_assets.py`) already wraps it, and what should happen next.

## Table Legend

- **Repo**: which repo the file lives in.
- **File**: relative path within the repo.
- **Command / function**: the entry point that triggers the write (Make target, main(), or direct invocation).
- **Target path(s) written**: the asset sub-tree(s) inside `lingo-frontend-web/assets/` that get touched.
- **Direct-write frontend?**: Yes / No / Read-only. "Yes" means the script opens, copies into, or otherwise mutates `lingo-frontend-web/assets/` without requiring an intermediate staging area.
- **Covered by staging bridge?**: whether `release-aggregator/scripts/sync_frontend_assets.py` currently invokes or otherwise gates this write. "Bridge IS the path" = the bridge itself performs the write. "Partially" = the bridge touches the same files via a different code path.
- **Recommendation**: keep / deprecate / migrate / remove.

---

## Inventory

| # | Repo | File | Command / function | Target path(s) written | Direct-write frontend? | Covered by staging bridge? | Recommendation |
|---|------|------|--------------------|------------------------|------------------------|----------------------------|----------------|
| 1 | release-aggregator | `scripts/sync_frontend_assets.py` | `make sync-frontend-assets` (or `make validate-frontend-assets`) | `assets/content/production/` (video + manifest), `assets/content/grammar/`, `assets/config/video_metadata.json` | Yes — deploys from worktree into frontend | Bridge IS the path | **Keep** — canonical entry point. Prefer this over all direct writes below. |
| 2 | release-aggregator | `scripts/prg/assembler_prototype.py` | `main()` writes `manifest.json`, `lesson_catalog.json`, `production_plan.json` | Writes to staging/outputs only; does **not** write to frontend directly | No | Not needed (staging-only) | **Keep** — future PRG intake path. |
| 3 | release-aggregator | `scripts/prg/seed_release_manifest.py` | `main()` reads frontend `manifest.json` / `lesson_catalog.json` | Reads only; writes PRG manifest to staging | No | Not needed (read-only) | **Keep** — seed tool for PRG. |
| 4 | content-pipeline | `scripts/sync_video_to_frontend.py` | `make sync-video-frontend FRONTEND_REPO=...` | `assets/content/production/packages/ko/video/core/`, `assets/content/production/packages/ko/i18n/{lang}/video/`, `assets/config/video_metadata.json` | Yes — but writes to whatever `--frontend-repo` is given | **Yes** — bridge calls `make sync-video-frontend` with worktree as FRONTEND_REPO, then release-aggregator merges manifests | **Keep** — bridged. Do not invoke directly against real frontend. |
| 5 | content-pipeline | `scripts/generate_video_index.py` | `main()` writes `video_metadata.json` | `lingo-frontend-web/assets/config/video_metadata.json` (hardcoded) | Yes | Partially — `sync_video_to_frontend.py` also generates `video_metadata.json` from the same data | **Deprecate** — superseded by `sync_video_to_frontend.py`. The hardcoded path makes it dangerous to run independently. |
| 6 | content-pipeline | `scripts/handoff/export_frontend_intake.py` | `make export-frontend-intake RUN_ID=...` | Writes to `release-aggregator/staging/frontend_intake/` — **not** frontend | No | Not needed (staging-only) | **Keep** — feeds the future PRG intake path. |
| 7 | content-pipeline | `pipelines/learning_library.py` | `make export-learning-library` | Writes to `dist/` — consumed by `sync_learning_library.sh` in frontend repo | No (writes to pipeline dist) | Not needed (intermediate artifact) | **Keep** — producer for learning-library sync. |
| 8 | content-pipeline | `Makefile` → `sync-video-frontend` | `make sync-video-frontend FRONTEND_REPO=...` | Delegates to `sync_video_to_frontend.py` (see row 4) | Indirect | **Yes** — invoked by bridge | **Keep** — Make target is the correct indirection. |
| 9 | content-ko | `scripts/ops/export_to_app.py` | `python3 scripts/ops/export_to_app.py` | `assets/content/production/packages/ko/core/dictionary_core.json`, `i18n/dict_ko_zh_tw.json`, `i18n/mapping.json`, `yarn/*.json`, `manifest.json`, `assets/content/grammar/` | **Yes** — hardcoded to `lingo-frontend-web/assets/content/production/packages/ko/` | **No** | **Migrate** — dictionary + dialogue assembly belongs in pipeline/PRG. This is the largest unwrapped direct-write. |
| 10 | content-ko | `scripts/ops/export_dialogue_track.py` | `python3 scripts/ops/export_dialogue_track.py --profile deploy` | `assets/content/production/packages/ko/yarn/` (plus `assets/content/staging/packages/ko/` for `--profile test`) | **Yes** — hardcoded to `lingo-frontend-web/assets/content/` | **No** | **Migrate** — dialogue export by track profile should move into PRG. Overlaps with row 9's yarn generation. |
| 11 | content-ko | `scripts/ops/export_frontend_grammar.py` | `make export-frontend-grammar FRONTEND_REPO=...` | `assets/content/grammar/notes/*.json`, `grammar_index.json` | Yes — but writes to whatever `--frontend-repo` is given | **Yes** — bridge calls this with worktree | **Keep** — bridged. Do not invoke directly against real frontend. |
| 12 | content-ko | `scripts/ops/export_learning_library_runtime.py` | `python3 ... --locale zh_tw` | Writes to `content-ko/runs/learning_library_runtime/` — **not** frontend | No | Not needed | **Keep** — produces runtime payloads for the viewer, not frontend assets. |
| 13 | content-ko | `scripts/ops/prepare_viewer_data.py` | `python3 scripts/ops/prepare_viewer_data.py` | Writes to `content-ko/scripts/tools/dict_viewer/data/` — **not** frontend | No | Not needed | **Keep** — developer tool for dict_viewer. |
| 14 | content-ko | `scripts/dev/update_polysemy.py` | `python3 scripts/dev/update_polysemy.py` | `assets/content/production/packages/ko/i18n/dict_ko_zh_tw.json`, `dict_ko_en.json` | **Yes** — hardcoded Windows paths | **No** | **Remove** — ad-hoc in-place mutator with hardcoded Windows paths. If polysemy updates are needed, they should flow through the normal dictionary pipeline. |
| 15 | content-ko | `scripts/tools/generate_mapping_patch.py` | `main()` reads legacy dict, writes patch locally | Reads `lingo-frontend-web/assets/content/production/.../dict_ko_zh_tw.json`; writes to `content/staging/` | No (reads frontend, writes locally) | Not needed | **Keep** — diagnostic tool. |
| 16 | content-ko | `scripts/tools/generate_zh_tw.py` | One-off generation script | Hardcoded Windows path to `lingo-frontend-web/assets/content/production/.../dict_ko_zh_tw.json` | **Yes** — hardcoded Windows path, write | **No** | **Remove** — stale one-off with hardcoded Windows path. |
| 17 | content-ko | `scripts/tools/generate_en.py` | One-off generation script | Hardcoded Windows path to `lingo-frontend-web/assets/content/production/.../dict_ko_en.json` | **Yes** — hardcoded Windows path, write | **No** | **Remove** — same as row 16. |
| 18 | content-ko | `scripts/archive/merge_dict.py` | Archived merge script | Hardcoded Windows path to `lingo-frontend-web/assets/content/production/.../dictionary_core.json` | **Yes** — hardcoded Windows path, write | **No** | **Remove** — already in archive. |
| 19 | content-ko | `Makefile` → `export-frontend-grammar` | `make export-frontend-grammar FRONTEND_REPO=...` | Delegates to `export_frontend_grammar.py` (see row 11) | Indirect | **Yes** — invoked by bridge | **Keep** — Make target is the correct indirection. |
| 20 | lingo-frontend-web | `scripts/sync_learning_library.sh` | `make sync-library` | `assets/artifacts/learning_library/ko/` (via `rsync` from `content-pipeline/dist/ko/`) | **Yes** — rsync within the frontend repo | **No** | **Keep** — separate data path (learning library, not production content). Not in scope for the production-asset bridge. |
| 21 | lingo-frontend-web | `scripts/sync_content.sh` | Legacy shell-based deploy from `release-aggregator/staging/{version}/` | `assets/content/production/packages/ko/dialogue/`, `assets/content/VERSION` | **Yes** | **No** (it IS an older, shell-based version of the bridge) | **Deprecate** — superseded by `sync_frontend_assets.py`. Keep as fallback documentation until PRG is fully proven. |
| 22 | lingo-frontend-web | `scripts/ci_preflight.sh` | `make ci-preflight` | Reads `assets/content/production/` and `assets/content/VERSION` | No (read-only gate) | Not needed (validation gate) | **Keep** — CI validation gate. |
| 23 | lingo-frontend-web | `finalize_a1_assets.py` | `python3 finalize_a1_assets.py` | `assets/content/production/packages/ko/yarn/*.json`, `packages/ko/manifest.json` (fixes IDs and zh-TW→zh_TW normalization) | **Yes** — mutates yarn files in place | **No** | **Remove** — one-time repair script. The fixes it applies (ID normalization, zh-TW key) should be enforced at generation time in the pipeline. |
| 24 | lingo-frontend-web | `enrich_a1_atoms.py` | `python3 enrich_a1_atoms.py` | `assets/content/production/packages/ko/yarn/*.json` (injects gold-standard atoms into yarn files) | **Yes** — mutates yarn files in place | **No** | **Migrate** — atom injection should happen in the pipeline/PRG, not as a post-hoc script on the frontend repo. |
| 25 | lingo-frontend-web | `tools/scripts/sync_manifest.py` | `python3 tools/scripts/sync_manifest.py` | `assets/config/universal_manifest.json` (wrong target), scans `assets/content/{lang}/dialogue/` (path no longer exists) | **Yes** — but wrong target and broken source path | **No** | **Remove** — stale. Hardcoded lesson IDs, wrong manifest path, source directory no longer exists. |
| 26 | lingo-frontend-web | `normalize_filenames_safe.py` | `python3 normalize_filenames_safe.py` | Renames files in `assets/audio/` (NFC normalization of filenames) | **Yes** — renames audio files in place | **No** | **Keep** — utility; not a content-asset writer. |
| 27 | lingo-frontend-web | `check_encoding.py` | `python3 check_encoding.py` | Reads `assets/audio/` and `assets/content/production/packages/ko/yarn/` | No (read-only diagnostic) | Not needed | **Keep** — diagnostic utility. |
| 28 | lingo-frontend-web | `Makefile` → `sync-video` | `make sync-video` | Delegates to `release-aggregator && make sync-frontend-assets` | No (redirects to bridge) | **Yes** (redirect) | **Keep** — convenience redirect. |
| 29 | lingo-frontend-web | `Makefile` → `validate-assets` | `make validate-assets` | Runs `flutter test test/core/asset_integrity_test.dart` | No (test-only) | **Yes** — invoked by bridge after deploy | **Keep** — validation gate. |

---

## Summary by Recommendation

### Keep (15 entries)
Rows: 1, 2, 3, 4, 6, 7, 8, 11, 12, 13, 15, 19, 20, 22, 26, 27, 28, 29
These are either correctly bridged, read-only, produce intermediate artifacts, or serve a separate data path.

### Deprecate (2 entries)
Rows: 5 (`generate_video_index.py` — superseded by `sync_video_to_frontend.py`), 21 (`sync_content.sh` — superseded by `sync_frontend_assets.py`)

### Migrate (3 entries)
Rows: 9 (`export_to_app.py` — largest gap; dictionary + dialogue assembly must move into pipeline/PRG), 10 (`export_dialogue_track.py` — overlap with row 9), 24 (`enrich_a1_atoms.py` — atom injection should be a pipeline step)

### Remove (6 entries)
Rows: 14 (`update_polysemy.py` — ad-hoc with hardcoded Windows path), 16 (`generate_zh_tw.py` — stale one-off), 17 (`generate_en.py` — stale one-off), 18 (`merge_dict.py` — archived), 23 (`finalize_a1_assets.py` — one-time repair done), 25 (`sync_manifest.py` — stale, broken paths)

---

## Critical Gap: Direct Writes NOT Covered by the Staging Bridge

Three scripts still write directly into `lingo-frontend-web/assets/` without going through the `sync_frontend_assets.py` worktree staging:

1. **`content-ko/scripts/ops/export_to_app.py`** (row 9) — writes `dictionary_core.json`, `dict_ko_zh_tw.json`, mapping, yarn dialogue files, grammar notes, and manifests.
2. **`content-ko/scripts/ops/export_dialogue_track.py`** (row 10) — writes yarn files to `production/` (and `staging/` for test profile).
3. **`lingo-frontend-web/enrich_a1_atoms.py`** (row 24) — injects gold-standard atoms into already-written yarn files.

These represent the main attack surface for asset drift between the content pipeline and the frontend. They should be the priority targets for migration into the PRG assembler or the staging bridge.

---

## Notes

- The bridge (`sync_frontend_assets.py`) today wraps **video** and **grammar** only. Video file sync remains delegated to `content-pipeline`, but package/production manifest merge is now owned by `release-aggregator`. Dictionary and learning-library regeneration are explicitly skipped by the bridge.
- The `Makefile` targets in `content-ko` and `content-pipeline` both print warnings directing users to the release-aggregator bridge (`prefer: cd ../release-aggregator && make sync-frontend-assets`), which is good hygiene.
- Several content-ko scripts still have hardcoded Windows paths (`e:\Githubs\lingo\...`) — they cannot run on macOS/Linux and are strong candidates for removal.
- The `sync_content.sh` script in lingo-frontend-web reads from `release-aggregator/staging/{version}/` and writes to `assets/content/production/packages/ko/dialogue/`. This is a legacy shell precursor to the current Python bridge and should be retired once PRG is fully proven.
