# LLLO -> V5 Dictionary + Grammar Integration Plan

Date: 2026-02-14  
Scope: `ko` target language, first learner language `zh_tw`  
Execution model: phase-by-phase with strict validation gates

## Goal

Integrate LLLO content into V5 architecture without cross-language coupling:

1. Dictionary and Grammar as structured source-of-truth.
2. Core/I18n separation (target-language core vs learner-language explanation).
3. Pipeline-generated artifacts only.
4. Frontend consumes released artifacts via contract.

## Non-Negotiable Rules

1. Core/I18n must be separated. Do not store atom core data under `ko__zh_tw` source.
2. No silent parsing failure. Every parse issue must be emitted to warnings/report.
3. Stable IDs required before build automation.
4. Legacy app compatibility transformations happen in output layer only.

## Repository Responsibilities

1. `core-schema`: schema contracts, validator, compatibility policy.
2. `content-ko`: source content, ingestion, normalization, merge rules.
3. `content-pipeline`: build/transform/validate to production artifacts.
4. `release-aggregator`: artifact collection, provenance, release manifest.
5. `lingo-frontend-web`: intake + runtime validation + integration tests.

## Data Model Baseline

### Dictionary

Core (`ko`):
- `atom_id` (stable)
- `lemma_id`
- `surface_forms[]`
- `pos`
- `senses[]`
- `source_refs[]`

I18n (`zh_tw`):
- `atom_id`
- `learner_lang`
- `gloss`
- `notes`
- `examples_translated[]`

### Grammar

Core (`ko`):
- `grammar_id` (stable)
- `pattern`
- `constraints`
- `examples[]`
- `token_refs[]` (references to `atom_id`)

I18n (`zh_tw`):
- `grammar_id`
- `learner_lang`
- `title`
- `explanation_md`
- `usage_notes`

### Stable ID Policy

1. `atom_id`: `ko:<lemma_slug>:<sense_no>`
2. `grammar_id`: `ko:g:<level>:<unit>:<slug>`

IDs must remain stable across wording edits.

## Source Layout (content-ko)

```text
content/source/ko/core/dictionary/atoms/*.json
content/source/ko/i18n/zh_tw/dictionary/*.json
content/source/ko/core/grammar/*.json
content/source/ko/i18n/zh_tw/grammar/*.json
content/source/ko/core/dialogue/*.json
```

## Phase Plan

### Phase 1: Contract Finalization (`KO-CONTRACT-01`)

Repo: `core-schema`

Deliverables:
1. `schemas/dictionary_core.schema.json`
2. `schemas/dictionary_i18n.schema.json`
3. `schemas/grammar_core.schema.json`
4. `schemas/grammar_i18n.schema.json`
5. `schemas/article_compat_grammar.schema.json`
6. `docs/CONTRACT_DICTIONARY_GRAMMAR.md`

Acceptance:
1. Example payloads validate successfully.
2. Schema versioning and breaking-change policy documented.

### Phase 2: Source Refactor (`KO-SOURCE-01`)

Repo: `content-ko`

Deliverables:
1. New source directory tree with core/i18n split.
2. Migration of existing `ko__zh_tw` dictionary/grammar source to split model.

Acceptance:
1. No core atom payload remains only under learner-specific path.

### Phase 3: Ingestion Layer (`KO-INGEST-01`)

Repo: `content-ko`

Scripts:
1. `scripts/import_lllo_raw.py`
2. `scripts/normalize_dictionary.py`
3. `scripts/normalize_grammar.py`
4. `scripts/review_report.py`

Flow:
`import_raw -> normalize -> review -> publish_candidate`

Outputs:
1. `content/staging/raw/...`
2. `content/staging/normalized/...`
3. `content/staging/reports/parse_warnings.json`

Acceptance:
1. A1-01 can run end-to-end and produce warnings report (empty allowed).

### Phase 4: Merge/Conflict Policy (`KO-MERGE-01`)

Repo: `content-ko`

Deliverables:
1. `docs/MERGE_PRECEDENCE.md`
2. conflict emitter: `content/staging/reports/conflicts.json`

Required precedence:
`manual_override > curated_dictionary > lesson_extracted`

Acceptance:
1. Conflict file generated on every run.

### Phase 5: Build Pipeline (`KO-PIPELINE-01`)

Repo: `content-pipeline`

Scripts:
1. `pipelines/build_dictionary.py`
2. `pipelines/build_grammar.py`
3. `pipelines/build_article_compat_from_grammar.py`
4. `pipelines/validate_bundle.py`

Outputs:
1. `dist/ko/core/dictionary_core.json`
2. `dist/ko/i18n/zh_tw/dictionary_zh_tw.json`
3. `dist/ko/core/grammar_core.json`
4. `dist/ko/i18n/zh_tw/grammar_zh_tw.json`
5. `dist/ko/article/grammar/*.json`

Gates:
1. Schema pass rate: 100%.
2. Duplicate `atom_id`: 0.
3. Unresolved grammar token ratio: <= threshold (define and document).

### Phase 6: Release Aggregation (`KO-RELEASE-01`)

Repo: `release-aggregator`

Deliverables:
1. Collect `core/`, `i18n/`, `article/grammar` artifacts.
2. `global_manifest.json` with provenance:
   - `source_repo`
   - `source_commit`
   - `schema_version`
   - `pipeline_version`
   - `artifact_hash`

Acceptance:
1. Staging release manifest validates against core-schema.

### Phase 7: Frontend Intake (`KO-FE-INTAKE-01`)

Repo: `lingo-frontend-web`

Deliverables:
1. Update `scripts/sync_content.sh` mapping for core + i18n + grammar-article outputs.
2. Update intake docs with explicit source->target path mapping.
3. Runtime contract: dictionary lookup uses core + i18n packs together.
4. Integration test for grammar token -> dictionary lookup.

Required checks:
1. `flutter analyze`
2. `flutter test test/core/asset_integrity_test.dart`
3. `flutter test test/repositories/event_repository_integration_test.dart`
4. `flutter test test/features/grammar/grammar_dictionary_link_test.dart`

## Handoff Contract (Every Phase)

Gemini must output:

1. `task_id`
2. `commit_hash`
3. `changed_files`
4. `commands_run`
5. `test_results`
6. `blockers`
7. `handoff_file_path` (`docs/handoffs/<task_id>_handoff.md`)

## Ready-to-Use Prompt

```text
請讀取 docs/planning/LLLO_V5_DICTIONARY_GRAMMAR_INTEGRATION_PLAN.md，
按 phase 順序執行，從 KO-CONTRACT-01 開始。

規則：
1) 嚴格遵守 Core/I18n 分層。
2) 不可跳 phase。
3) 每個 phase 完成後提交 commit，並產生 handoff。
4) 回報格式固定：
   - task_id
   - commit_hash
   - changed_files
   - commands_run
   - test_results
   - blockers
   - handoff_file_path
```
