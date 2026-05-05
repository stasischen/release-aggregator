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

Frontend video runtime currently maps unsupported Korean learner locales to `zh_tw` because
the shipped Korean video/dictionary content package only includes `zh_tw`.

- Current code: `lingo-frontend-web/lib/features/video/domain/video_locale_support.dart`
- Risk: user locale and content locale are conflated. Future `ko -> en` package support
  could be masked if the fallback is not retired.
- Retirement condition: production package manifest explicitly declares supported content
  locales per domain and frontend resolves video/dictionary locale through that manifest.

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
- Retirement condition: pipeline no longer emits stale aliases and an asset integrity gate
  fails if aliases reappear.

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
- Retirement condition: a dictionary resolver package or bridge module is defined and the
  dictionary core-origin migration Phase 3 validation passes.

### 6. Dictionary core contains localized fields

Current packaged dictionary core may include `definitions.zh_tw` and `translation.zh_tw`.

- Current output: `assets/content/production/packages/ko/core/dictionary_core.json`
- Risk: strict core/i18n separation is not enforceable; localized text can leak through
  fallback code and hide missing i18n pack coverage.
- Retirement condition: dictionary package emission strips localized display text from
  core and emits all display strings/senses through locale packs.

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

1. Add manifest-driven supported-locale resolution for dictionary/video/learning_library.
2. Add asset integrity gates for stale aliases, per-word dictionary files, and empty i18n
   regressions.
3. Move `shared_bank` semantics into Learning Library manifest/source metadata.
4. Define dictionary resolver package placement for `mapping_v2` and related bridge data.
5. Strip localized fields from dictionary core after i18n pack coverage gates pass.
6. Remove legacy i18n bridges from `content-pipeline` only after v2 inventory emits
   canonical i18n sidecars.

## Acceptance Criteria

- Every temporary bridge above has a tracking subtask with an owner, blocker, and
  retirement gate.
- Frontend tests fail if Korean video dictionary runtime silently routes to an unsupported
  i18n package.
- Pipeline tests fail if Learning Library sentence i18n coverage regresses to empty output.
- Release docs clearly state current acceptable bridge behavior versus final contract.
- Source-of-truth policy defines which runtime artifacts are authoritative and which
  legacy paths are quarantined.
- No schema change is implemented without a reviewed brief and migration plan.
