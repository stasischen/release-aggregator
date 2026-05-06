# fccdr-07 Blocker Recheck

Date: 2026-05-06
Task: `fccdr-07`
Status: still blocked

## Summary

`fccdr-07` cannot be completed yet.

The frontend coverage gate passes, but only because `content-pipeline` still
uses legacy i18n bridge reads from `content/i18n/...`. The blocker is not
resolved until canonical v2 Learning Library i18n sidecars exist and the
pipeline can emit runtime artifacts from those sidecars without legacy reads.

## Current Evidence

- `content-ko/content_v2/i18n` currently has 0 files.
- Pipeline v2 output can produce runtime artifacts, but output i18n is still
  sourced from legacy bridge logic.
- Current frontend assets show Learning Library sentence i18n coverage of
  `3345/3346 = 99.97%`.
- The missing translated sentence is:
  `sent.src.ko.dialogue.a1_01.L01-D1-01`.

## Coverage By Surface

| Surface | Current Runtime Coverage | Source |
| --- | ---: | --- |
| shared/example bank sentences | 2133/2133 | legacy bridge |
| video-derived source sentences | 1212/1212 | legacy video i18n bridge |
| Learning Library sentences total | 3345/3346 | legacy bridge |
| Knowledge i18n | 218 items | legacy `content/i18n/zh_tw/learning_library/knowledge` |
| dialogue source sentence | 0/1 for `a1_01` missing row | missing canonical/legacy translation |

## Legacy Bridge Locations

Current `content-pipeline/pipelines/learning_library.py` still uses legacy
bridge paths at these decision points:

- knowledge i18n fallback comment around line 180
- `_load_legacy_learning_library_i18n("knowledge", item_id)` around line 183
- shared/example sentence legacy lookup around line 239
- source metadata legacy lookup around line 280
- video/dialogue/article sentence translation from legacy translations around
  line 309
- `_load_legacy_source_i18n` around line 365
- `_load_legacy_learning_library_i18n` around line 392

These bridge reads are acceptable only while `fccdr-07` remains blocked.

## Missing Canonical Sidecars

Recommended minimum canonical v2 sidecars:

- `content_v2/i18n/zh_tw/learning_library/sources.json`
  - keyed by `source_id`
- `content_v2/i18n/zh_tw/learning_library/sentences.json`
  - keyed by `source_id` + `sentence_id`
  - video/dialogue/article rows preserve `turn_id`
- `content_v2/i18n/zh_tw/learning_library/knowledge.json`
  - keyed by `knowledge_id`
- `content_v2/i18n/zh_tw/learning_library/example_sentence.json`
  - or merged into `sentences.json`
  - shared bank must have explicit source key such as `shared_bank`
- `content_v2/i18n/zh_tw/content_assets/video.json`
  - or one sidecar per source
  - keyed by `source_id`, `turn_id`, `sentence_id`
- `content_v2/i18n/zh_tw/content_assets/dialogue.json`
  - must include the current `A1-01` missing translation

## Retirement Conditions

`fccdr-07` can move from `blocked` to implementation-ready only when all of
these are true:

1. `content-ko` emits canonical v2 i18n sidecars under
   `content_v2/i18n/zh_tw/...` or another agreed manifest path.
2. `content-pipeline` v2 lookup order is:
   - canonical v2 sidecar first
   - legacy bridge only behind an explicit fallback flag
3. A fixture run disables or removes legacy `content/i18n` and still produces
   non-empty aligned i18n artifacts.
4. Frontend Learning Library i18n coverage gate passes from synced pipeline
   output.
5. `_load_legacy_source_i18n` and `_load_legacy_learning_library_i18n` can be
   retired, or quarantined behind a named fallback flag with owner and deadline.

## Next Tasks

1. Content owner emits canonical sidecars for Learning Library source/sentence
   i18n.
2. Content owner emits canonical sidecars for knowledge i18n.
3. Content owner emits canonical sidecars for video/dialogue content asset
   sentences, including `turn_id` where applicable.
4. Pipeline owner updates lookup order and adds a no-legacy fixture test.
5. Frontend sync validates that coverage remains at or above the current floor.
