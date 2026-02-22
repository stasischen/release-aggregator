# TASK: KO Rules Engine Heuristic Integration

## Context

In the A2 V5 Audit phase, we developed `fix_surgery.py` to automate common atomic corrections (e.g., past tense decomposition, counter normalization, proper noun tagging). Currently, these rules only run as a post-processing step for manual surgery. Integrating them into the core mapping engine will significantly reduce manual labor for future lessons (B1, B2).

## Objectives

1. **Analyze `fix_surgery.py` Rules**: Categorize existing rules (Broad Mappings vs. Surface Heuristics).
2. **Design Engine Plug-in**: Research how to inject these heuristics into `rules_engine.py` without breaking existing rule-based logic.
3. **Handle Ambiguity**: Move the "Audit Warning" logic from `fix_surgery.py` to the pipeline report to alert reviewers of high-risk automatic mappings.
4. **Validation**: Ensure that any engine-level changes maintain 100% reconstruction pass rates for historical A1/A2 gold standards.

## Sub-tasks

- [ ] **Heuristic Extraction**: Document current 100+ rules from `fix_surgery.py`. (Assigned: Agent)
- [ ] **Engine Architecture Review**: Analyze `RulesEngine.resolve()` for extension points.
- [ ] **Pilot Implementation**: Migrate high-confidence broad mappings (e.g., `ko:n:안` -> `ko:adv:안`) to the engine dictionary or a new "pre-resolve" hook.
- [ ] **Verification**: Run `ko_data_pipeline.py` on all A1/A2 lessons to check for regressions.

## Expected Outcome

- Reduced lines in `surgery_XX.json` files for new lessons.
- Automated handling of 80%+ common V5 standardization patterns.
- Robust warning system for ambiguous polysemous words (e.g., "네").
