# Task Brief

## Metadata

- Task ID: FRONTEND_CONTENT_CONTRACT_DEBT_RETIREMENT
- Owner: release-aggregator control tower
- Target repos: `release-aggregator`, `lingo-frontend-web`, `content-pipeline`
- Read-only context repo: `content-ko`
- Status: queued
- DeepSeek routing: flash -> pro
- Created: 2026-05-05

## Goal

Retire the temporary bridges and hardcoded frontend content assumptions introduced while
making v2-derived Korean dictionary, video, Knowledge Bank, and Sentence Evidence usable.

This is a contract hardening task, not a UI redesign task. The immediate goal is to make
the current hardcoding explicit, add gates that prevent regression, and define the schema
decisions required before removing each bridge.

## Current Temporary Bridges

### 1. Korean video locale fallback

Frontend video runtime previously mapped unsupported Korean learner locales to `zh_tw`
because the shipped Korean video/dictionary content package only includes `zh_tw`.

- Current code: `lingo-frontend-web/lib/features/video/domain/video_locale_support.dart`
- Risk: user locale and content locale are conflated. Future `ko -> en` package support
  could be masked if the fallback is not retired.
- Retirement condition: completed for frontend in `fccdr-02`. Production package manifests
  now drive supported content locale resolution for video, dictionary, and Learning
  Library. If a requested learner locale is not packaged, runtime selects from manifest
  supported locales instead of relying on a Korean-only special case.

### 1a. English UI fallback chrome

The app already ships `assets/config/ui_strings_en.json`; this is UI chrome fallback only,
not a content translation pack.

- Current code: `lingo-frontend-web/lib/core/i18n/ui_strings_provider.dart`
- Decision: keep English UI as the safety language for app navigation and empty/error
  states, but do not synthesize `ko -> en` dictionary/video/Learning Library content until
  a real package exists.
- Guard: English UI string asset is parsed in tests, and provider parsing is BOM-safe for
  existing config files.

### 2. Learning Library v2 i18n legacy bridge

`content-pipeline` reads `content_v2/inventory/example_sentence` and
`content_v2/inventory/content_assets/video`, then merges zh_tw text from legacy
`content/i18n/zh_tw/...`.

- Current code: `content-pipeline/pipelines/learning_library.py`
- Risk: output correctness depends on path conventions and id string transforms such as
  `video:{source}:turn_v_001 -> v_001`.
- Retirement condition: v2 inventory artifacts or a canonical sidecar contain stable
  i18n records keyed by canonical `source_id`, `turn_id`, and `sentence_id`.

### 3. Sync script alias exclusions

Frontend sync excludes stale legacy alias files such as `sentences_index.json` and
`knowledge_index.json`.

- Current code: `lingo-frontend-web/scripts/sync_learning_library.sh`
- Risk: file exclusion hides output drift instead of making the pipeline contract the only
  source of truth.
- Retirement condition: frontend gate completed in `fccdr-03`. Bundled artifacts and the
  packaged Korean manifest reject stale Learning Library aliases except the canonical
  `sources_index.json` file. Pipeline cleanup remains a follow-up if emission still
  requires sync-time exclusions.

### 4. `shared_bank` frontend semantics

Sentence Evidence treats `shared_bank` as source-less example material and labels it
`Example Bank`.

- Current code: Learning Library mapper/UI in `lingo-frontend-web`.
- Risk: UI owns product semantics that should come from artifact metadata.
- Retirement condition: Learning Library core manifest models `shared_bank` or example
  banks as first-class source/source-group metadata with localized display labels.

### 5. `mapping_v2` module placement

`mapping_v2.json` is loaded from the dictionary i18n module, but it is resolver/origin
mapping data, not pure localized display text.

- Current code: `lingo-frontend-web/lib/core/repositories/dictionary_repository.dart`
- Risk: core/i18n boundary remains semantically muddy. Removing it prematurely could break
  dictionary origin and candidate disambiguation.
- Decision: completed in `fccdr-05`. `mapping_v2` / surface candidate routing belongs in
  a target-language `dictionary.resolver` module, not learner-locale i18n. The resolver
  module owns candidate ordering, homograph metadata, entry/sense references, and temporary
  origin fallback cache until core-origin Phase 3 validation passes.
- Retirement condition: a dictionary resolver package or bridge module is defined and the
  dictionary core-origin migration Phase 3 validation passes.

### 6. Dictionary core contains localized fields

Current packaged dictionary core may include `definitions.zh_tw` and `translation.zh_tw`.

- Current output: `assets/content/production/packages/ko/core/dictionary_core.json`
- Risk: strict core/i18n separation is not enforceable; localized text can leak through
  fallback code and hide missing i18n pack coverage.
- Finding: current bundled Korean core has 7,329 atoms, and all 7,329 carry
  `definitions.zh_tw` and `translation.zh_tw` duplicated with `dict_ko_zh_tw.json`.
- Decision: completed in `fccdr-06`. Dictionary packages should split into
  `dictionary.core` lexical inventory, locale-keyed `dictionary.i18n` display packs, and
  `dictionary.resolver` surface candidate routing. Frontend should not use core as a
  learner-language display fallback after strict assets are emitted.
- Retirement condition: dictionary package emission strips localized display text from
  core and emits all display strings/senses through locale packs.

### 7. Atom POS composition leaks through UI DTOs

`LingoAtom.pos` may currently contain either a displayable POS label such as `noun` /
`verb` / `particle`, or backend validation composition such as `adj+e+e`, `v+e`, or
resolver-like technical identifiers.

- Current frontend behavior: reference UI filters out POS values containing `+` or `:`
  before rendering token breakdown labels.
- Risk: one DTO field has two meanings. Frontend components must know backend debug
  conventions to avoid leaking technical composition into learner-facing UI.
- Retirement condition: atom/runtime DTOs split display POS from validation composition:
  `pos` or `display_pos_key` is learner-facing/i18n-safe, while `composition` or
  `debug_pos_composition` is backend/pipeline-only. Frontend token UI consumes only the
  display field and never parses composition strings.

### 8. Locale-specific Learning Library frontend field names

Learning Library frontend models previously encoded the current Korean to zh-TW package in
field names such as `surfaceKo`, `translationZhTw`, `titleZhTw`, and `summaryZhTw`.

- Previous code: `lingo-frontend-web/lib/features/learning_library/...`
- Risk: adding another target language or learner locale would require duplicating domain
  model fields instead of swapping content packages. It also encouraged tests and mock
  fixtures to preserve old schema names even after v2 artifacts moved to neutral fields.
- Decision: because the app is pre-launch, do not add compatibility fallbacks. Runtime
  frontend contracts use `surface`, `translation`, `title`, and `summary` directly.
- Retirement condition: completed in frontend slice `fccdr-11`; content/package validators
  should reject the old Learning Library frontend field names if they reappear in runtime
  fixtures or synced artifacts.

## Non-Goals

- Do not modify lesson runtime data format.
- Do not remove `mapping_v2` origin cache until dictionary core-origin migration Phase 3
  validation passes.
- Do not change `content-ko` source files as part of this task unless a later content
  subtask explicitly approves it.
- Do not block current UI polish or missing-word cleanup on schema retirement.
- Do not collapse domain adapter semantics. The target is unified manifest/path/locale
  rules, not unified domain meaning.

## Recommended Order

1. Keep Learning Library frontend/domain fields locale-neutral: `surface`, `translation`,
   `title`, and `summary`; do not reintroduce `Ko`/`ZhTw` suffixes in domain DTOs.
2. Keep manifest-driven supported-locale resolution for dictionary/video/learning_library.
3. Add asset integrity gates for stale aliases, per-word dictionary files, and empty i18n
   regressions.
4. Move `shared_bank` semantics into Learning Library manifest/source metadata.
5. Define dictionary resolver package placement for `mapping_v2` and related bridge data.
6. Split display POS from backend POS composition in atom/runtime DTO contracts.
7. Strip localized fields from dictionary core after i18n pack coverage gates pass.
8. Remove legacy i18n bridges from `content-pipeline` only after v2 inventory emits
   canonical i18n sidecars.

## Acceptance Criteria

- Every temporary bridge above has a tracking subtask with an owner, blocker, and
  retirement gate.
- Frontend tests fail if Korean video dictionary runtime silently routes to an unsupported
  i18n package.
- Pipeline tests fail if Learning Library sentence i18n coverage regresses to empty output.
- Frontend asset integrity tests fail if bundled Learning Library artifacts reintroduce
  stale `*_index.json` aliases, dictionary packages ship per-word i18n runtime files, or
  Learning Library/video i18n coverage drops below the configured baseline.
- Release docs clearly state current acceptable bridge behavior versus final contract.
- Source-of-truth policy defines which runtime artifacts are authoritative and which
  legacy paths are quarantined.
- No schema change is implemented without a reviewed brief and migration plan.
- Learning Library frontend/runtime code no longer uses `surfaceKo`, `translationZhTw`,
  `titleZhTw`, or `summaryZhTw` as domain or DTO fields.
