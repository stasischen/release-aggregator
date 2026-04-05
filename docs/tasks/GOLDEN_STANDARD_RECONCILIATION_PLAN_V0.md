# Golden Standard Reconciliation Plan V0

## 1. Overview

This document outlines the plan to reconcile and ingest "Golden Standard" (review assets) and "Surgery" (executable patches) into the unified build and package pipeline.

### The Problem

Currently, the unified build pipeline (`content-pipeline/pipelines/build.py`) ignores reviewed assets. It reconstructs every lesson from `content/core/dialogue/*.json` using the logic-only engine (`KoreanTokenizer`). This means:
- Manual review fixes in `gold_standards/*.jsonl` or `overrides/*.jsonl` are LOST during build.
- Engine fallback errors (e.g. `ko:n:*` swallowing particles) reappear even for "verified" lessons.
- The pipeline lacks a "Locked Lesson" ingestion path that bypasses engine volatility.

---

## 2. Review Asset Inventory (Summary)

Based on an initial scan of `content-ko`, the assets fall into three main categories:

| Category | Typical State | Lessons | Risks |
| :--- | :--- | :--- | :--- |
| **Legacy-Complete** | Gold exists in `content/gold_standards`, but `runs/` only has `attest/ack`. | A2-01 ~ A2-25 | `surgery_*.json` working files are missing from git (local-only by SOP). Need to "dump" gold back to surgery if re-review is needed. |
| **In-Transition** | `runs/` has `surgery` and `attest`, but no `gold` file in `runs`. | B1-01 | `apply` has not been completed or results were moved without cleanup. |
| **Complete-New-Flow** | `runs/` has everything: `preflight_ack`, `draft/gold`, `surgery`, `attest`. | C1-01, etc. | High fidelity, but still not ingested by the main pipeline. |

> [!NOTE]
> See `REVIEW_ARTIFACT_INVENTORY_V0.md` for a detailed per-lesson inventory.

---

## 3. Current Flow Breakdown (The Gap)

The current pipeline follows this path:

1. **Source**: `content/core/dialogue/*.json` (Raw text + speaker tags)
2. **Engine**: `KoreanTokenizer` (Regex + Rules + Logic)
3. **Output**: `dist_unified/staging/*.json` (Combined Core/I18N with Tokens)

### The Breakdown Point

In `content-pipeline/pipelines/build.py` (Line 99):

```python
tokens = engine.tokenize(clean_text)
```

There is **no check** for any of the following:

- `content/overrides/<LESSON>.jsonl`
- `content/gold_standards/dialogue/<LEVEL>/<LESSON>.jsonl`

The review/golden path is a **parallel track** that never merges back into the build track.

---

## 4. Definition of Roles

To resolve the confusion between assets, we redefine their responsibilities:

| Asset | Role | Status in Build |
| :--- | :--- | :--- |
| **Golden Sample** (`.jsonl`) | **Source Truth**. Represents the full lesson state (surface + canonical atoms). | Should be the **primary input** for "Locked" lessons. |
| **Surgery** (`.json`) | **Executable Patch**. A simplified edit-view for manual intervention. | Should be used to **materialize** overrides into the Golden Sample. |
| **Attest** (`.json`) | **Audit Record**. Signed witness of a human full-pass review. | Should be a **QA Gate** requirement for any lesson marked as "Verified". |

---

## 5. Integration Options

We propose two main routes for integration:

### Route A: Override Ingestion (Preferred for Incremental Migration)

The build pipeline remains engine-first, but looks for an override map.

1. **Action**: Update `build.py` to check `content/overrides/<LESSON>.jsonl`.
2. **Logic**: If an override exists for a `(line_id, eojeol_index)`, use the override's atoms instead of the engine's.
3. **Pros**:
   - Engine still handles the "long tail" of unreviewed lessons.
   - Minimal impact on performance.
   - Overlays naturally with `engine` logic.
4. **Cons**: Requires a "finalize" step to extract overrides from Golden Samples.

### Route B: Dual-Ingestion (Strict Locked Mode)

The build pipeline treats reviewed lessons as distinct from draft lessons.

1. **Action**: If `gold_standards/<LEVEL>/<LESSON>.jsonl` exists, build **directly** from it, bypassing the engine and even the raw `core/dialogue/*.json`.
2. **Pros**: 100% fidelity to what was reviewed. Zero engine volatility.
3. **Cons**: High friction if the source `core/dialogue/*.json` changes (out-of-sync risk). Requires a strict "re-draft" workflow.

---

## 6. Recommended Direction: **Hybrid Plan B with Regression Gate**

We recommend future formal flow as **Engine-first with Override/Golden overrides + Mandatory Regression Gate**.

1. **Ingestion**: `build.py` should ingest `content/overrides/*.jsonl`.
2. **Finalization**: Every review run MUST end with `scripts/ops/finalize_lesson_review.py` which pushes the overrides to `content/overrides/`.
3. **Verification**: `qa_gate.py` should verify that for any lesson with `attest`, the built output matches the `Gold Sample`.

---

## 7. First Recovery Plan (Phase 1)

Focus on `A2-01` and the A2 block, as it has the most "Legacy-Complete" but "Disconnected" assets.

### Target 1: A2-01 (Recovery of Working State)

- **Current State**: Has `A2-01.jsonl` in `gold_standards`. Has `attest` in `runs/A2-01`. Missing `surgery_A2-01.json` in git.
- **Action**: Use `04_gsd_surgeon.py dump` to restore `surgery_A2-01.json` from the gold standard.
- **Validation**: Run `finalize_lesson_review.py` to materialize `content/overrides/A2-01.jsonl`.
- **Verification**: Ensure `build.py` (once updated) picks up these overrides.

### Target 2: B1-01 (Completion)

- **Current State**: Has `surgery_B1-01.json` and `attest`. Missing `gold` in `runs/`.
- **Action**: Run `orchestrator.py apply --lesson B1-01` to generate the gold sample.
- **Action**: Promote result to `content/gold_standards/dialogue/B1/`.
- **Action**: Run `finalize` to create overrides.

### Target 3: C1-01 (Standardization)

- **Action**: Run `finalize` on existing `runs/C1-01` assets to ensure it follows the "Override Ingestion" pattern.

---

## 9. Re-reviewing the Splitting Process (Engine Refinement)

The user has explicitly requested to **re-review the splitting (segmentation) workflow** using the existing Golden Standards. This means transitioning from a purely manual patch-and-forget approach to a **Learning Loop**.

### The Learning Loop Workflow

1. **Audit**: Match `gold_standards/*.jsonl` against the current `KoreanTokenizer`.
2. **Identification**: Identify where the engine's high-confidence rules (e.g. `std_pron_ne_poss`) disagree with human-verified gold.
3. **Adjustment**:
   - If the Gold is correct: Update `engine/rules/rules.json` or `dictionary.json` to handle the case better, or add a specific entry to `surgery_heuristics.json`.
   - If the Engine is correct (newer/better): Update the legacy Gold file (using `remediate_gold.py`).
4. **Generalization**: Apply the new rules to the next level of content (B1/B2) to reduce "Surgery Fatigue".

### Action: "Re-drafting from Gold"

We will implement a new `orchestrator.py` mode: `python scripts/review/orchestrator.py re-review --lesson <ID>`.
-   **Old Flow**: `Raw -> Engine -> Surgery (Manual)`.
-   **Gold Flow**: `Gold -> Engine Comparison -> Discrepancy Surgery`.
-   **Benefit**: Human reviewers only look at what the engine *changed* vs the previous gold standard, rather than starting from scratch.

---

## 10. Summary of immediate implementation

| Priority | Task | Target Dir | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | Build Ingestion | `content-pipeline/` | Update `build.py` to ingest `content/gold_standards/*.jsonl`. | **DONE** |
| **P1** | Materialization | `content-ko/scripts/` | Run `finalize_lesson_review.py` for A2-01 ~ A2-25. | **Active** |
| **P2** | Audit & Adjust | `content-ko/engine/` | Compare gold vs engine for A2, adjust `rules.json` to respect common `gold` patterns. | **Proposed** |
| **P3** | Recovery | `content-ko/data/` | Dump `A2-01.jsonl` back to `surgery_A2-01.json` for manual fine-tuning if needed. | **Proposed** |
