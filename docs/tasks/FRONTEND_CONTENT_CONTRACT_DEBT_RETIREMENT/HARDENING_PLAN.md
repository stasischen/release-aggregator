# Hardening Plan

## Decision Principle

Do not remove bridge logic just because it looks ugly. Remove it only when the replacement
contract is explicit, tested, and emitted by the pipeline.

The final target is:

- unified manifest/path/locale/validation rules
- domain-specific adapters remain separate
- no frontend route or widget guesses content package layout
- no content package relies on stale aliases or hidden legacy paths

## Current Acceptable Bridges

| Bridge | Acceptable Until | Must Not Hide |
| :--- | :--- | :--- |
| `ko -> zh_tw` video locale fallback | package manifests declare supported locales | missing `ko -> en` package work |
| legacy Learning Library i18n merge | v2 canonical i18n sidecars exist | empty source translations |
| sync alias exclusions | pipeline stops emitting aliases | stale artifact layout |
| `shared_bank` UI label | manifest models example bank metadata | source-less examples |
| `mapping_v2` under i18n | resolver package placement approved | origin/cache migration risk |
| localized fields in dictionary core | strict split coverage gates pass | missing i18n pack entries |

## Suggested Schema Deltas

### Package Manifest

Add support-locale declarations:

```json
{
  "modules": {
    "dictionary": {
      "core": "dictionary_core.json",
      "i18n": {
        "zh_tw": "dict_ko_zh_tw.json"
      },
      "resolver": {
        "surface_mapping": "mapping_v2.json"
      }
    },
    "video": {
      "core": ["..."],
      "i18n": {
        "zh_tw": ["..."]
      }
    },
    "learning_library": {
      "core_manifest": "assets/artifacts/learning_library/ko/library_manifest.json"
    }
  }
}
```

### Learning Library

Model example banks explicitly:

```json
{
  "source_groups": [
    {
      "id": "shared_bank",
      "kind": "example_bank",
      "label_i18n": {
        "zh_tw": "例句庫"
      }
    }
  ]
}
```

### V2 Source I18n Sidecar

Emit canonical turn/sentence translations instead of requiring legacy path search:

```json
{
  "source_id": "src.ko.video.ewL6SaZzjyU",
  "locale": "zh_tw",
  "sentences": [
    {
      "sentence_id": "sent.src.ko.video.ewL6SaZzjyU.v_001",
      "turn_id": "v_001",
      "translation": "大家好。我是再臨。"
    }
  ]
}
```

### Dictionary

Split display text from resolver data:

```text
core/
  dictionary_core.json          canonical atom/entity data only
resolver/
  surface_mapping_v2.json       surface -> atom candidates/origin refs
i18n/zh_tw/
  dictionary_i18n.json          meanings, senses, labels, descriptions
```

## Validation Gates

- `dictionary_core.json` has no locale-keyed display fields after strict split.
- Every shipped video package has at least one supported i18n locale declared.
- Learning Library sentence i18n coverage cannot drop below the current accepted baseline
  without an explicit content-gap report.
- Frontend video dictionary lookup test uses production assets and fails on unsupported
  locale routing.
- Sync scripts fail if legacy alias files reappear in frontend runtime artifacts.

### Executable Contract Registry

The first gate is now codified in:

- `docs/tasks/assets/contracts/learning_library.package.v1.schema.json`
- `docs/tasks/assets/contracts/manifest.package.v1.schema.json`
- `scripts/validate_content_contracts.py`

Run this before accepting pipeline or frontend asset-sync changes:

```bash
python3 scripts/validate_content_contracts.py \
  --learning-library-manifest /Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko/library_manifest.json \
  --package-manifest /Users/ywchen/Dev/lingo/content-pipeline/dist/ko/packages/manifest.json \
  --require-locale zh_tw \
  --min-sentence-translations 3345
```

This prevents the common failure mode where frontend code silently reads a stale
Learning Library layout, deprecated `*_index.json` aliases, missing i18n packs,
or a package manifest pointing at files that no longer exist.

## Source-Of-Truth Enforcement

Use `SOURCE_OF_TRUTH_POLICY.md` as the operational rule for future debugging and
implementation. The policy is intentionally stricter than the current repo state:

- frontend runtime reads exported runtime artifacts only
- pipeline may read legacy only through named bridges
- agents inspect runtime artifact and manifest before grepping legacy source files
- legacy paths are quarantined by tests and bridge-retirement tasks instead of deleted
