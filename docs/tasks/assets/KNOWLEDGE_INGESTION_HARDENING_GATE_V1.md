# Knowledge Ingestion Hardening Gate V1

**Task ID**: `kg-normalize-001`
**Status**: Draft
**Owner Repo**: `release-aggregator`
**Scope**: Curriculum-source ingestion hardening, pre-promotion validation, and manual review gating for `content-ko`

## 1. Objective

Define the hard gate that must sit between curriculum-source ingestion and canonical `content-ko` promotion.

The gate exists to prevent schema-valid but semantically broken batches from entering the canonical corpus.

## 2. Problem Statement

Recent ingest waves show four recurring failure classes:

1. Legacy nested payloads leak into V5-style content.
2. Title / summary fields can be polluted by UI fallback text.
3. Translation fields may be empty while the batch is still marked complete.
4. Example references can repeat, drift, or point at non-canonical targets.

JSON validity alone does not catch these failures.

## 3. Gate Model

Every batch must pass the following gates in order:

1. `schema_gate`
2. `content_gate`
3. `manual_review_gate`
4. `promotion_gate`

Only `approved` batches may be promoted into canonical `content-ko`.

## 4. Required Checks

### 4.1 Schema Gate

The batch must conform to the frozen V5 contract:

- Flat fields only.
- No legacy nested wrappers such as `zh_TW: { ... }`.
- Required canonical fields must be present and typed correctly.
- Generated IDs must follow the canonical slug pattern and must not contain placeholder tokens such as `unknown` or malformed suffixes such as `..v1`.

### 4.2 Content Gate

The batch must also satisfy semantic minimums:

- `title` must be content-derived, not UI fallback copy.
- Translation fields may not be silently empty.
- `description` / `summary` / `note` fields may not be filled with template noise.
- `explanation` content must not absorb teacher talk, repeated fragments, or example sentence fragments.
- `example_sentence_refs` must be unique and resolvable.
- Shared-usage rows must point at a concrete existing canonical example, not an implied placeholder.

### 4.3 Manual Review Gate

Automated validation is necessary but not sufficient.

Human review must confirm:

- The batch is semantically coherent.
- Shared-usage merge or retain decisions are correct.
- The `example_sentence` bank is not being polluted with duplicate canonical IDs.
- The batch did not move pedagogical material into the wrong field.

### 4.4 Promotion Gate

Promotion is allowed only when:

- schema gate passes
- content gate passes
- manual review status is `approved`
- the batch has no unresolved hard blockers

## 5. Workflow

1. Generate draft artifacts into staging or scratch.
2. Run machine validation.
3. Produce a review note with explicit findings.
4. Apply manual review decisions.
5. Promote only approved items into canonical `content-ko`.
6. Re-run validation after promotion.

## 6. Acceptance Criteria

This task is complete when:

- hard gate rules are written down clearly enough to be enforced by automation
- manual review is a required promotion step
- canonical promotion is no longer allowed from unchecked generator output

## 7. Out Of Scope

- Rewriting existing curriculum content
- Taxonomy reorg
- Bulk re-ingestion
- Frontend changes
- Relaxing the hard gate to accept placeholder data

