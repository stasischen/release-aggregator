# Golden Standard Reconciliation Plan V0 (Legacy)

> [!NOTE]
> This document has been superseded by [GOLDEN_REVIEW_INTEGRATION_PLAN_V1.md](GOLDEN_REVIEW_INTEGRATION_PLAN_V1.md). 
> Please refer to the V1 plan for the formal integration contract and recovery strategy.

## 1. Overview

This document outlines the plan to reconcile and ingest "Golden Standard" (review assets) and "Surgery" (executable patches) into the unified build and package pipeline.

### The Problem (Historical Note)

Previously, the unified build pipeline (`content-pipeline/pipelines/build.py`) ignored reviewed assets. It reconstructed every lesson from `content/core/dialogue/*.json` using the logic-only engine (`KoreanTokenizer`). 

**Update**: As of Phase 1, `build.py` now supports basic `gold_standards` ingestion, resolving the primary disconnection.

---

## 2. Review Asset Inventory (Summary)

Based on an initial scan of `content-ko`, the assets fall into three main categories:

| Category | Typical State | Lessons | Risks |
| :--- | :--- | :--- | :--- |
| **Legacy-Complete** | Gold exists in `content/gold_standards`, but `runs/` only has `attest/ack`. | A2-01 ~ A2-25 | `surgery_*.json` working files are missing from git (local-only by SOP). Need to "dump" gold back to surgery if re-review is needed. |
| **In-Transition** | `runs/` has `surgery` and `attest`, but no `gold` file in `runs`. | B1-01 | `apply` has not been completed or results were moved without cleanup. |
| **Complete-New-Flow** | `runs/` has everything: `preflight_ack`, `draft/gold`, `surgery`, `attest`. | C1-01, etc. | High fidelity, but still not ingested by the main pipeline. |

> [!NOTE]
> See [REVIEW_ARTIFACT_INVENTORY_V0.md](REVIEW_ARTIFACT_INVENTORY_V0.md) for a detailed per-lesson inventory.

---

## 3. Implementation History

### P0: Build Ingestion (Active)

Update `build.py` to ingest `content/gold_standards/*.jsonl`. This is currently in Phase 1 (Best-effort line-level fallback).

---

## 4. Summary of Task Status

| Priority | Task | Target Dir | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | Build Ingestion | `content-pipeline/` | Update `build.py` to ingest `content/gold_standards/*.jsonl`. | **DONE** |
| **P1** | Materialization | `content-ko/scripts/` | Run `finalize_lesson_review.py` for A2-01 ~ A2-25. | **Active** |
| **P2** | Audit & Adjust | `content-ko/engine/` | Compare gold vs engine for A2, adjust `rules.json` to respect common `gold` patterns. | **Proposed** |
| **P3** | Recovery | `content-ko/data/` | Dump `A2-01.jsonl` back to `surgery_A2-01.json` for manual fine-tuning if needed. | **Proposed** |
