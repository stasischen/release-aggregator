# Dialogue/Yarn Bridge Parity Inventory — 2026-05-03

## Scope

| Artifact | Path |
|---|---|
| export_dialogue_track.py | `content-ko/scripts/ops/export_dialogue_track.py` |
| export_to_app.py (dialogue/yarn features) | `content-ko/scripts/ops/export_to_app.py` |
| sync_frontend_assets.py (bridge) | `release-aggregator/scripts/sync_frontend_assets.py` |
| Frontend asset reader | `lingo-frontend-web/lib/features/study/data/repositories/study_content_locator.dart` |
| Frontend i18n overlay | `lingo-frontend-web/lib/core/services/i18n_overlay_service.dart` |

---

## 1. What files and paths does export_dialogue_track.py currently output?

**Target schema:** `<content-root>/<channel>/packages/ko/yarn/{app_id}.json`

- `content-root` → passed via `--content-root` (default: none, must be explicit)
- `channel` → `staging` (for `--profile test`) or `production` (for `--profile deploy`)
- `app_id` format → `ko_{app_level}_dialogue_{lesson_id_lowercase}.json`

**Concrete examples (A1-01):**
- Staging: `<content-root>/staging/packages/ko/yarn/ko_l1_dialogue_a1_01.json`
- Production: `<content-root>/production/packages/ko/yarn/ko_l1_dialogue_a1_01.json`

**Manifest update:** writes `manifest.json` at `<content-root>/<channel>/packages/ko/manifest.json` with `files.yarn` array containing the list of generated yarn filenames.

**Staging seeding behavior (lines 176–188):** when `target == "staging"`, `_ensure_target_package` copies `core/`, `i18n/`, `video/`, and `manifest.json` from production to staging if they don't already exist there. Production target does none of this.

**Profile config** (`content-ko/content/staging/release_tracks/ko_dialogue_tracks.json`):
```json
{
  "profiles": {
    "test":    { "levels": ["A1"], "lessons": [] },
    "deploy":  { "levels": ["A1"], "lessons": [] }
  }
}
```
Both profiles currently export only A1 (25 lessons). Levels can be extended via `--levels` CLI flag. There are 125 dialogue source files across A1–C1 (25 per level).

**Level-to-app mapping:**
| CEFR | App Code |
|---|---|
| A1 | l1 |
| A2 | l2 |
| B1 | l3 |
| B2 | l4 |
| C1 | l5 |

**Data sources used per yarn file:**
- `content/core/dialogue/{level}/{lesson_id}.json` — core dialogue turns
- `content/gold_standards/dialogue/{level}/{lesson_id}.jsonl` — atom annotations per line
- `content/i18n/zh_tw/dialogue/{level}/{lesson_id}.json` — zh_TW translations

**Yarn JSON shape per file:**
```json
{
  "id": "ko_l1_dialogue_a1_01",
  "type": "dialogue",
  "nodes": {
    "ko_l1_dialogue_a1_01": {
      "turns": [
        {
          "id": "L1",
          "role": "A",
          "text": { "ko": "...", "zh_TW": "..." },
          "content": { "atoms": [...] }
        }
      ]
    }
  }
}
```

---

## 2. What dialogue/yarn files does the frontend actually read?

**Primary read path** — `StudyContentLocator.corePath` (lines 7–15):
```
assets/content/production/packages/{lang}/core/dialogue/{baseFolder}/{lessonId}.json
```

When `type == 'yarn'`, it is remapped to `'dialogue'` for path construction (line 8: `final t = type == 'yarn' ? 'dialogue' : type`).

`baseFolder` is extracted from the lesson ID via regex `^([A-Z]\d+)-` (e.g., `A1-01` → `A1`).

**Concrete example (ko, A1-01, type=yarn):**
```
assets/content/production/packages/ko/core/dialogue/A1/A1-01.json
```

**i18n path** — `StudyContentLocator.i18nPath` (lines 18–27):
```
assets/content/production/packages/{lang}/i18n/{locale}/dialogue/{baseFolder}/{lessonId}.json
```

**Current ground truth: the `core/dialogue/` directory does not exist in the frontend repo.** The only file under `packages/ko/core/` is `dictionary_core.json`. No dialogue content is deployed to production today.

`I18nOverlayService.loadAndMergeEvent` (lines 29–44) is the first content-load attempt in the event pipeline. It calls `StudyContentLocator.corePath` and `StudyContentLocator.i18nPath`. When both fail (which they will today since the directories don't exist), the catch at line 93 returns `null`, and `EventRepository` falls back to `atomReferenceHandler.loadAtom` (line 79) using the same `StudyContentLocator.corePath` — which also fails for the same reason.

**The critical finding:** the frontend reads from `core/dialogue/{level}/{lessonId}.json` but both exporter scripts write to `yarn/{app_id}.json`. These are different directory names AND different file names. This is the root parity gap.

**What the frontend does serve today:**
- 3 grammar-heavy modular lessons: `packages/ko/lessons/{lessonId}/build/lesson_content.v1.json`
- ~29 video lessons: `packages/ko/video/core/{videoId}.json` + `packages/ko/i18n/zh_tw/video/{videoId}.json`
- Dictionary: `packages/ko/core/dictionary_core.json`, i18n JSONs, mapping.json
- Grammar notes: `assets/content/grammar/notes/{grammar_id}.json`

No dialogue/yarn content is live.

---

## 3. If the release-aggregator bridge calls export_dialogue_track.py, would it overwrite or delete existing production assets?

**Short answer: no direct path collision, but the bridge does not currently call it.**

**Path analysis:**

| What | Path |
|---|---|
| export_dialogue_track.py writes | `{worktree}/production/packages/ko/yarn/` |
| Frontend reads dialogue from | `{worktree}/production/packages/ko/core/dialogue/` |
| Existing production assets | `{worktree}/production/packages/ko/{core/,i18n/,video/,lessons/}` |

The `yarn/` directory does not overlap with `core/dialogue/`, `core/`, `lessons/`, or `video/`. So writing to `yarn/` would not overwrite or delete existing production assets. The `yarn/` directory already exists at `packages/ko/yarn/` but is empty.

**Bridge wiring status:**

`sync_frontend_assets.py` currently handles only:
- `make sync-video-frontend` (line 268) — video assets via content-pipeline Makefile
- `export_frontend_grammar.py` (line 280) — grammar notes
- `update_video_manifests` / `update_production_manifest` (lines 275, 188) — video lesson entries in manifests

It does **not** call `export_dialogue_track.py`. The bridge comment at lines 1–9 explicitly states it "intentionally wires only generators that are currently safe to run."

The bridge also uses a worktree pattern (line 261): `prepare_worktree` copies `PRODUCTION_REL` and `GRAMMAR_REL` to a staging worktree first, generators write to the worktree, then `deploy_from_worktree` copies back to the frontend repo in one batch. This pattern would protect against partial overwrites if export_dialogue_track.py were added.

**Manifest collision risk:** export_dialogue_track.py writes `files.yarn` to `packages/ko/manifest.json`. The current production manifest.json at `packages/ko/manifest.json` uses a `modules` structure (not `files`). If export_dialogue_track.py's `_update_manifest` overwrites this manifest, it would destroy the `modules.dictionary`, `modules.learning_library`, and `modules.video` entries. This is a real risk that needs attention before wiring into the bridge — the manifest format differs between the two systems.

---

## 4. Is export_to_app.py's dialogue/grammar functionality ready for formal deprecation?

**Dialogue: yes, but conditional on path alignment.**

export_to_app.py's `aggregate_dialogues`:
- Hardcoded to levels A1, A2, B1 only (B2, C1 excluded)
- Writes to `<package-root>/yarn/` — same wrong path as export_dialogue_track.py
- Uses `unified_content_item_loader.load_dialogue_normalized_items` for atom resolution (content_v2 pipeline) vs export_dialogue_track.py's gold_standards JSONL approach
- No profile/rollout support — exports all discovered lessons unconditionally
- App ID format identical to export_dialogue_track.py: `ko_l1_dialogue_{lowercase_id}`

export_dialogue_track.py is a strict superset: it has all 5 levels, profile-based rollout, `--keep-existing-yarn` for incremental deploys, and `--levels`/`--lessons` CLI overrides.

**Grammar: partially superseded.**

export_to_app.py `sync_grammar` (lines 200–206) does a raw file copy from `i18n/zh_tw/grammar/*.json` to the target grammar root. This is a simplistic copy with no processing, no index, and no skipping logic.

export_frontend_grammar.py (called by the bridge at line 281) does proper note generation: reads core grammar data + i18n explanations, builds structured notes with `grammar_id`, `title`, `explanation_md`, and `example_sentence_refs`, produces a `grammar_index.json`, and skips entries with missing data. This is the production-quality path.

**Dictionary: not compared in this inventory** — export_to_app.py's `aggregate_dictionary` uses content_v2 inventory manifests. The bridge does not currently handle dictionary, and this inventory is scoped to dialogue/yarn/grammar.

**Deprecation recommendation:**

| Feature | Ready? | Condition |
|---|---|---|
| `aggregate_dialogues` | Yes | After path mismatch is resolved and bridge wires export_dialogue_track.py |
| `sync_grammar` | Yes | Already superseded by export_frontend_grammar.py in the bridge |
| `aggregate_dictionary` | No | No replacement wired in the bridge yet |

---

## 5. Codex-ready minimal change list and files that must not be touched

### Must-change files (minimal)

**A. Frontend: `study_content_locator.dart`** — align read path with exporter write path, **OR**

**B. Exporter: `export_dialogue_track.py`** — align write path with frontend read path.

Two possible resolutions:

**Resolution A (change frontend to read `yarn/` with app_id naming):**
- Edit `study_content_locator.dart` `corePath` and `i18nPath` to construct `packages/ko/yarn/{app_id}.json` when type is yarn/dialogue
- Requires app_id resolution logic: `ko_{levelToApp[level]}_dialogue_{lessonId.lowercase}.json`
- Also update `i18n_overlay_service.dart` if it makes assumptions about file shape from path

**Resolution B (change exporter to write `core/dialogue/` with lesson_id naming):**
- Edit `export_dialogue_track.py` `_build_yarn` to output to `core/dialogue/{level}/{lesson_id}.json` instead of `yarn/{app_id}.json`
- Update `_ensure_target_package` to manage `core/dialogue/` directory instead of `yarn/`
- Update `_update_manifest` accordingly

Resolution B is likely lower-risk because the frontend already resolves paths from lesson IDs naturally.

### Must-change files (bridge wiring)

**`release-aggregator/scripts/sync_frontend_assets.py`:**
- Add a method to call `export_dialogue_track.py` against the staging worktree
- Wire it into `main()` (e.g., behind a `--skip-dialogue` flag, analogous to `--skip-video`)
- Ensure the manifest update from export_dialogue_track.py is compatible with the existing modules-based manifest format (or transform after the fact)
- The bridge currently calls `content-pipeline` Makefile for video; dialogue generation lives in `content-ko`, so the call pattern would be a direct `python3` invocation, similar to how `export_frontend_grammar.py` is called at line 280

### Files that must NOT be changed

| File | Why |
|---|---|
| `content-ko/scripts/ops/export_to_app.py` | Legacy V5 exporter; being deprecated. Any changes here create dual-maintenance burden. Let it atrophy. |
| `lingo-frontend-web/lib/features/study/data/adapters/modular_lesson_adapter.dart` | Handles `lesson_content.v1.json` format (modular lessons), not yarn/dialogue files. Different concern entirely. |
| `lingo-frontend-web/lib/features/study/data/adapters/course_discovery_adapter.dart` | Reads from production manifest `lessons[]` and lesson_catalog; doesn't touch dialogue file paths directly. |
| `lingo-frontend-web/assets/content/production/manifest.json` | Generated artifact. Should be updated by bridge, not hand-edited. |
| `lingo-frontend-web/assets/content/production/packages/ko/manifest.json` | Generated artifact. Same reason. |
| `content-ko/content/staging/release_tracks/ko_dialogue_tracks.json` | Can be updated to add levels as rollout progresses, but that's a content decision, not a code fix. |

### Additional considerations

**Manifest format divergence:** The current `packages/ko/manifest.json` (modules-based) and the manifest format that `export_dialogue_track.py` writes (files-based) are incompatible. The exporter's `_update_manifest` creates `{"files": {"yarn": [...]}}` while the existing manifest has `{"modules": {"dictionary": {...}, "learning_library": {...}, "video": {...}}}`. Before wiring into the bridge, the exporter must either adopt the modules format or the bridge must merge safely.

**i18n dialogue files:** The frontend's `I18nOverlayService` expects i18n data at `i18n/{locale}/dialogue/{level}/{lessonId}.json`. The content-ko repo has these at `i18n/zh_tw/dialogue/{level}/{lessonId}.json`. These must be copied to the frontend alongside the yarn files, or bundled into the yarn JSON directly (which is what both exporters currently do — translations are inlined into the yarn `text` field).

**Atom reference handler:** In `EventRepository` (line 79), the fallback path uses `atomReferenceHandler.loadAtom(finalPath)`. The `finalPath` comes from `StudyContentLocator.corePath`. If the path format changes, this handler must also understand the new path or the yarn file shape.

---

## Summary

The dialogue/yarn export pipeline has a fundamental path mismatch: exporters write to `yarn/` with app_id naming, while the frontend reads from `core/dialogue/` with lesson_id naming. Neither resolution is large in lines of code, but both touch the critical read/write contract between content-ko and the frontend. The bridge (`sync_frontend_assets.py`) does not currently call any dialogue exporter, so zero dialogue content is deployed to production. The manifest format incompatibility between the modules-based and files-based schemas is a secondary but real collision risk that must be resolved before wiring.

**Inventory date:** 2026-05-03
**Source files examined:** 6 (3 Python, 3 Dart)
**Dialogue source lessons available (content-ko):** 125 (A1–C1, 25 each)
**Dialogue lessons deployed to frontend:** 0
