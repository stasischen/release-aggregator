---
name: knowledge-lab-review
description: Use when reviewing Korean knowledge-lab planning or migration packs for duplicate IDs, taxonomy drift, core-i18n mismatches, invalid references, OCR corruption, missing promised items, or schema-shape inconsistencies.
---

# Knowledge Lab Review

Use this skill to review knowledge-lab planning or migration work before merge.

Primary repos:

- `/Users/ywchen/Dev/lingo/release-aggregator`
- `/Users/ywchen/Dev/lingo/content-ko`
- `/Users/ywchen/Dev/lingo/lingo-curriculum-source`

## Load First

Before reviewing, read:

1. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/KNOWLEDGE_INGESTION_PLAN_V0.md`
2. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/KNOWLEDGE_FIRST_MIGRATION_PACK_V0.md`
3. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md`
4. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/CONTENT_KO_OVERLAY_MIGRATION_MAPPING.md`
5. `/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_ARTIFACT_SPEC_V0.md`

If the review is pack-specific, also read the relevant pack plan in `release-aggregator/docs/tasks/`.

## Review Contract

### Findings First

- Report concrete findings first, ordered by severity.
- Use a code-review mindset, not a brainstorming mode.
- Prefer bugs, regressions, integrity failures, and contract mismatches.
- If there are no findings, say so explicitly.

### What Counts As A Finding

Only report issues that materially affect correctness, consistency, or maintainability.

Valid finding categories:

- duplicate canonical knowledge items
- taxonomy drift or path/ID inconsistency
- core/i18n pairing mismatch
- unresolved `source_ref` or invalid targets in links/topics
- OCR or mixed-script corruption in user-facing content
- promised migration items missing from the actual diff
- schema-shape inconsistency inside the migrated pack
- broken reference rewrite after canonical renames

Do not file findings for:

- minor style preferences
- speculative future enhancements
- alternative naming choices unless they break an existing contract

## Standard Review Workflow

1. Identify the actual scope:
   - branch diff
   - working tree diff
   - or a named pack/commit
2. Check whether claimed work matches actual changed files.
3. Inspect `content-ko` canonical items before trusting new IDs.
4. Run a parity check between:
   - `content/core/learning_library/knowledge/...`
   - `content/i18n/zh_tw/learning_library/knowledge/...`
5. Search for stale legacy IDs after renames.
6. Search for unresolved references in links and topics.
7. Scan for mixed-script corruption and OCR leftovers.
8. Compare claimed deliverables against actual files and IDs.

## Required Checks

### 1. Canonical Duplication

Check whether the pack creates a second item for a concept that already exists.

Examples:

- same `surface`, same scope, different ID
- old canonical item left in place while a replacement item is added

### 2. Core / i18n Path Pairing

For every new or renamed knowledge item:

- core and i18n should both exist
- relative paths should match unless the repo explicitly supports exceptions
- filename alignment should match canonical ID policy

### 3. Reference Integrity

Check:

- `links/... target_id`
- `topics/... knowledge_refs`
- any retained `source_ref`

Report unresolved or half-migrated references.

### 4. OCR / Mixed-Script Scan

Look for:

- Hangul mixed with Latin/Han/Bengali/etc. inside Korean examples
- malformed suffix names
- corrupted teaching examples
- obvious copy/transcription artifacts

### 5. Claimed Scope vs Actual Scope

If the author says a pack migrated N items, confirm that:

- files exist
- IDs exist
- cleanup/renames are fully applied

## Useful Review Commands

Prefer fast checks:

- `git diff --name-status ...`
- `rg`
- parity checks between `core` and `i18n`
- targeted file reads for suspicious items

Example parity logic:

- compare relative JSON paths under `core/learning_library/knowledge` and `i18n/zh_tw/learning_library/knowledge`
- report missing peers

## Output Format

Each finding should include:

- severity
- file path
- tight line reference
- one-paragraph explanation of the failure and why it matters

After findings, optionally include:

- open questions
- residual risks

Do not bury findings under long summaries.
