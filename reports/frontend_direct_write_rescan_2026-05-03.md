# Frontend Direct-Write Rescan — 2026-05-03

Follow-up to the [2026-05-03 inventory](frontend_direct_write_inventory_2026-05-03.md). This rescan focuses on whether the three "migrate" candidates have been cleaned of hardcoded `lingo-frontend-web` output paths, and catalogs any remaining direct-write surfaces.

---

## 1. Three Migrate Scripts — Hardcoded-Path Verification

| # | Script | Repo | Previously had hardcoded frontend path? | Now clean? | Verdict |
|---|--------|------|----------------------------------------|------------|---------|
| 1 | `scripts/ops/export_to_app.py` | content-ko | Had default output to frontend | **Yes** — `--package-root` and `--grammar-root` now required; description warns "do not point this directly at lingo-frontend-web" | **Clean** |
| 2 | `scripts/ops/export_dialogue_track.py` | content-ko | Had default output to frontend | **Yes** — `--content-root` now required; description warns "Prefer release-aggregator staging instead of writing to lingo-frontend-web directly" | **Clean** |
| 3 | `enrich_a1_atoms.py` | lingo-frontend-web | Previously auto-walked frontend yarn dir | Removed after parity review confirmed atom injection is covered by `export_dialogue_track.py` and PRG intake | **Removed** |

**结论：三个 migrate scripts 均已不再有 hardcoded `lingo-frontend-web` output path。** 所有写入目标现由调用者通过 `--package-root`、`--content-root`、`--yarn-root` 显式传入。

---

## 2. Direct-Write Script Inventory (All Four Repos)

### 2.1 Scripts that write into `assets/content/production/` or `assets/content/grammar/`

| # | Script | Repo | Trigger | Path structure hardcoded? | Bridge wraps it? |
|---|--------|------|---------|--------------------------|------------------|
| A1 | `scripts/sync_frontend_assets.py` | release-aggregator | `make sync-frontend-assets` | Yes (bridge IS the path) | Bridge itself |
| A2 | `scripts/sync_video_to_frontend.py` | content-pipeline | `make sync-video-frontend FRONTEND_REPO=...` | Yes — hardcodes `assets/content/production/packages/ko/...` and `assets/config/video_metadata.json` relative to `--frontend-repo` | **Yes** — bridge calls with worktree |
| A3 | `scripts/ops/export_frontend_grammar.py` | content-ko | `make export-frontend-grammar FRONTEND_REPO=...` | Yes — hardcodes `assets/content/grammar/...` relative to `--frontend-repo` | **Yes** — bridge calls with worktree |
| A4 | `scripts/ops/export_to_app.py` | content-ko | Direct invocation with `--package-root` + `--grammar-root` | No — explicit args only | **No** — not yet wrapped |
| A5 | `scripts/ops/export_dialogue_track.py` | content-ko | Direct invocation with `--content-root` | No — explicit arg only | **No** — not yet wrapped |
| A6 | `enrich_a1_atoms.py` | lingo-frontend-web | Removed | N/A | N/A |

### 2.2 Scripts that write into `assets/artifacts/learning_library/`

| # | Script | Repo | Trigger | Writes to frontend? |
|---|--------|------|---------|---------------------|
| B1 | `scripts/sync_learning_library.sh` | lingo-frontend-web | `make sync-library` | **Yes** — rsync from `content-pipeline/dist/` into `assets/artifacts/learning_library/` |
| B2 | `pipelines/learning_library.py` | content-pipeline | `make export-learning-library` | No — writes to `dist/` (intermediate) |

### 2.3 Scripts that write to release-aggregator staging (not frontend directly)

| # | Script | Repo | Output |
|---|--------|------|--------|
| C1 | `scripts/handoff/export_frontend_intake.py` | content-pipeline | `release-aggregator/staging/frontend_intake/<run_id>/` |
| C2 | `scripts/prg/assembler_prototype.py` | release-aggregator | `release-aggregator/staging/prototype_output/` |
| C3 | `scripts/prg/seed_release_manifest.py` | release-aggregator | Staging only (reads frontend, writes staging) |

### 2.4 Read-only scripts that still reference `lingo-frontend-web` by name

| # | Script | Repo | What it does |
|---|--------|------|-------------|
| D1 | `scripts/tools/generate_mapping_patch.py` | content-ko | Removed stale read-only diagnostic |
| D2 | `scripts/dev/gap_analysis.py` | content-ko | Removed stale Windows-only diagnostic |

---

## 3. Hardcoded Frontend Path Inventory

### 3.1 Hardcoded `lingo-frontend-web` literals in source code (non-help-string)

| Script | Line | Content | Severity |
|--------|------|---------|----------|
| `content-ko/scripts/dev/gap_analysis.py` | N/A | Removed | No remaining source reference |
| `content-ko/scripts/tools/generate_mapping_patch.py` | N/A | Removed | No remaining source reference |

### 3.2 Hardcoded `assets/content/...` path suffixes (relative to variable root)

| Script | Lines | Path suffix | Context |
|--------|-------|------------|---------|
| `content-pipeline/scripts/sync_video_to_frontend.py` | 133, 135 | `assets/content/production/packages/ko/...`, `assets/config/video_metadata.json` | Relative to `--frontend-repo` arg |
| `content-ko/scripts/ops/export_frontend_grammar.py` | 42 | `assets/content/grammar/...` | Relative to `--frontend-repo` arg |
| `content-ko/scripts/ops/export_dialogue_track.py` | 171 | `{staging\|production}/packages/ko/...` | Relative to `--content-root` arg |

### 3.3 Help strings that mention `lingo-frontend-web` (warnings, OK)

These are intentional warnings directing users away from direct writes. Not a problem.

- `export_to_app.py:212` — "do not point this directly at lingo-frontend-web"
- `export_dialogue_track.py:212` — "Prefer release-aggregator staging instead of writing to lingo-frontend-web directly"
- `export_frontend_grammar.py:33` — "staging bridge instead of writing to lingo-frontend-web directly"

### 3.4 Hardcoded absolute developer paths (machine-specific)

| Script | Path |
|--------|------|
| `content-pipeline/scripts/batch_ingest_jaerim.py` | `/Users/ywchen/Dev/lingo/content-pipeline/.venv/bin/python3`, `.../release-aggregator` |
| `content-pipeline/scripts/refill_subtitles.py` | `/Users/ywchen/Dev/lingo/content-pipeline/.venv/bin/python3`, `.../content-ko/content/core/video/`, `.../release-aggregator` |
| `content-pipeline/scripts/handoff/export_frontend_intake.py` | `--handoff-root` default: `/Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs` |
| `content-pipeline/scripts/handoff/run_handoff_stage.py` | Multiple defaults under `/Users/ywchen/Dev/lingo/` |
| `lingo-frontend-web/normalize_filenames.py` | `audio_base = "/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/audio"` |
| `lingo-frontend-web/normalize_filenames_safe.py` | `audio_base = "/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/audio"` |
| `lingo-frontend-web/check_encoding.py` | `yarn_dir = "/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/..."` |

---

## 4. Docs Still Referencing Direct Writes

| Doc | Content | Status |
|-----|---------|--------|
| `content-ko/docs/archive/DIRECTORY_STRUCTURE.md:22` | `lingo-frontend-web/assets/content/production/packages/ko` | **Archived** — explicitly marked as archive; says "NEVER write back" |
| `content-pipeline/README.md:33` | "Syncs video/dialogue assets and updates frontend manifests." | **Descriptive** — documents what `sync-video-frontend` does, but does not instruct direct writes |
| `lingo-frontend-web/docs/operations/content_artifact_intake.md` | Documents using `sync_content.sh` (deprecated redirect) and `sync_learning_library.sh` with absolute paths | **Stale** — references deprecated `sync_content.sh` and hardcoded paths to `../release-aggregator` |

No actively maintained doc was found that **recommends** writing directly into `lingo-frontend-web/assets/` without going through the release-aggregator staging bridge.

---

## 5. Safe-to-Remove Candidates

| # | File | Repo | Reason |
|---|------|------|--------|
| R1 | `enrich_a1_atoms.py` | lingo-frontend-web | Removed after migrate-script parity review. |
| R2 | `scripts/dev/gap_analysis.py` | content-ko | Removed stale Windows-only diagnostic. |
| R3 | `scripts/tools/generate_mapping_patch.py` | content-ko | Removed stale diagnostic dependent on frontend dictionary assets. |
| R4 | `lingo-frontend-web/docs/operations/content_artifact_intake.md` | lingo-frontend-web | Stale; references deprecated `sync_content.sh` and hardcoded file paths. The canonical doc is now `release-aggregator/docs/`. |

---

## 6. Still-Migrate Candidates (not yet bridged)

| # | Script | Gap | Priority |
|---|--------|-----|----------|
| M1 | `content-ko/scripts/ops/export_to_app.py` | Dictionary + dialogue assembly not yet wrapped by bridge. Bridge (`sync_frontend_assets.py`) explicitly comments: "Dictionary and learning-library assets are validation-gated here but not regenerated by this bridge yet." Must move dictionary generation into `content-pipeline` (PRG `export_frontend_intake.py`) and wire up a `sync_dictionary` step in the bridge. | **P1** |
| M2 | `content-ko/scripts/ops/export_dialogue_track.py` | Profile-based dialogue export not yet wrapped by bridge. Short-term: bridge should call this (as it does for grammar). Long-term: legacy yarn format will be superseded by PRG `course.package.json`. | **P1** |
| M3 | `content-pipeline/scripts/sync_video_to_frontend.py` + `content-ko/scripts/ops/export_frontend_grammar.py` | Already bridged via `sync_frontend_assets.py`, but both still hardcode `assets/content/...` path suffixes. If the frontend asset tree layout ever changes, these break. Consider making the path suffixes configurable or defined in a single contract file. | **P2** |
| M4 | `content-pipeline/scripts/handoff/export_frontend_intake.py` | PRG course package generated to staging, but no bridge step yet to deploy it into frontend. This is the future replacement for legacy yarn + dictionary, but the bridge doesn't consume it yet. | **P2** |

---

## 7. Summary

**Three migrate scripts verified clean.** `export_to_app.py` and `export_dialogue_track.py` no longer contain hardcoded `lingo-frontend-web` output paths. `enrich_a1_atoms.py` has been removed because its atom injection is covered by `export_dialogue_track.py` and PRG intake.

**Remaining hardcoded `lingo-frontend-web` references** are confined to:
- Warning/help strings in 3 export scripts (intentional, directing users to the bridge)
- 1 archived doc (`DIRECTORY_STRUCTURE.md`)
- Several machine-specific absolute developer paths (e.g., `normalize_filenames.py`)

**Attack surface status:**
- Direct writes through the bridge (video + grammar): **covered**
- Direct writes not yet bridged (dictionary + legacy dialogue): **still open** (M1, M2)
- Separate data path (learning library): **out of scope** for production-asset bridge
- Deprecated redirects (`sync_content.sh`, `sync-video` Makefile target): **safe compatibility wrappers**

**No new direct-write surfaces were introduced.** The three scripts that were modified moved in the right direction (from hardcoded defaults to explicit required arguments). The next priority is P1: wire up dictionary and dialogue into the staging bridge.
