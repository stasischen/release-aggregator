# Task Brief

## Metadata

- Task ID: LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF
- Owner: release-aggregator control tower
- Target repos: `release-aggregator`, `lingo-frontend-web`
- Read-only context repo: `content-ko`
- Status: in_progress
- DeepSeek routing: flash -> pro
- Created: 2026-05-04
- Last updated: 2026-05-04

## Goal

Continue the existing Learning Library multi-layer plan by turning the deferred `LLCM-008`
handoff into an active product/frontend task.

The outcome is a Knowledge-First Lab product path that uses the existing shared graph
(`source`, `sentence`, `topic`, `knowledge_item`, `vocab_set`, dictionary refs) without
inventing a new schema and without confusing artifact intake completion with UI/product
completion.

## Background

Existing canonical planning already defines the architecture:

- `docs/guides/LEARNING_SOURCE_MULTILAYER_ARCHITECTURE.md`
- `docs/guides/KNOWLEDGE_LAB_CONTENTKO_ARCHITECTURE.md`
- `docs/tasks/assets/LLCM_005G_CORE_I18N_PACK_EMISSION_SPEC.md`
- `docs/tasks/assets/LLCM_005H_FRONTEND_COMPOSITION_INTAKE_SPEC.md`
- `docs/tasks/archive/20260428/20260428_LEARNING_LIBRARY_CONTENTKO_MIGRATION_TASKS.json`

The current gap is execution state, not architecture absence:

- `LLCM-008` was the unresolved handoff: plan the handoff from content-first prototype to future knowledge-first lab.
- `TASK_INDEX.md` previously marked `LEARNING_LIBRARY_CONTENTKO_MIGRATION` done, which hid that UI handoff work remained.
- This task now promotes `LLCM-008` into active Layer 2 work while preserving the completed artifact-migration history.
- Frontend artifact mode can load Learning Library data, but the Knowledge Lab still presents an old source/detail style instead of an index-first knowledge/topic/vocab browser.
- The frontend artifact manifest does not list `vocab_sets`, while `LLCM-005G` requires vocab set packs.

## Product Direction

Use the existing split:

- `Content-First Learning`: source entry point for video/dialogue/article/story.
- `Knowledge-First Lab`: knowledge/topic/vocab entry point for grammar book, pattern book, topic reference, and reverse lookup.

Both paths share the same graph. They must not share one main screen or collapse domain
semantics into a generic adapter.

## Scope

In scope:

- Reconcile task state and active ownership for `LLCM-008`.
- Define Knowledge-First Lab UI acceptance for current Korean assets:
  - dictionary: roughly 7000 entries
  - video/source: 20+ items
  - knowledge lab: roughly 200 knowledge items
  - sentence/example bank: existing generated learning_library sentence packs
- Define artifact contract reconciliation for `vocab_sets.json` vs `vocab_sets_index.json`.
- Define frontend route/navigation/product gates for Knowledge Lab.
- Prepare implementation packets for frontend-only UI work after the contract is accepted.

Out of scope:

- Do not change lesson runtime data format.
- Do not modify `content-ko` content files in this task unless a later content-specific subtask explicitly approves it.
- Do not modify `content-pipeline` in this task unless the artifact contract reconciliation selects a pipeline fix as the next task.
- Do not remove `mapping_v2` origin cache.
- Do not make Gemini own frontend code changes.

## Findings To Address

1. Task status drift: `LEARNING_LIBRARY_CONTENTKO_MIGRATION` was indexed as fully done while its unresolved Knowledge-First Lab handoff had not been promoted to active work.
2. Artifact naming drift: `LLCM-005G` requires `core/vocab_sets.json`, but the frontend manifest currently omits it and current assets use a different naming pattern.
3. Product mode drift: frontend artifact loading is not the same as Knowledge-First Lab product completeness.
4. Contract boundary drift: `FRONTEND_V2_INTAKE_COMPLETION` explicitly did not include dictionary, grammar, or learning-library in its resolver slice.
5. UI acceptance gap: Knowledge Lab needs index-first browse/search/filter/reverse-lookup acceptance criteria for hundreds of items.

## Acceptance Criteria

- `TASK_INDEX.md` contains this active task and no longer implies that Knowledge-First Lab handoff is complete.
- The task packet records the canonical prior docs and states that no new schema should be invented.
- A Gemini prompt exists for content/artifact inventory only.
- A Codex implementation packet exists for the next narrow frontend step.
- The task split distinguishes:
  - release-aggregator planning and reconciliation
  - content/artifact inventory
  - frontend UI implementation
  - deferred content-pipeline fix
- No frontend code changes are made before this task artifact exists.
