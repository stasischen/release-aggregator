# TLG-017 — Gemini CLI Auto-Generation Architecture (Multi-Language, Easy->Hard)

## 1. Target
Use Gemini CLI with stable prompts + contracts to auto-produce course units across languages and CEFR levels.

## 2. Production Loop
1. Planner (LLM)
- Input: language profile + level band + functional outcomes
- Output: `tlg005_generator_input_v1` batch

2. Skeleton Compiler (Script)
- `tlg005_generate_unit_v1.py`
- Produces deterministic 13-node scaffold + constraints

3. Semantic Writer (LLM)
- Fill node payloads with language-real content (dialogue/reading/speaking/writing)
- Keep register/genre constraints

4. Structural Gate (Script)
- `tlg006_validate_unit_v1.py`

5. Reasonability Gate (LLM + Script)
- LLM outputs `tlg006_llm_review_report_v1`
- `tlg006_llm_review_gate.py` blocks bad outputs

6. Repair Loop
- Only regenerate failed nodes based on review findings

## 3. Why This Works
- Script controls shape, ordering, and contracts.
- LLM controls language realism and pedagogical naturalness.
- Gate controls quality and rejects unusable units.

## 4. Difficulty Progression
- A1-A2: survival task completion, low discourse load
- B1-B2: discourse management + strategy use
- C1-C2: stance/mediation/pragmatics precision

Progression rule:
- Each next level must keep previous core functions and add new complexity dimensions.

## 5. Gemini Prompt Pack
Use prompt templates in:
- `docs/tasks/prompts/gemini/planner_prompt.md`
- `docs/tasks/prompts/gemini/semantic_writer_prompt.md`
- `docs/tasks/prompts/gemini/reviewer_prompt.md`

Prompt rendering helper:
```bash
python scripts/tlg_gemini_emit_prompts.py \
  --unit-input staging/tlg005_input.a1_u01.json \
  --blueprint staging/demo_A1-U01.unit_blueprint_v1.json \
  --outdir staging/gemini_prompts/A1-U01
```

## 6. Definition of Done
- A batch can run end-to-end with no manual schema patching.
- Failed units return actionable node-level repair hints.
- Viewer-ready fixtures are generated only after both gates pass.
