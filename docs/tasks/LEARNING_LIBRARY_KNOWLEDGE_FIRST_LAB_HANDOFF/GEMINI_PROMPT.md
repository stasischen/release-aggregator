# Gemini Prompt

## Objective

Run a read-only content/artifact inventory for the Learning Library Knowledge-First Lab
handoff. The goal is to confirm what already exists in `content-ko`, what is emitted into
frontend artifacts, and where the current artifact naming or manifest contract drifts from
the existing LLCM plan.

Do not modify code or content.

## Context

Repos:

- Control: `/Users/ywchen/Dev/lingo/release-aggregator`
- Frontend: `/Users/ywchen/Dev/lingo/lingo-frontend-web`
- Content: `/Users/ywchen/Dev/lingo/content-ko`

Canonical prior docs:

- `/Users/ywchen/Dev/lingo/release-aggregator/docs/guides/LEARNING_SOURCE_MULTILAYER_ARCHITECTURE.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/guides/KNOWLEDGE_LAB_CONTENTKO_ARCHITECTURE.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/LLCM_005G_CORE_I18N_PACK_EMISSION_SPEC.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/LLCM_005H_FRONTEND_COMPOSITION_INTAKE_SPEC.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/TASK_BRIEF.md`

Important constraints:

- Do not invent a new schema.
- Do not change lesson runtime format.
- Do not edit frontend code.
- Do not edit `content-ko` or `content-pipeline`.
- Treat `vocab_sets` as a teaching selection layer, not dictionary truth.
- Keep dictionary truth separate from Learning Library vocab sets.

## Files / Paths To Inspect

- `/Users/ywchen/Dev/lingo/content-ko/content/core/learning_library`
- `/Users/ywchen/Dev/lingo/content-ko/content/i18n/zh_tw/learning_library`
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/learning_library`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko/library_manifest.json`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library`

## Questions To Answer

1. Counts: how many source/sentence/knowledge/topic/vocab/link artifacts exist in `content-ko` and frontend assets?
2. Contract drift: does frontend artifact output match `LLCM_005G` required pack names?
3. Manifest drift: does `library_manifest.json` list every required core/i18n pack?
4. Data readiness: do knowledge items have enough kind/subcategory/tags/refs to support index-first browse?
5. UI readiness: which frontend screens currently use source-first detail UI vs knowledge-first index UI?
6. Risk: what missing or inconsistent data would block Knowledge Lab index-first UI without changing schema?

## Required Output Format

Return a concise report with:

- Findings ordered P0/P1/P2/P3.
- Inventory table with counts and file locations.
- Contract drift table: expected vs actual pack names.
- UI readiness table: screen/route, current behavior, gap.
- Recommended next task split.
- Explicit non-goals and files not modified.

