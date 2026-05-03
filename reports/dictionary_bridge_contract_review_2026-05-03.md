# Dictionary V5 Frontend Assets Bridge Readiness Review

**Date**: 2026-05-03
**Status**: Draft / Contract Review
**Scope**: Cross-repo dictionary asset flow (content-ko -> content-pipeline -> release-aggregator -> lingo-frontend-web)

## 1. Frontend Runtime Requirements

The `lingo-frontend-web` runtime (specifically `DictionaryRepository.dart`) expects a strict package-based structure.

### Required Files & Paths
All paths are relative to `assets/content/production/packages/ko/`:

| Filename | Module | Relative Path | Schema / Structure |
| :--- | :--- | :--- | :--- |
| `manifest.json` | N/A | `./manifest.json` | `PipelineManifest` (version, modules, files mapping) |
| `dictionary_core.json` | `core` | `./core/dictionary_core.json` | V5 Core Atom Map (keyed by `atom_id`) |
| `dict_ko_zh_tw.json` | `i18n` | `./i18n/dict_ko_zh_tw.json` | V5/V4 I18n Atom Map (keyed by `atom_id`) |
| `Strings_zh_tw.json` | `i18n` | `./i18n/Strings_zh_tw.json` | UI/Lesson String Map (keyed by ID or index) |
| `mapping.json` | `i18n` | `./i18n/mapping.json` | Surface-to-AtomID map (legacy/runtime lookup) |

### Contract Details
- **Case Sensitivity**: Frontend handles `zh_tw` vs `zh_TW` via normalization, but prefers lowercase `zh_tw` in filenames.
- **Manifest Dependency**: The `DictionaryRepository` does *not* hardcode sub-paths; it queries the `manifest.json` for the `core` and `i18n` modules to find the actual filenames.

---

## 2. Content-Pipeline Capabilities & Gaps

### Current Scripts
- **`pipelines/learning_library.py`**: 
    - **Capability**: Can generate `dictionary_core.json` and `dict_ko_zh_tw.json` directly from V2 Inventory (JSONL shards).
    - **Status**: Production-ready for "Global Dictionary" export.
- **`scripts/handoff/export_frontend_intake.py`**:
    - **Capability**: Generates a full package (including `manifest.json`, `Strings_zh_tw.json`, and `mapping.json`) from a specific handoff `RUN_ID`.
    - **Status**: Used for per-lesson or per-run updates.

### Identified Gaps
1.  **Orchestration Gap**: No single command currently aggregates the "Global Dictionary" (from `learning_library.py`) with the "Lesson Strings/Mapping" (from handoffs) into a single "Master Bridge Source".
2.  **Mapping Source**: `mapping.json` is still primarily sourced from `content-ko/content/i18n/zh_tw/mapping.json`. The pipeline needs to ensure this is synced or regenerated during the bridge run.

---

## 3. Release-Aggregator Bridge Configuration

The `sync_frontend_assets.py` script is the designated bridge.

### Proposed Source Paths
The bridge should read from a "Staging Source" prepared by `content-pipeline`:
- **Source**: `content-pipeline/dist/ko/` (where `learning_library.py --out dist` emits).
- **Files to Copy**:
    - `packages/ko/manifest.json`
    - `packages/ko/core/dictionary_core.json`
    - `packages/ko/i18n/dict_ko_zh_tw.json`
    - `packages/ko/i18n/Strings_zh_tw.json`
    - `packages/ko/i18n/mapping.json`

### Staging Source Logic
The bridge should **not** run the heavy generators itself. It should:
1.  Expect `content-pipeline/dist/ko` to be populated.
2.  Perform a `prepare_worktree` copy.
3.  Execute `make validate-assets` in the frontend repo before final deployment.

---

## 4. Read-Only / Dry-Run Validation

Yes, a safe validation path is possible without deployment.

### Dry-Run Workflow
1.  **Aggregator Side**: Add a `--dry-run` flag to `sync_frontend_assets.py`.
2.  **Staging Worktree**: Use the existing `prepare_worktree` logic which creates a temporary directory.
3.  **Cross-Repo Gate**: Run `make validate-assets FRONTEND_REPO=<staged_worktree>` from the `content-pipeline` or `aggregator`.
4.  **Integrity Test**: The frontend's `test/core/asset_integrity_test.dart` already validates if the manifest matches the files on disk. This can be run against the staging directory.

---

## 5. Codex-ready Modification List

### Minimal Changes
1.  **`content-pipeline/Makefile`**: Add a target `export-bridge-dictionary` that runs `learning_library.py` and copies `mapping.json`/`Strings_zh_tw.json` from `content-ko` into a unified `dist/` structure.
2.  **`release-aggregator/scripts/sync_frontend_assets.py`**:
    - Remove the "Dictionary skipped" warning.
    - Add a `copy_dictionary` step in `main()` that pulls from `content-pipeline/dist/ko`.
    - Allow `--skip-dictionary` for safety during initial rollout.
3.  **`release-aggregator/Makefile`**: Wire the `sync-frontend-assets` to call the new pipeline export target if dictionary sync is requested.

### Acceptance Criteria
- [ ] `sync_frontend_assets.py` completes without manual path intervention.
- [ ] `lingo-frontend-web/assets/content/production/packages/ko/manifest.json` contains valid references to the new JSON files.
- [ ] `make validate-assets` in `lingo-frontend-web` passes (0 failures).
- [ ] The generated `dictionary_core.json` passes the V5 schema validation in `content-pipeline`.
