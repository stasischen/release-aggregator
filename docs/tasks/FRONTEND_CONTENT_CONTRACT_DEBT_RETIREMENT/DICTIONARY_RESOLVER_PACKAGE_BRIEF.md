# Dictionary Resolver Package Placement Brief

Date: 2026-05-06
Task: `fccdr-05`
Repos: `lingo-frontend-web`, `content-pipeline`, `release-aggregator`

## Decision

Create a target-language dictionary resolver package and move `mapping_v2.json`
out of the dictionary i18n module.

Recommended package boundary:

```json
{
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

The resolver package is target-language specific, not learner-locale specific.
It may contain surface-to-atom candidate routing, homograph metadata, entry/sense
references, usage rank, and temporary origin fallback data. It must not contain
learner-language display strings.

## Why Not Keep `mapping_v2` In I18n

Current shipped Korean manifest lists:

- `core/dictionary_core.json`
- `i18n/dict_ko_zh_tw.json`
- `i18n/Strings_zh_tw.json`
- `i18n/mapping.json`
- `i18n/mapping_v2.json`

But `mapping_v2.json` has `entry_schema: surface_candidates.v1` and stores:

- surface forms such as `말`, `눈`, `어요`, `는`
- ordered candidate atom ids
- `homograph_key`
- `entry_refs` and `sense_refs`
- `usage_rank`
- optional origin fallback cache

That data is resolver/origin routing metadata. It is not localized display text.
Keeping it under i18n creates three problems:

1. Locale boundary drift: every learner locale appears to own resolver data even
   though the same resolver data should serve all learner locales for the same
   target language.
2. Hidden fallback risk: UI can accidentally treat missing i18n as acceptable
   because core or resolver cache still carries display-like fields.
3. Multi-language scaling risk: adding another learner locale would duplicate
   resolver files or require undocumented sharing rules.

## Package Semantics

### Core

Core owns target-language lexical inventory:

- atom id
- lemma
- POS / display POS key
- surface forms
- entry structure
- sense ids and entry numbers
- relations
- target-language source/origin where canonical and validated
- non-localized metadata

Core must not own learner-language glosses, explanations, or localized display
strings after `fccdr-06` completes.

### I18n

I18n owns learner-language display:

- atom glosses
- sense glosses
- descriptions/explanations
- UI string tables tied to learner locale

I18n must be keyed by learner locale and must not contain surface candidate
routing.

### Resolver

Resolver owns target-language lookup bridges:

- surface to ordered candidates
- candidate atom id or composite atom id
- candidate POS key
- homograph key
- `entry_refs`
- `sense_refs`
- usage rank / confidence
- temporary origin fallback cache

Resolver may keep origin fallback fields only until core-origin migration Phase
3 validation passes. After that, origin fallback fields become deprecated and
should be removed from emitted resolver artifacts.

## Proposed Resolver Schema

File: `resolver/surface_candidates.v1.json`

```json
{
  "version": 1,
  "schema": "dictionary.surface_candidates.v1",
  "target": "ko",
  "entries": {
    "말": [
      {
        "atom_id": "ko:n:말",
        "lemma": "말",
        "pos": "n",
        "homograph_key": "말|n|ko:n:말",
        "entry_refs": [
          {
            "entry_no": "1",
            "sense_ids": ["s1"]
          }
        ],
        "sense_refs": [
          {
            "sense_id": "s1",
            "entry_no": "1"
          }
        ],
        "confidence": 1.0,
        "usage_rank": 28,
        "source": "dictionary_core.surface_forms"
      }
    ]
  }
}
```

Temporary fields allowed during migration:

- `origin`
- `row_origin`
- `entry_refs[].origin`
- `entry_refs[].origin_candidates`
- `sense_refs[].origin`

These fields are resolver cache, not learner-facing text. Frontend may display
origin only through `DictionaryResolver.getOrigin()`, with core origin winning
over resolver fallback.

## Frontend Migration Plan

### Phase 1: Add Resolver Module Loading

- Extend package manifest parsing to accept `dictionary.resolver`.
- Load resolver files from `packages/{target}/resolver/`.
- Keep a compatibility path for current bundled app only if needed during one
  transition commit, but because the app is not launched, prefer a direct
  cutover once pipeline emits the new module.
- Rename frontend concepts from `chunkMapping` to `surfaceCandidates` where it
  clarifies responsibility.

### Phase 2: Gate Package Boundaries

Add asset integrity checks:

- `mapping_v2.json` must not be listed under `dictionary.i18n`.
- resolver files must exist for every target dictionary package.
- resolver entries must reference existing core atom ids.
- resolver `entry_refs` / `sense_refs` must reference valid core entries and
  senses when present.
- i18n files must not contain resolver-only fields such as `homograph_key`,
  `entry_refs`, or `sense_refs`.

### Phase 3: Retire Origin Cache

After dictionary core-origin migration Phase 3 validation passes:

- core origin becomes the only canonical origin source.
- resolver origin cache fields are rejected by validation.
- `DictionaryResolver.getOrigin()` no longer needs resolver fallback except for
  legacy fixtures.

## Pipeline Migration Plan

1. Emit `packages/{target}/resolver/surface_candidates.v1.json` from the same
   source currently used for `mapping_v2.json`.
2. Update package manifest:
   - remove `mapping.json` / `mapping_v2.json` from `dictionary.i18n`
   - add `dictionary.resolver`
3. Keep filename schema explicit: `surface_candidates.v1.json`, not
   `mapping_v3.json`.
4. Add pipeline validation for resolver-to-core references.
5. Add package validation that no localized display strings leak into resolver.

## Current Frontend Findings

- Current runtime code loads `dictionary.resolver` from
  `resolver/surface_candidates.v1.json` and parses `entries` into
  `DictionaryMappingCandidate`.
- `DictionaryResolver.resolveSurfaceToCandidates()` uses these candidates for
  homograph and multi-candidate lookup.
- `DictionaryResolver.getOrigin()` already prioritizes core origin over mapping
  cache, which matches the migration direction.
- Tests already cover:
  - composite candidates
  - multi-candidate homographs
  - core origin winning over mapping cache
  - mapping origin cache as fallback when core origin is missing
  - no-context multi-entry core origin is not guessed

## Acceptance Criteria

- Runtime manifest has a dedicated `dictionary.resolver` module.
- Frontend loads resolver data from the resolver module, not i18n.
- `dict_{target}_{learner}.json` and `Strings_{learner}.json` remain the only
  learner-locale dictionary i18n runtime files.
- Resolver candidates still support video atom lookup, sentence detail lookup,
  dictionary candidate selection, and homograph display.
- No removal of mapping/origin fallback occurs until Phase 3 core-origin
  validation passes.

## Non-Goals

- Do not change lesson runtime format.
- Do not collapse dictionary, Knowledge Lab, Sentence Bank, or video domain
  semantics into one adapter.
- Do not remove resolver origin fallback fields until dictionary core-origin
  migration Phase 3 validation passes.
- Do not solve dictionary localized-core leakage here; that is `fccdr-06`.
