---
name: knowledge-lab-refactor
description: Use when planning or executing Korean knowledge-lab ingestion, normalization, manual migration packs, or schema/pipeline follow-up across release-aggregator, content-ko, and lingo-curriculum-source.
---

# Knowledge Lab Refactor

Use this skill for the `reports -> normalized knowledge -> content-ko learning_library/knowledge` workflow.

Primary repos:

- `/Users/ywchen/Dev/lingo/release-aggregator`
- `/Users/ywchen/Dev/lingo/content-ko`
- `/Users/ywchen/Dev/lingo/lingo-curriculum-source`

## Load First

Read these before proposing taxonomy changes or migration work:

1. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/KNOWLEDGE_INGESTION_PLAN_V0.md`
2. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/KNOWLEDGE_FIRST_MIGRATION_PACK_V0.md`
3. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md`
4. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/CONTENT_KO_OVERLAY_MIGRATION_MAPPING.md`
5. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_ARTIFACT_SPEC_V0.md`

## Scope

This skill covers:

- source inventory of `lingo-curriculum-source/reports`
- taxonomy mapping into `grammar`, `pattern`, `connector`, `expression`, `usage`
- normalization and canonical ID decisions
- manual migration packs into `content-ko`
- duplicate cleanup, typo/OCR cleanup, and integrity checks
- pipeline/schema follow-up notes

This skill does not cover:

- frontend implementation in `lingo-frontend-web`
- bulk auto-conversion as a first step
- dictionary atom design
- treating planning documents as if migration is already done

## Core Rules

### 1. Source Roles

- `reports` are migration input and historical reference
- `content-ko` is the post-normalization source of truth
- `release-aggregator` owns planning, migration rules, and task framing

### 2. Taxonomy Boundaries

- `ending` always maps to `grammar > ending`
- `connector` is only for independent lexical connectors
- `usage` is not the default bucket; prefer `usage_notes_zh_tw` or teaching blocks
- do not flatten everything into `grammar`

### 3. Canonicalization

- never derive final knowledge IDs from report filenames
- use canonical IDs based on concept, not source series numbering
- when an equivalent canonical item already exists in `content-ko`, merge into it instead of creating a duplicate
- if a migration changes taxonomy for an existing canonical item, call that out explicitly before doing it

### 4. Migration Discipline

- prefer manual migration packs before writing normalizer scripts
- keep each pack small enough to review cleanly
- remove unresolved `source_ref` values rather than inventing fake IDs
- proofread for mixed-script/OCR corruption before considering the pack done

## Standard Workflow

### Planning Mode

1. Inventory relevant reports, but keep scope bounded.
2. Map each source family to the target taxonomy.
3. Define canonical item shape, split/merge rules, and first-pack scope.
4. Write or update planning docs in `release-aggregator/docs/tasks/`.

### Migration Mode

1. Inspect existing canonical knowledge files in `content-ko` first.
2. Build or extend one migration pack at a time.
3. Add or update:
   - `content/core/learning_library/knowledge/...`
   - `content/i18n/zh_tw/learning_library/knowledge/...`
4. Merge into existing canonical items when appropriate.
5. Remove duplicate IDs or abandoned trial files.
6. Check for unresolved references, OCR corruption, and taxonomy drift.

### Review Mode

Focus findings on:

- duplicate canonical items
- taxonomy/path/ID inconsistency
- unresolved `source_ref` or link targets
- user-facing content corruption or mistranscription
- missing promised migration items

## Review Checklist

Before calling a migration pack clean, verify:

- no duplicate concepts remain under different IDs
- no unresolved `source_ref` placeholders remain
- no mixed-script corruption remains in Korean examples
- no accidental taxonomy migration happened without explicit intent
- core and i18n files are paired
- new IDs follow the canonical naming rule

## Preferred Next Step Logic

- If taxonomy or shape is still unstable: update planning docs first.
- If taxonomy is stable but migration is unproven: do a small manual pack.
- If multiple manual packs succeed cleanly: propose schema/pipeline extension.
- Only after that: propose a normalizer script.
