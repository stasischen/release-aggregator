# Cross-Language Review/Lock Pipeline Plan

**Date**: 2026-02-16  
**Owner**: release-aggregator  
**Scope**: KO first (`A1/A2/B1`), then reusable for other languages.

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

## 3. Directory Contract

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

## 4. Data Model (Universal)

### 4.1 surface_candidates

Required fields:
- `lang`
- `surface`
- `candidate_atom_id`
- `candidate_signature`
- `sources` (`rule` / `dictionary` / `override`)
- `rule_ids`
- `occurrence_count`
- `max_confidence`
- `sample_source_refs`
- `reconstruct_ok`

### 4.2 surface_locks

Required fields:
- `lang`
- `surface`
- `final_atom_id`
- `candidate_signature`
- `lock_scope` (`global` / `context`)
- `context_signature` (nullable for global)
- `status` (`locked` / `stale`)
- `decision_source` (`manual` / `auto-promoted`)
- `approved_by`
- `approved_at`
- `note`

### 4.3 surface_review_queue

Required fields:
- `lang`
- `surface`
- `candidate_atom_ids`
- `candidate_signature`
- `reason` (`new_surface` / `signature_changed` / `collision` / `stale_lock`)
- `priority`
- `sample_source_refs`

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

4. Branch policy:
- One review batch per branch (e.g., `codex/ko-locks-a1-a2-b1-r1`)
- PR gate runs queue/lock integrity checks.

## 7. Gates (Language-agnostic)

Hard gates:
- `coverage_locked_rate == 1.0` (for in-scope levels)
- `unresolved_surface_count == 0`
- `collision_unresolved_count == 0`
- `reconstruction_pass_rate == 1.0`
- `stale_lock_count == 0`

Soft metrics:
- `new_surface_count`
- `auto_reuse_rate`
- `manual_review_delta`

## 8. KO Rollout Plan (A1/A2/B1)

Phase R1 (Foundations)
- Freeze schemas and directories.
- Move existing manual locks into canonical `surface_locks.jsonl`.

Phase R2 (Pipeline integration)
- Write candidates/queue/effective resolution into runtime.
- Apply locks + line overrides to produce accepted/conflicts.

Phase R3 (Collaboration tooling)
- Add claim checker + compile_locks command.
- Add stale lock detector based on candidate signature.

Phase R4 (CI)
- Add hard gates and scoped-level validation (`A1/A2/B1` now, exclude `B2/C1`).

Phase R5 (Cross-language adoption)
- Implement adapter interfaces for TH/DE/JP.
- Reuse same review/lock engine and gate scripts.

## 9. Non-Goals

- Unifying language-specific tokenizer rules.
- Replacing linguistic manual judgment with auto-only mode.

## 10. Acceptance Criteria

1. Re-running pipeline does not erase manual locks.
2. Previously approved stable surfaces are auto-reused.
3. Only new/changed surfaces enter review queue.
4. Same process can run on another machine with deterministic output.
5. Same review/lock core can be reused by another language repo without changing lock schemas.
