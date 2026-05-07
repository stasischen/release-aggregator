# Dictionary Strict Core/I18n Split Plan

Date: 2026-05-06
Task: `fccdr-06`
Repos: `lingo-frontend-web`, `content-pipeline`, `content-ko`, `release-aggregator`

## Goal

Make dictionary runtime packages enforce a clean three-way split:

1. `dictionary.core`: target-language lexical inventory and non-localized metadata
2. `dictionary.i18n`: learner-language display strings
3. `dictionary.resolver`: target-language surface candidate routing

This prevents the app from accidentally showing stale Korean-to-zh-TW data when
another learner locale or another target language is added.

## Current State

Bundled Korean package currently ships:

- `assets/content/production/packages/ko/core/dictionary_core.json`
- `assets/content/production/packages/ko/i18n/dict_ko_zh_tw.json`
- `assets/content/production/packages/ko/i18n/Strings_zh_tw.json`
- `assets/content/production/packages/ko/resolver/surface_candidates.v1.json`

Observed drift:

- Resolved in `fccdr-18`: synced `dictionary_core.json` has 7,381 atoms with
  0 localized display fields and 0 learner-locale keys.
- `dict_ko_zh_tw.json` duplicates those display fields in the i18n pack.
- Resolver placement drift was resolved in `fccdr-17`: surface candidate routing
  now lives under `dictionary.resolver`, not dictionary i18n.

This is pre-launch, so the migration should be direct rather than preserving old
runtime shapes indefinitely.

## Target Package Shape

```json
{
  "version": "5.1.0",
  "target": "ko",
  "learner_lang": "zh_tw",
  "modules": {
    "dictionary": {
      "core": "dictionary_core.json",
      "i18n": {
        "zh_tw": ["dict_ko_zh_tw.json", "Strings_zh_tw.json"]
      },
      "resolver": ["surface_candidates.v1.json"]
    }
  }
}
```

`dictionary.i18n` should be keyed by learner locale. Do not use a flat list that
mixes `dict_ko_zh_tw.json`, `Strings_zh_tw.json`, and resolver files.

## Core Contract

Allowed core fields:

- `id`
- `atom_id`
- `lemma`
- `pos`
- `display_pos_key`
- `surface_forms`
- `entries`
- `senses`
- `relations`
- `origin`
- `metadata`
- `source_refs`
- `status`
- `mapping_status`
- `tags`
- `usage_rank`
- `difficulty_rank`
- target-language proficiency metadata such as `topik_level`, `nikl_level`,
  `nikl_rank`

Forbidden core localized display fields:

- `definitions`
- `translation`
- `meaning`
- `description`
- `gloss`
- `localized`
- `i18n`
- any locale-keyed map such as `zh_tw`, `zh_cn`, `en`, `ja`, `th`

Important nuance: core may contain target-language origin data such as Hanja if
it is lexical source metadata. Core must not contain learner-language glosses or
explanations.

## I18n Contract

File: `i18n/{learner}/dict_{target}_{learner}.json`

Recommended shape:

```json
{
  "version": 1,
  "schema": "dictionary.i18n.v1",
  "target": "ko",
  "learner": "zh_tw",
  "atoms": [
    {
      "id": "ko:n:말",
      "meaning": "1. 話；言語 2. ① 話；語言；② 馬",
      "senses": [
        {
          "sense_id": "s1",
          "entry_no": "1",
          "sense_no": "1",
          "meaning": "話；言語",
          "description": null
        }
      ]
    }
  ]
}
```

Allowed i18n fields:

- `id`
- `atom_id`
- `meaning`
- `translation`
- `definitions`
- `senses`
- `description`
- `examples`
- learner-language notes or explanations

Forbidden i18n fields:

- resolver-only fields: `homograph_key`, `entry_refs`, `sense_refs`,
  `usage_rank`, `confidence`
- target inventory fields not needed for display: full `surface_forms`,
  `relations`, source refs, core status fields

I18n may include minimal `entry_no` and `sense_id` only to align display text to
core entries/senses. These are reference keys, not resolver routing.

## Resolver Contract

Use the `fccdr-05` decision:

- file path: `resolver/surface_candidates.v1.json`
- schema: `dictionary.surface_candidates.v1`
- target-language specific
- no learner-language display text
- no origin fallback cache; origin display resolves from dictionary core entries

## Frontend Migration

### Current frontend dependency points

- `DictionaryRepository.loadSurfaceCandidates()` loads
  `resolver/surface_candidates.v1.json` from `dictionary.resolver`.
- `DictionaryResolver._findRawEntry()` falls back to `_baseDict` when a language
  pack entry is missing.
- `DictionaryParser.extractMeaning()` and `DictionaryParser.extractSenses()`
  read `definitions` directly from whichever entry they receive.
- `DictionarySearchEngine` indexes definitions from both base dictionary and
  language packs, making localized search work even if i18n is missing.

### Required frontend changes

1. Stop reading display meanings/senses from core:
   - if learner pack is loaded, display fields come from i18n only
   - if i18n is missing, return a UIStrings-backed "uncollected" placeholder
     rather than silently using core localized fallback
4. Keep core lookup for lexical fields only:
   - term
   - lemma
   - POS
   - origin
   - relation metadata
5. Search can index target-language terms from core, but learner-language search
   must index only i18n packs.

### Transitional rule

Because the app is not launched, do not add long-term compatibility for
localized core. A short-lived compatibility commit is acceptable only if needed
to land pipeline and frontend in separate commits. It must be guarded by tests
that fail once strict assets are expected.

## Content Pipeline Migration

1. Emit strict `core/dictionary_core.json` with no localized display fields.
   - Status: completed in `fccdr-18`.
2. Emit learner display packs under `i18n/{learner}/`.
3. Emit `resolver/surface_candidates.v1.json`.
   - Status: resolver generation overlays i18n definitions/translation at build
     time only, preserving `sense_refs` / `entry_refs` without reintroducing
     learner display text into core.
4. Update manifest shape to use:
   - `dictionary.core`
   - `dictionary.i18n.{learner}`
   - `dictionary.resolver`
5. Preserve enough core entry/sense references so i18n and resolver can align to
   core without duplicate display data.
6. Origin cache retirement completed in `fccdr-19`; resolver no longer emits
   `origin`, `row_origin`, or `origin_candidates`.

## Validation Gates

### Package manifest gates

- `dictionary.i18n` must be a locale-keyed map, not a flat mixed list.
- `mapping.json` and `mapping_v2.json` must not be listed under
  `dictionary.i18n`.
- `dictionary.resolver` must exist and list `surface_candidates.v1.json`.

### Core gates

- Reject core atoms containing `definitions`, `translation`, `meaning`,
  `description`, `gloss`, `localized`, or `i18n`.
- Reject any core atom with top-level learner-locale keys.
- Reject core nested maps that use learner-locale keys for display fields.
- Allow target-language lexical origin fields.

### I18n gates

- Every i18n atom id must exist in core.
- Required learner locale pack coverage must stay above the current production
  baseline.
- I18n must not contain resolver-only fields.
- I18n senses may reference core `entry_no` / `sense_id`, and those references
  must exist in core.

### Resolver gates

- Every candidate `atom_id` component must exist in core.
- `entry_refs` and `sense_refs` must reference core entries/senses when present.
- Resolver must not contain learner-locale display keys.
- Resolver must not contain origin fallback fields: `origin`, `row_origin`, or
  `origin_candidates`.

## Suggested Task Split

### Slice A: Pipeline Package Shape

- Completed in `fccdr-17`: `dictionary.resolver` emission, resolver file
  placement, and locale-keyed dictionary i18n manifest structure.

### Slice B: Frontend Resolver Module Loading

- Completed in `fccdr-17`: frontend loads `surface_candidates.v1.json` from
  `dictionary.resolver` and keeps candidate/homograph UI behavior unchanged.

### Slice C: Strict Core Emission

- Strip localized fields from `dictionary_core.json`.
- Ensure i18n pack contains equivalent display coverage.
- Update frontend to reject display fallback from core.

### Slice D: Contract Validators

- Add release-aggregator schema / validator checks.
- Add frontend asset integrity tests for shipped assets.
- Add pipeline tests for strict core and resolver reference alignment.

## Acceptance Criteria

- `dictionary_core.json` has zero learner-language display fields.
- `dict_ko_zh_tw.json` remains complete enough for dictionary, video atom, and
  sentence detail display.
- `surface_candidates.v1.json` powers all surface candidate lookups.
- `surface_candidates.v1.json` contains routing refs only and has zero resolver
  origin fallback fields.
- Multi-candidate / homograph UI still works.
- Missing i18n displays a localized "uncollected" placeholder, not `[No Meaning]`
  and not stale core display text.
- Asset integrity tests fail if old mixed module placement reappears.

## Non-Goals

- Do not reintroduce mapping/origin fallback after `fccdr-19`.
- Do not rewrite lesson runtime format.
- Do not change `content-ko` source inventory in this planning slice.
- Do not reduce dictionary display quality while moving fields; i18n coverage
  must be proven before stripping core display fields.
