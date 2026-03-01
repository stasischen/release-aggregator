# TLG-015 — Hybrid Unit Generation (Script Skeleton + LLM Semantics + Gate)

## 1. Objective
Prevent low-quality, repetitive unit output by separating:
- deterministic structure generation (`script-first`)
- semantic content generation (`LLM-first`)
- contract and coherence enforcement (`gate-first`)

## 2. Three-Stage Pipeline
1. Stage A — Script Skeleton
- Build fixed 13-node sequence (`L1,L2,L3,D1,G1,G2,P1,P2,P3,P4,P5,P6,R1`).
- Fill immutable contract fields: `node_id`, `learning_role`, `content_form`, `output_mode`, rubric skeleton.

2. Stage B — LLM Semantics
- Generate node-level semantics constrained by `unit_intent` and `pattern_meta`.
- Each node must output:
  - `title_zh_tw`
  - `summary_zh_tw`
  - `expected_output_zh_tw`
  - `payload.node_contract` (`node_goal_zh_tw`, `input_from_prev`, `output_to_next`)

3. Stage C — TLG-006 Gate
- Block on coherence/contract failures.
- Retry only failed nodes, not full unit regeneration.

## 3. Unit Intent Contract (New Upstream Requirement)
`tlg005_generator_input_v1` should include:

```json
{
  "unit_intent": {
    "theme_zh_tw": "校園報到與自我介紹",
    "scenario": "new_student_orientation",
    "primary_outcome": "完成初次見面與問路",
    "guardrails": [
      "keep spoken polite register",
      "avoid off-theme shopping content"
    ]
  }
}
```

## 4. Quality Gates (Minimum)
Blockers:
- `ERR_UNIT_THEME_DRIFT`
- `ERR_NODE_PURPOSE_MISSING`
- `ERR_CAN_DO_UNCOVERED`
- `ERR_DUPLICATE_SUMMARY_CLUSTER`

Warnings:
- `WARN_PATTERN_NOTE_LEAKAGE`
- `WARN_CONTEXT_JUMP`

## 5. Implementation Notes (v1)
- `scripts/tlg005_generate_unit_v1.py` now emits node-level copy and `payload.node_contract`.
- `scripts/tlg005_adapt_for_modular_viewer.py` converts `unit_blueprint_v1` into modular viewer fixture without leaking pattern notes as repeated node copy.

## 6. Acceptance Commands
```bash
python scripts/tlg005_generate_unit_v1.py \
  --input staging/tlg005_input.a1_u01.json \
  --pattern-library docs/tasks/pattern_library/ko_survival_pattern_library_v1.json \
  --output staging/demo_A1-U01.unit_blueprint_v1.json

python scripts/tlg006_validate_unit_v1.py \
  --blueprint staging/demo_A1-U01.unit_blueprint_v1.json \
  --repair-registry docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json

python scripts/tlg005_adapt_for_modular_viewer.py \
  --input staging/demo_A1-U01.unit_blueprint_v1.json \
  --output docs/tasks/mockups/modular/data/units/a1_u01_unit_blueprint_v1_preview.json \
  --title-zh-tw "A1-U01 v1 Preview（Node Contract）" \
  --theme-zh-tw "校園報到與自我介紹"
```
