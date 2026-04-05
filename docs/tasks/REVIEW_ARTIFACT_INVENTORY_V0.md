# Review Artifact Inventory V0

## 1. Summary Metrics

- **Total Lessons Scanned**: 4 (Sampled: A2-01, A2-06, B1-01, C1-01)
- **Repo Status**: Unified Build does NOT ingest any of these assets.
- **Data Fragmentation**: High. Assets are split across `runs/`, `content/gold_standards/`, and `reports/`.

---

## 2. Detailed Inventory (Representative Samples)

| Lesson | Run Dir Assets | Permanent Gold | Status Judgment | Risks |
| :--- | :--- | :--- | :--- | :--- |
| **A2-01** | `ack`, `attest` | `A2-01.jsonl` | **Legacy-Complete** | Working `surgery` file missing. Must re-dump from gold if re-review needed. |
| **A2-06** | `ack`, `attest` | `A2-06.jsonl` | **Legacy-Complete** | `runs/A2-06` folder incorrectly contains `A2-21~25` gold/surgery. Path leakage. |
| **B1-01** | `ack`, `surgery`, `attest` | `B1-01.jsonl` | **In-Transition** | Missing `gold` in `runs/`. Unclear if `apply` was fully finalized. |
| **C1-01** | `ack`, `gold`, `surgery`, `attest` | `C1-01.jsonl` | **Complete-New-Flow** | Ideal state, but still not materialized to `overrides/`. |

---

## 3. Findings & Anomalies

### A. Run Directory Chaos

The folder `data/reviews/runs/A2-06` contains artifacts for `A2-21` to `A2-25`. This indicates that either:

- The `orchestrator.py` was forced to output to a specific run folder.
- Or these lessons were part of a batch "Run 06" and correctly matched their internal lesson IDs.

**Recommendation**: Standardize run folder naming to `runs/<LESSON_ID>` strictly.

### B. Missing Overrides

The `content/overrides/` directory is essentially empty (`audit_report.txt` only).
This is the **missing link** for the automated build pipeline. The `finalize_lesson_review.py` script exists to populate this, but it hasn't been part of the standard SOP execution for legacy lessons.

### C. Surgery SOP Compliance

Per `KO_REVIEW_RUN_ARTIFACT_POLICY.md`, `surgery_*.json` is kept local-only.
This works for privacy/conflict reduction but leaves the repo without "executable edit history".

**Recommendation**: For "Certified" lessons, we should commit the final `overrides/*.jsonl` as the permanent record, even if we don't commit the full working surgery.

---

## 4. Lesson-specific Breakdown (Discovery)

- **A2-01 to A2-25**: All have permanent gold standards. The "reconciliation" here is purely about (1) Ingestion into build and (2) Materialization to overrides.
- **B-Level**: Progressing. `B1-01` is the current bridge.
- **C-Level**: `C1-01` is the pilot for the new flow.
