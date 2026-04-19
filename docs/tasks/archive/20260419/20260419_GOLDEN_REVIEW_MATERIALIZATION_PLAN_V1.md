# Golden Review Materialization Plan V1

This document defines the Phase 3 strategy: **Materialization**, which transitions review outputs from temporary run-specific files into stable, committed assets in the `content/overrides/` directory.

## 1. Override Materialization Contract

The **Materialized Override** is the definitive build-consumable asset for a "Certified" lesson.

| Field | Description | Example |
| :--- | :--- | :--- |
| `line_id` | Dialogue line ID | `L01-D1-01` |
| `eojeol_index` | Token index in line | `0` |
| `surface` | Original surface text | `사람이` |
| `atoms` | List of constituent atoms | `["ko:n:사람", "ko:e:이"]` |
| `final_atom_id` | Concatenated atom ID | `ko:n:사람+ko:e:이` |
| `status` | Record status | `locked` |
| `decision_source` | Source of truth | `manual` |
| `reviewer` | Reviewer identity | `antigravity` |
| `updated_at` | Timestamp | `2026-04-06T...` |

### Storage Location
- **Path**: `content/overrides/<LESSON_ID>.jsonl`
- **Ownership**: Committed to the `content-ko` repository.

## 2. Standardized Artifact Roles

| Asset | Role | Path | Consumed By |
| :--- | :--- | :--- | :--- |
| **Gold Standard** | Linguistic Reference | `gold_standards/dialogue/` | Materializer |
| **Override** | Pipeline Input | **`overrides/`** | **`build.py`** |
| **Surgery** | Working File | `data/reviews/runs/` | Orchestrator |
| **Attest** | Process Evidence | `data/reviews/runs/` | Materializer / Gate |

## 3. Workflow optimization

1.  **Orchestration**: `orchestrator.py apply` -> `finalize_lesson_review.py`.
2.  **Gate Requirement**: `finalize` requires a valid `surgery_full_pass_attest.json`.
3.  **Build Ingestion**: `build.py` priorities: `Overrides` > `Gold Standards` > `Engine Rules`.

## 4. Recovery Pack #1 Targets

- `A2-01`: Standardize and materialize.
- `A2-06`: Resolve path leakage and materialize.
- `B1-01`: Promote and materialize.
