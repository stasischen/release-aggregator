# V2 i18n Bridge Findings

Date: 2026-05-05

## Summary

The observed missing Chinese text in Knowledge Bank and video-backed sentence detail was not a content authoring gap.

- Grammar knowledge zh_tw explanations already exist in the Learning Library i18n artifact under `explanation_md`.
- V2 atomized video source files under `content_v2/inventory/content_assets/video` do not carry inline translations.
- Legacy video translations already exist under `content/i18n/zh_tw/video`.
- The Learning Library pipeline previously only looked for inline `turn.translations`, so v2 video sentence i18n emitted as empty strings.

## Confirmed Counts

- `assets/artifacts/learning_library/ko/i18n/zh_tw/knowledge.json`: `207 / 218` knowledge items have non-empty `explanation_md`.
- After frontend fallback to `description`, `217 / 218` knowledge items have displayable zh_tw detail text.
- Remaining missing display detail: `kg.grammar.copula.polite_yeyo_ieyo`.
- `content-ko/content/core/video`: `29` legacy video source files.
- `content-ko/content/i18n/zh_tw/video`: `29` legacy video translation files.
- `content-ko/content_v2/inventory/content_assets/video`: `10` atomized Learning Library video source files in this checkout.
- After pipeline bridge fix, Learning Library video sentence i18n for the 10 exported video sources is `1212 / 1212`.
- Example: `src.ko.video.ewL6SaZzjyU` is now `70 / 70`, with `v_001` translated as `大家好。我是再臨。`.

## Chain Diagnosis

There are two related but separate frontend content chains:

1. Video runtime package chain

This chain already bridges 29/29 atomized video sidecars into frontend video runtime packages. It is tracked by `V2_ATOMIZED_RUNTIME_FRONTEND_BRIDGE_FIX`.

2. Learning Library source/sentence chain

This chain reads `content_v2/inventory/content_assets/video`. That inventory currently contains only 10 video JSON files, and those files are atomized but do not include zh_tw translations. The pipeline must merge existing legacy i18n by source id and turn id.

## Implemented Repair

- `content-pipeline/pipelines/learning_library.py` now loads legacy source i18n for v2 source assets.
- V2 video turn ids such as `video:ewL6SaZzjyU:turn_v_001` are mapped to legacy translation keys such as `v_001`.
- `lingo-frontend-web/scripts/sync_learning_library.sh` now syncs `dist/ko/artifacts` when the pipeline emits the package layout, preserving the frontend loader contract:
  - `assets/artifacts/learning_library/ko/core/...`
  - `assets/artifacts/learning_library/ko/i18n/zh_tw/...`
  - `assets/artifacts/learning_library/ko/library_manifest.json`
- `content-pipeline/pipelines/learning_library.py` now cleans stale legacy output paths before emission. The current schema does not allow frontend dictionary runtime to ship per-word JSON files; dictionary runtime output is `dist/ko/packages/core/dictionary_core.json` plus `dist/ko/packages/i18n/dict_ko_zh_tw.json`.

## Remaining Content/Contract Follow-Up

- Decide whether Learning Library should export all 29 videos or keep a curated 10-source Knowledge Bank subset.
- If the target is all 29, promote the missing 19 video atomized sources into `content_v2/inventory/content_assets/video` or teach the Learning Library pipeline to consume the canonical 29/29 atom sidecars.
- Keep this separate from video runtime atom playback, which already has its own completed bridge.
- Add a zh_tw Learning Library knowledge i18n sidecar for `kg.grammar.copula.polite_yeyo_ieyo` or map it to the existing lesson grammar note if this item should remain user-facing.
