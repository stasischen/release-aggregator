# SENTENCE_BANK_BATCH_24 Migration Plan

Migration of 50 sentences from the legacy sentence bank to Content V2 inventory.

## Goal
Establish a new atomized batch for sentences `ex.ko.s.001201` through `ex.ko.s.001250`.

## Batch Packet Contract (v1.0)
Following [BATCH_PACKET_SCHEMA.md](file:///e:/Githubs/lingo/content-ko/content_v2/review/BATCH_PACKET_SCHEMA.md), the following contract is established for Batch 24:

```json
{
  "batch_id": "SENTENCE_BANK_BATCH_24",
  "sentence_range": "ex.ko.s.001201-001250",
  "source_scope": "content/core/learning_library/example_sentence/",
  "staging_scope": "content_v2/staging/example_sentence/batch_24_atomized.json",
  "current_gate_state": "init",
  "ledger_ref": "content_v2/review/manual_review_ledger.jsonl",
  "reuse_index_ref": "content_v2/review/manual_review_ledger.index.json",
  "tail_scope": "content_v2/inventory/dictionary/2026-04-30-fix/tail.jsonl",
  "special_in_scope": ["Affix Normalization", "Macro-Atom Collapse", "Polite Endings"],
  "required_outputs": ["content_v2/inventory/example_sentence/batch_24.json"]
}
```

## Machine Status & Claims
- **Canonical Claim Location**: `docs/tasks/machines/local.json` (Local to `content-ko` repo).
- **Global Visibility**: `release-aggregator/docs/tasks/MACHINE_STATUS.md` (Updated in the `release-aggregator` workspace).
- **Machine ID**: `gamer`

## Proposed Changes

### Content KO

#### [NEW] [batch_24_raw.json](file:///e:/Githubs/lingo/content-ko/content_v2/staging/example_sentence/batch_24_raw.json)
- Temporary payload for LLM processing containing IDs and surfaces.

#### [NEW] [batch_24_atomized.json](file:///e:/Githubs/lingo/content-ko/content_v2/staging/example_sentence/batch_24_atomized.json)
- The raw output of the atomization process.

#### [NEW] [batch_24.json](file:///e:/Githubs/lingo/content-ko/content_v2/inventory/example_sentence/batch_24.json)
- The finalized, validated, and promoted batch.

## Workflow (SOP Alignment)

1. **Pull**: Use `scripts/ops/sentence_bank_ingest.py` to extract 50 sentences starting from `ex.ko.s.001201`.
2. **Canonical Reuse Check**: Before atomization, verify if tokens exist in `manual_review_ledger.index.json` or `tail.jsonl` to ensure lane consistency.
3. **Atomize**: Apply `docs/prompts/PROMPT_V2_SENTENCE_ATOMIZATION.md` to generate V2 atoms.
4. **Internal Review**: Validate morphological splits and POS tags against latest policies (Family A/B/C/D).
5. **Lint**: Run `scripts/legacy/v2_msr_linter.py` for normalization.
6. **Coverage Scan**: Run `scripts/ops/check_atom_coverage.py` to identify orphans.
7. **Orphan Triage**: Resolve orphans using [CONTENT_V2_SHARED_ATOMIZATION_LANES.md](file:///e:/Githubs/lingo/content-ko/docs/tech/CONTENT_V2_SHARED_ATOMIZATION_LANES.md).
8. **Promotion**: Move the finalized batch to inventory only after attaining Zero-Orphan status.

## Verification Plan

### Automated Tests
- `python scripts/ops/check_atom_coverage.py --content-path content_v2/staging/example_sentence/batch_24.json`
- `python scripts/legacy/v2_msr_linter.py content_v2/staging/example_sentence/batch_24.json`
