# Cross-Language Review/Lock Pipeline Plan (V1.0 - FROZEN)

**Date**: 2026-02-25  
**Status**: ❄️ Frozen (Contract Locked)  
**Owner**: release-aggregator  

**Scope**: 

- **Active**: KO (`A1`, `A2`, `B1`)
- **Deferred**: KO (`B2`, `C1`)
- **Goal**: Reusable for all languages (TH, DE, JP, etc.)

## 1. Problem

Current mapping outputs are rerunnable artifacts, but manual review decisions can be lost or mixed with runtime outputs. This causes repeated re-review and unstable cross-device collaboration.

## 2. Target Architecture

Separate pipeline into three layers:

1. Language Rules Layer (language-specific)
   - Produces segmentation/mapping candidates only.
   - Per-language rules remain independent.

2. Universal Review/Lock Layer (shared)
   - Uses shared schemas for candidates, review queue, locks, and effective resolution.
   - Same logic for KO/TH/DE/JP/etc.

3. Collaboration Layer (multi-machine)
   - Runtime artifacts are disposable.
   - Human lock data is canonical and versioned in Git.

## 3. Directory Contract (Naming & Layout)

### 3.1 Canonical human-reviewed data (commit to git)

- `content/source/{lang}/review/mapping/surface_locks.jsonl`
- `content/source/{lang}/review/mapping/line_overrides/{lesson}.jsonl`
- `content/source/{lang}/review/mapping/review_events/{reviewer}/{timestamp}.jsonl`
- `content/source/{lang}/review/mapping/review_claims/{reviewer}.json`

### 3.2 Runtime pipeline outputs (do not commit)

- `data/staging/runtime/token_candidates.jsonl`
- `data/staging/runtime/surface_candidates.jsonl`
- `data/staging/runtime/surface_review_queue.jsonl`
- `data/staging/runtime/surface_resolution_effective.jsonl`
- `data/staging/runtime/mapping_accepted.jsonl`
- `data/staging/runtime/mapping_conflicts.jsonl`

### 3.3 Reproducible snapshots (optional commit, usually artifact)

- `data/staging/runs/{run_id}/...`
- `data/staging/runs/latest.json`

## 4. Data Model (Universal Schema)

### 4.1 surface_candidates

Required for all languages to enter the review queue.

- `lang`: Language code (e.g. `ko`)
- `surface`: The raw text surface.
- `candidate_atom_id`: Proposed atom ID from rules/dict.
- `candidate_signature`: Hash of (surface + candidate_atom_id + rule_logic_version).
- `sources`: List of strings (`rule`, `dictionary`, `override`, `suggestion`).
- `rule_ids`: List of rule IDs that triggered this candidate.
- `occurrence_count`: Number of times this surface appears in the batch.
- `sample_source_refs`: List of `lesson:line` examples.

### 4.2 surface_locks

The final source of truth for a surface's mapping.

- `lang`: Language code.
- `surface`: The raw text surface.
- `final_atom_id`: The locked atom ID.
- `candidate_signature`: The signature this lock was based on (used for stale detection).
- `lock_scope`: `global` (everywhere) or `context` (specific phrase/lesson).
- `status`: `locked` or `stale`.
- `decision_source`: `manual` (human) or `auto-promoted` (high confidence bot).
- `approved_by`: Username/AgentID.
- `approved_at`: ISO timestamp.

### 4.3 surface_review_queue

Items requiring human attention.

- `surface`: The surface to review.
- `reason`: `new_surface`, `signature_changed` (stale), `collision` (multiple high-conf candidates).
- `priority`: `P0` (blocker), `P1` (new), `P2` (optimization).

## 5. Reuse Rules (Skip Re-review)

A reviewed surface can be auto-reused only when:

1. `surface` matches
2. `candidate_signature` unchanged
3. `lock_scope` valid for current context

If candidate signature changes, mark old lock as `stale` and push to review queue.

## 6. Multi-Machine Collaboration Model

1. Claim before review:
   - Reviewer writes `review_claims/{reviewer}.json`
   - CI checks no duplicated active claim on same surface set.

2. Review as append-only events:
   - Review writes to reviewer-specific event files.
   - No direct concurrent editing of one shared large lock file.

3. Compile locks deterministically:
   - `compile_locks` merges events => `surface_locks.jsonl`
   - Stable sorting + deterministic conflict policy.

## 7. Gates (Language-agnostic Integrity)

Hard gates (Must be 100% pass for production):

- `coverage_locked_rate == 1.0` (for in-scope levels)
- `unresolved_surface_count == 0`
- `collision_unresolved_count == 0`
- `stale_lock_count == 0`

## 8. KO Rollout Scope (A1/A2/B1)

**Phase R1 (Foundations) - CURRENT STATUS: DONE**

- Freeze schemas and directories.
- Move existing manual locks into canonical `surface_locks.jsonl`.
- **Scope Limit**: Only process `A1`, `A2`, and `B1` levels.
- **Deferral**: `B2` and `C1` levels are excluded from the current locking cycle to prioritize stabilization of the core levels.

## 9. Appendix: Implementation Contract

1. **Naming Convention**: All lock-related files MUST use `.jsonl` (line-delimited JSON) for better git merging and large file handling, except for `review_claims` which is a single `.json`.
2. **Signature Logic**: `candidate_signature` must be deterministic. If a language repo changes its tokenizer version, all signatures must be recalculated, triggering `stale_lock` states in the review queue.
3. **Disposable Runtime**: Any file under `data/staging/runtime/` can be deleted at any time; the pipeline must be able to reconstruct it from `content/source/{lang}/review/` and `Gold Standard` files.
