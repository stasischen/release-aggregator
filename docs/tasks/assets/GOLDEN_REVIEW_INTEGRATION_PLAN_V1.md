# Golden Review Integration Plan V1

This document formalizes the `golden / surgery / attest` integration for the Lingo content pipeline. It defines roles, build priorities, mismatch policies, and recovery strategies to ensure manual review efforts are preserved and institutionalized.

## 1. Roles & Priority Contract

| Asset | Source Path | Role | Build Priority |
| :--- | :--- | :--- | :--- |
| **Golden Sample** | `content/gold_standards/**/*.jsonl` | **Truth** | **1 (Highest)** |
| **Surgery** | `data/reviews/runs/**/surgery_*.json` | **Executable Patch** | N/A (Internal) |
| **Attest** | `data/reviews/runs/**/attest.json` | **Audit Record** | Gate Requirement |
| Engine Rules | `engine/rules/*.json` | **System Rules** | **2 (Fallback)** |

### Priority Contract (Phased)

#### Phase 1 (Current)

1. **Best-effort Ingestion**: If a Golden Sample exists, `build.py` attempts to ingest it.
2. **Line-level Fallback**: If a line-level sync fails (mismatch or missing gold), the build silently falls back to the engine for that line.
3. **Audit**: `is_gold: true` marks ingested tokens, but no hard gate exists for `is_verified`.

#### Phase 2 (Target)

1. **Gold-Mandatory**: For lessons marked as "Verified", ingestion is mandatory. The engine is bypassed.
2. **Hard Mismatch Gate**: Lexical drift between source and gold MUST trigger a build failure.
3. **Attestation Requirement**: `is_verified: true` in the output manifest REQUIRES the presence of a valid `attest.json`.

---

## 2. Unified Build Integration Contract

### Ingestion Logic (`build.py`)

- **Loose Sync**: Handles minor formatting/punctuation differences between source text and gold surface.
- **Traceability**: Injected tokens must carry:
  - `is_gold: true`
  - `source_of_decision: "GOLDEN_SAMPLE"`
  - `rule_id`: Original rule ID if preserved, or `"gold_ingest"`.

### Integrity Gate
- `integrity_gate.py` must check for `attest.json` presence for any lesson claiming "Verified" status.

---

## 3. Mismatch Policy (Source vs. Gold)

| Drift Type | Built Output | Action |
| :--- | :--- | :--- |
| **Formatting** (Spaces/Punctuation) | **Warning** | Build continues with auto-alignment. |
| **Lexical** (Word mismatch) | **FAIL** | Stop build. Requires `re-draft` or `surgery`. |
| **Structural** (Line ID/Atom missing) | **FAIL** | Stop build. High risk of data corruption. |

---

## 4. Legacy Recovery Strategy

| Category | Typical State | Action |
| :--- | :--- | :--- |
| **Legacy-Complete** | Has Gold, missing Surgery. | `04_gsd_surgeon.py dump` gold to surgery. |
| **In-Transition** | Has Surgery, missing Gold. | `orchestrator.py apply` to finalize gold. |
| **Complete-New-Flow** | Has everything. | Validate and Ingest. |

### Recovery Pack #1 (First Implementation)

1. `A2-01`: Recover surgery from gold; test build ingestion.
2. `A2-06`: Resolve path leakage (A2-21~25 data in A2-06 folder).
3. `B1-01`: Finalize and promote to gold.
4. `C1-01`: End-to-end verification.

---

## 5. Engine Learning Loop

The gap between `Engine` and `Gold` should decrease over time.

1. **Analysis**: Use `analyze_gold_vs_engine.py` to identify high-incidence discrepancies.
2. **Promotion**: If a discrepancy occurs >10 times, promote the fix to `engine/rules/rules.json`.
3. **Cleanup**: Re-run `remediate_gold.py` to sync gold with improved engine logic where applicable.

---

## 6. Implementation Task Plan

See [GOLDEN_REVIEW_INTEGRATION_TASKS.json](GOLDEN_REVIEW_INTEGRATION_TASKS.json) for the executable list.
Phase 1 focuses on documentation and the primary recovery pack.
