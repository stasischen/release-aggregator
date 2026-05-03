# Frontend Asset Parity Audit - 2026-05-03

## Verdict

`content-pipeline/pipelines/learning_library.py --v2` is now runnable and can be used as a source for dictionary and learning-library artifacts, but it is not a complete frontend production sync step.

It must not overwrite `lingo-frontend-web/assets/content/production/packages/ko/manifest.json` as-is because the generated package manifest only covers dictionary and learning-library modules. The repaired frontend package manifest also needs `Strings_zh_tw.json`, `mapping.json`, and video module declarations.

## Commands Run

```bash
cd /Users/ywchen/Dev/lingo/content-pipeline
python pipelines/learning_library.py --content-repo ../content-ko --lang zh_tw --out "$TMP/dist" --v2
```

## Compatibility Fix Applied

`learning_library.py --v2` previously failed on mixed example-sentence inventory shapes:

- Older rows use `id` and `translations`.
- Newer rows use `item_id` and `translation`.

The loader now accepts both shapes.

The generated package manifest also now emits frontend-compatible dictionary file names:

```json
{
  "dictionary": {
    "core": "dictionary_core.json",
    "i18n": "dict_ko_zh_tw.json"
  }
}
```

This matches `DictionaryRepository`, which appends those names under `packages/ko/core/` and `packages/ko/i18n/`.

## Parity Summary

Compared generated output under temp `dist/ko/` with current `lingo-frontend-web/assets/content/production/`.

| Artifact | Generated Shape | Frontend Shape | Byte-Identical | Decision |
|---|---:|---:|---|---|
| `packages/core/dictionary_core.json` | `atoms=7306` | `atoms=7017` | No | Candidate upgrade, requires frontend validation before sync |
| `packages/i18n/dict_ko_zh_tw.json` | `atoms=7306` | `atoms=7017` | No | Candidate upgrade, requires frontend validation before sync |
| `packages/manifest.json` | `modules=2` | `modules=2` | No | Do not overwrite; needs merge/intake logic |
| `artifacts/core/sources_index.json` | `sources=11` | `sources=3` | No | Candidate upgrade |
| `artifacts/core/sentences_index.json` | `sentences=12` | `sentences=4` | No | Candidate upgrade |
| `artifacts/core/knowledge_index.json` | `knowledge=217` | `knowledge=217` | Yes | Safe parity |
| `artifacts/core/topics_index.json` | `topics=4` | `topics=4` | Yes | Safe parity |
| `artifacts/core/vocab_sets_index.json` | `vocab_sets=0` | `vocab_sets=0` | Yes | Safe parity |
| `artifacts/i18n/zh_tw/sources.json` | `sources=11` | `sources=3` | No | Candidate upgrade |
| `artifacts/i18n/zh_tw/sentences.json` | `sentences=12` | `sentences=4` | No | Candidate upgrade |
| `artifacts/i18n/zh_tw/knowledge.json` | `knowledge=217` | `knowledge=217` | Yes | Safe parity |
| `artifacts/i18n/zh_tw/topics.json` | `topics=4` | `topics=4` | Yes | Safe parity |
| `artifacts/i18n/zh_tw/vocab_sets.json` | `vocab_sets=0` | `vocab_sets=0` | Yes | Safe parity |

## Follow-Up Tasks

1. Add a dedicated frontend intake merge step for package manifests instead of overwriting `packages/ko/manifest.json`.
2. Validate generated `dictionary_core.json` and `dict_ko_zh_tw.json` against frontend dictionary tests before promoting generated output.
3. Keep `make export-learning-library` as an export command, not a frontend sync command.
4. Build a separate grammar note exporter; no existing script emits `grammar_index.json` plus `grammar/notes/*.json` in the frontend `GrammarNote` shape.
5. Run PRG root manifest/catalog assembly only as a dry-run until `production_plan.json` has zero gaps.
