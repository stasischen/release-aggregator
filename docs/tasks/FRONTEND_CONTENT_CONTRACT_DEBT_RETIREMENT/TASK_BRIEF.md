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
`content_v2/inventory/content_assets/video`, then merges learner-language text
from canonical `content_v2/i18n/<locale>/learning_library` sidecars.

- Current code: `content-pipeline/pipelines/learning_library.py`
- Risk: output correctness depends on path conventions and id string transforms such as
  `video:{source}:turn_v_001 -> v_001`.
- 2026-05-06 cutover: content-pipeline commit `c2bfba7` reads canonical sidecars first
  and only reads legacy `content/i18n` behind explicit `--allow-legacy-i18n-bridge`.
  The current missing row is `sent.src.ko.dialogue.a1_01.L01-D1-01`.
- Retirement condition: completed for sidecar-first default path. Final fallback symbol
  removal and the release-side `forbid` gate are tracked by `fccdr-14`.

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

### 5. Dictionary resolver module placement

Surface candidate routing used to be loaded as `mapping_v2.json` from the
dictionary i18n module, but it is resolver/origin mapping data, not pure
localized display text.

- Current code: `lingo-frontend-web/lib/core/repositories/dictionary_repository.dart`
- Risk: core/i18n boundary remains semantically muddy. Removing it prematurely could break
  dictionary origin and candidate disambiguation.
- Decision: completed in `fccdr-05`. `mapping_v2` / surface candidate routing belongs in
  a target-language `dictionary.resolver` module, not learner-locale i18n. The resolver
  module owns candidate ordering, homograph metadata, entry/sense references, and temporary
  origin fallback cache until core-origin Phase 3 validation passes.
- Status: package placement completed in `fccdr-17`. Runtime now loads
  `resolver/surface_candidates.v1.json`, and package/asset gates reject
  `mapping.json` / `mapping_v2.json` under dictionary i18n.
- Remaining retirement condition: dictionary core-origin migration Phase 3
  validation passes, then the temporary origin fallback fields inside resolver
  candidates can be removed.

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
- Status: completed in `fccdr-18`. Dictionary package emission strips localized display
  text from core, keeps display strings/senses in locale packs, and builds resolver
  references by overlaying i18n only during resolver package generation.
- Retirement condition: completed; package and frontend gates now reject localized display
  leakage back into `dictionary_core.json`.

### 7. Atom POS composition leaks through UI DTOs

`LingoAtom.pos` may currently contain either a displayable POS label such as `noun` /
`verb` / `particle`, or backend validation composition such as `adj+e+e`, `v+e`, or
resolver-like technical identifiers.

- Current frontend behavior: reference UI filters out POS values containing `+` or `:`
  before rendering token breakdown labels.
- Risk: one DTO field has two meanings. Frontend components must know backend debug
  conventions to avoid leaking technical composition into learner-facing UI.
- Finding: current bundled assets expose 54 unique video atom `pos` values and 158 unique
  Sentence Bank atom `pos` values. Many are composition chains such as `adj+e+e`, `v+e`,
  and `n+cop+e`.
- Decision: completed in `fccdr-10`. Runtime atom contracts should preserve Korean `+`
  composition and composite ids, add learner-facing `display_pos_key`, and add an
  automated composition-to-display mapping table. Only unknown/ambiguous mappings need
  review. Frontend learner UI should consume `display_pos_key` and must not render
  composition strings as POS labels.
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
- Do not remove resolver origin fallback fields until dictionary core-origin migration
  Phase 3 validation passes.
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
5. Keep dictionary surface candidates in `dictionary.resolver`, not learner-locale i18n.
6. Split display POS from backend POS composition in atom/runtime DTO contracts.
7. Strip localized fields from dictionary core after i18n pack coverage gates pass.
8. Cut `content-pipeline` over to canonical Learning Library i18n sidecars and quarantine
   or remove legacy bridge reads.

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
