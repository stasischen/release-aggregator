# PRG-006: Verification and Rollback Rules (Release Gating)

This document formalizes the validation and rollback criteria established during the `PRG-005` Pilot. It serves as the authoritative guide for determining if a production release is safe and how to revert if a failure is detected.

---

## 1. Pilot Scope Recap

The current validated scope is limited to **exactly-matched video lessons**.

- **Approved Units**: `bonus_video`
- **Approved Lessons**:
  - `ko_v1_vlog_IGEj-oDKyw8_conv_store`
  - `ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson`
- **Strict Logic**: Only items explicitly listed in the `release_manifest` (allowlist) are eligible for production.

> [!WARNING]
> **No Cross-Lesson Shims**: This pilot does NOT support mapping a source (e.g. `A1-01.json`) to a differently named lesson (e.g. `ko_l1_dialogue_a1_01`) unless it is explicitly defined in the manifest.

---

## 2. Verification Criteria

### **Pass/Fail conditions**

#### **Strict Mode (Production Build)**

- **Criteria**: Must have **0 Gaps**.
- **Result**: If `gap_count > 0`, the build MUST fail. No production artifacts are committed.
- **Usage**: Mandatory for all final CI/CD production releases.

#### **Planning Mode (Analysis)**

- **Criteria**: Report all gaps in `production_plan.json`.
- **Result**: Always "passes" technically to show the impact of the current allowlist vs candidate source.
- **Usage**: Used by developers to debug mapping issues or to identify missing content in staging.

### **Gap Classification**

| Gap Reason | Severity | Definition | Action Required |
| :--- | :--- | :--- | :--- |
| `missing_candidate` | **Fatal** | Lesson in manifest not found in staging. | Ingest lesson into staging first. |
| `asset_path_mismatch` | **Fatal** | Staging path differs from manifest's `asset_path`. | Update manifest or fix staging structure. |
| `content_type_mismatch` | **Fatal** | Manifest type (e.g. `dialogue`) differs from staging type. | Fix manifest or staging metadata. |
| `disk_missing` | **Fatal** | Candidate exists in inventory but file is missing on disk. | Re-run staging pipeline / check workspace. |
| `unresolved_unit_id` | **Fatal** | Lesson belongs to `__unassigned__` unit. | Assign lesson to a valid unit in the manifest. |

---

## 3. Rollback Procedure

> [!IMPORTANT]
> **Revert Target**: Rollback always targets the **previous known-good production bundle / generated artifacts**.

### **Step 1: Identify Failure**

If any of the following occur after a release:
- Frontend crashes due to missing `manifest.json` entries.
- Integrity check failure (checksum mismatch).
- Production assets (`manifest.json`, `lesson_catalog.json`) are empty or corrupted.

### **Step 2: Rollback Actions**

1. **Restore Assets**: Revert `manifest.json` and `lesson_catalog.json` to the version from the previous Git commit or deployment backup.
2. **Restore Bundles**: Revert the entire production content folder (`production/**`) to the previous stable state.

### **Step 3: Post-Mortem**

- Check `production_plan.json` for gaps that were ignored during a non-strict run.
- Verify `release_manifest` for typos or incorrect IDs.

> [!CAUTION]
> **No Manual Edits**: DO NOT manually edit `manifest.json` or `lesson_catalog.json` during a rollback. These are derived artifacts. Reverting the source manifest and re-running the assembler is the only supported way to "fix" a build.

---

## 4. Operational Notes

1. **Source of Truth**: The `prd.release_manifest.json` (or specific allowlist file) is the ONLY source of truth for release decisions.
2. **Derived Artifacts**: `manifest.json` and `lesson_catalog.json` are transient and should be treated as output-only.
3. **Candidate Updates**: If content in staging changes (e.g. name or path), the `release_manifest` MUST be updated BEFORE running the assembler.
4. **Contract Stability**: The assembler maintains a strict contract. If a lesson ID changes, it is treated as a new lesson.
