# TLG-018 — Pedagogy Constraints & Gate Policy (Production Quality)

## Goal
Ensure generated units are teachable, coherent, and instructionally aligned, not just schema-valid.

## New Blocker Rules (TLG-006)
1. `ERR_OBJECTIVE_TASK_TYPE_MISMATCH`
- Trigger:
  - comprehension node uses production-style goal, or
  - production node uses pure comprehension-style goal
- Why:
  - learning objective and task type are misaligned.

2. `ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH`
- Trigger:
  - mixed payload styles in same task item (for example `choices` + `response_choices_ko`),
  - missing canonical required fields for that node form,
  - L2 missing anchor metadata.
- Why:
  - downstream renderer/checker ambiguity and teaching intent drift.

3. `ERR_LOGIC_PRECONDITION_FAIL`
- Trigger:
  - L2 `source_anchor_line` does not exist in L1 content.
- Why:
  - comprehension question cannot be solved from provided input.

4. `ERR_SCRIPT_CONTAMINATION`
- Trigger:
  - for `target_lang=ko`, a Korean content field contains mixed Hangul + CJK ideographs.
- Why:
  - target-language contamination degrades trust and learning quality.

5. `ERR_REGISTER_GENRE_MISMATCH_BY_ROLE`
- Trigger:
  - `review_card` with `notice/article` genre constraints,
  - dialogue-role nodes with non-dialogue genre.
- Why:
  - role-specific pedagogy and style contract is violated.

## Required Anchor Policy
- L2 must include:
  - `source_anchor_node_id` pointing to L1
  - `source_anchor_line` traceable in L1 dialogue
- Any non-anchored comprehension item is not production-ready.

## Node Purpose Contract Policy
Every node should keep:
- `payload.node_contract.node_goal_zh_tw`
- `payload.node_contract.input_from_prev`
- `payload.node_contract.output_to_next`

Gate alignment uses this contract as first-class source of truth.

## Acceptance Command
```bash
python scripts/tlg006_validate_unit_v1.py \
  --blueprint <unit_blueprint_v1.json> \
  --repair-registry docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json
```

## Rollout
- Phase 1: enable as blocker for KO A1/A2 generation.
- Phase 2: extend script contamination logic by target language profile.
