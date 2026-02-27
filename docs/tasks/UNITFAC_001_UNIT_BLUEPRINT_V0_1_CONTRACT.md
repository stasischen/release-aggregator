# UNITFAC-001: Unit Blueprint v0.1 Contract Freeze

| Field | Value |
| :--- | :--- |
| **Contract Name** | Unit Blueprint Protocol |
| **Version** | `v0.1` |
| **Status** | **FROZEN** |
| **Effective Date** | 2026-02-27 |
| **Target Audience** | AI Content Agents, Human Authors, Frontend Adapters |

---

## 1. Overview

The `unit_blueprint_v0.1` contract represents the transition from "Technical Mockups" to "Production-Ready Pilots." It formalizes the educational requirements discovered during the development of Pilot Unit `A1-U05`.

**Key Goal**: Ensure every unit contains a complete educational loop (Input -> Check -> Structure -> Output -> Review) with explicit metadata for retrieval and spacing.

---

## 2. Structural Extensions (Superset of v0)

`v0.1` is a backward-compatible extension of `v0`. All `v0` fields remain valid, but the following are now **mandatory for Production-Ready (PR) status**.

### 2.1 Global Metadata

- `unit.learning_objective_type`: Defining the focus of the unit.
  - Allowed: `survival_functional`, `vocabulary_expansion`, `grammar_foundation`, `social_interaction`.
- `unit.difficulty_scaffold_level`: (Integer 1-5) 1 = High help/hints, 5 = Independent production.

### 2.2 Node-Level Additions

- **Comprehension Check**: `content_form: comprehension_check` is now a standard form.
- **Review Metadata**: `review_card` nodes MUST include `retrieval_target` in the payload.
  - `form`: Focus on spelling/structure.
  - `function`: Focus on context/meaning.
  - `mixed`: Both.
- **Improved Output Modes**:
  - `pattern_transform`: Explicitly for switching variables within a sentence frame.
  - `repair_practice`: Focused on communication failure recovery (e.g., "Wait," "Slow down").

### 2.3 Followup Extensions

- `scheduled_followups[].transfer_pattern_refs`: An array of strings referencing the key patterns (e.g., `["주세요", "-(으)세요"]`) to be reinforced in future units.

---

## 3. Mandatory PR Skeleton (The "Zero-Tolerance" List)

Units frozen under `v0.1` must meet the following minimum node set (as defined in `UNITFAC-002`):

1. **Immersion Input (2+)**: Must include 1 Dialogue + 1 Non-Dialogue (Message/Notice).
2. **Comprehension Check (1)**: Must immediately follow the first Input node.
3. **Structure Pattern (2+)**: 1 Dictionary Pack + 1 Pattern Card.
4. **Controlled Output (2+)**: 1 Chunk Assembly + 1 Response Builder.
5. **Productive Output (2)**: 1 Speaking Prompt + 1 Writing Prompt.
6. **Review Retrieval (1)**: Final node with `retrieval_target`.
7. **Followups (2+)**: Explicitly scheduled at `+1` and `+3` units.

---

## 4. Backward-Safe Migration Rules

To transition from `v0` (Legacy) to `v0.1` (PR):

1. **Rule 1: Soft Migration**: `mockup-check` will allow `version: unit_blueprint_v0` but will flag it with a **LINT_LEGACY_VERSION** warning.
2. **Rule 2: Promotion Path**:
   - Change `version` string to `unit_blueprint_v0.1`.
   - Add missing metadata fields (`learning_objective_type`, `retrieval_target`).
   - Fill in `transfer_pattern_refs` for all followups.
3. **Rule 3: Field Preservation**: Renderers MUST NOT break if an optional sub-metadata field is missing; they should fallback to `v0` default display.
4. **Rule 4: Mandatory Translation**: All strings in `v0.1` MUST have `zh_tw` counterparts. Partial translation is no longer permitted for PR units.

---

## 5. Prohibited Breaking Changes

The following changes are **strictly prohibited** in the `v0.x` branch to avoid breaking the renderer:

- Renaming existing top-level keys (`unit`, `sequence`, `payload`).
- Changing the `unit_id` format (e.g., changing `A1-U04` to `U04_A1`).
- Modifying the internal structure of `dialogue_turns` or `chunk_assembly` tasks.

---

## 6. Pilot Confirmation

This contract is frozen based on the successful implementation and validation of:
- `docs/tasks/mockups/a1_u05_unit_blueprint_v0.json` (to be updated to v0.1)
- `scripts/mockup_check.py` (v0.1 lint rules integrated)
