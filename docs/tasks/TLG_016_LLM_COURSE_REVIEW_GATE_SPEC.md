# TLG-016 — LLM Course Reasonability Review Gate Spec

## 1. Goal
Add an LLM-based review layer to TLG-006 so unusable course drafts are blocked before frontend preview.

## 2. Scope
- Input: `unit_blueprint_v1`
- Output: `tlg006_llm_review_report_v1`
- Gate mode: `blocker-first`

## 3. Review Dimensions (1-5)
Required score keys:
- `theme_coherence`: does the whole unit stay in one task theme/storyline
- `node_payload_alignment`: node title/summary vs payload task consistency
- `progression_logic`: does L1->R1 progression make pedagogical sense
- `task_authenticity`: are tasks usable in real communication
- `redundancy_control`: avoids repetitive/duplicated node content

Score meaning:
- 1 = broken/unusable
- 2 = major issues
- 3 = borderline
- 4 = good
- 5 = strong

## 4. Required Review Output
See schema:
- `docs/tasks/schemas/tlg006_llm_review_report_v1.schema.json`

Mandatory sections:
- `overall_decision` (`pass`/`revise`/`fail`)
- `scores`
- `blocking_findings`
- `node_reviews` (must cover every node id)
- `summary_zh_tw`

## 5. Gate Rules
`ERR_LLM_REVIEW_DECISION_FAIL` (blocker):
- `overall_decision` is `fail`

`ERR_LLM_REVIEW_SCORE_TOO_LOW` (blocker):
- any dimension score `< 4`

`ERR_LLM_REVIEW_BLOCKING_FINDING` (blocker):
- any finding with severity `blocker`

`ERR_LLM_REVIEW_NODE_COVERAGE_MISSING` (blocker):
- missing node review for any node in blueprint

`WARN_LLM_REVIEW_NODE_NEEDS_REVISION`:
- node verdict is `needs_revision` but no blocker triggered

## 6. Integration
Recommended sequence:
1. `tlg005_generate_unit_v1.py`
2. `tlg006_validate_unit_v1.py` (structural gate)
3. LLM review generation (external LLM / agent)
4. `tlg006_llm_review_gate.py` (reasonability gate)
5. adapter + viewer

## 7. Acceptance Commands
```bash
python scripts/tlg006_llm_review_gate.py \
  --blueprint staging/demo_A1-U01.unit_blueprint_v1.json \
  --report staging/demo_A1-U01.llm_review_report.json
```
