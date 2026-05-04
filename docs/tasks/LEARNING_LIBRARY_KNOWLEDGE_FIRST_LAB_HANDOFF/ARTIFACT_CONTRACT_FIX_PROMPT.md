# Artifact Contract Fix Prompt

## Objective

Fix the Learning Library artifact emission contract drift before Knowledge-First Lab UI
implementation proceeds.

This is a contract/content artifact task, not a frontend UI task.

## Context

Repos:

- Control: `/Users/ywchen/Dev/lingo/release-aggregator`
- Pipeline: `/Users/ywchen/Dev/lingo/content-pipeline`
- Content: `/Users/ywchen/Dev/lingo/content-ko`
- Frontend assets for verification: `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko`

Relevant files:

- `/Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py`
- `/Users/ywchen/Dev/lingo/content-ko/content/core/learning_library/vocab_sets`
- `/Users/ywchen/Dev/lingo/content-ko/content/i18n/zh_tw/learning_library/vocab_sets`
- `/Users/ywchen/Dev/lingo/content-ko/content/core/learning_library/links`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko/library_manifest.json`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/LLCM_005G_CORE_I18N_PACK_EMISSION_SPEC.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/INVENTORY_DRIFT_REPORT.md`

## Confirmed Drift

- `content-pipeline/pipelines/learning_library.py` writes `core/vocab_sets_index.json`, but `LLCM-005G` requires `core/vocab_sets.json`.
- Frontend `library_manifest.json` omits `vocab_sets` from core and i18n lists.
- Current emitted `core/vocab_sets_index.json` is empty even though `content-ko/content/core/learning_library/vocab_sets` has source files.
- Current emitted `core/links.json` is empty even though `content-ko/content/core/learning_library/links` has source files.
- `topics.json` contains `source_refs` such as `src.ko.video.79Pwq7MTUPE`, while `sources_index.json` uses bare IDs such as `79Pwq7MTUPE`.

## Required Fix Scope

Prefer the smallest pipeline/content fix that makes artifacts match the existing contract:

1. Emit canonical `core/vocab_sets.json`.
2. Include `vocab_sets.json` in `library_manifest.json` core list.
3. Include `vocab_sets.json` in i18n manifest list when the i18n file exists.
4. Ensure vocab set source files are actually loaded into emitted artifacts.
5. Ensure links source files are actually loaded into emitted artifacts, or explicitly document why links remain deferred.
6. Normalize source refs consistently across `sources_index`, `topics`, and links, or document the canonical ID policy and update emission accordingly.

## Hard Constraints

- Do not change lesson runtime data format.
- Do not invent a new Learning Library schema.
- Do not move dictionary truth into vocab sets.
- Do not edit frontend UI.
- Do not remove frontend compatibility fallback until new artifacts are generated and validated.
- Keep changes narrow and add/adjust tests or validation commands.

## Acceptance Criteria

- Generated artifacts contain non-empty `core/vocab_sets.json` when source vocab sets exist.
- Generated artifacts contain non-empty `core/links.json` when source links exist, or a tracked follow-up explains why links are intentionally deferred.
- `library_manifest.json` lists every required core/i18n pack per accepted contract.
- Topic/source refs resolve under one canonical ID policy.
- Validation command and output are provided.

## Required Output

Return:

- Files changed.
- Exact validation commands run.
- Before/after artifact counts.
- Any deferred items with reason.

