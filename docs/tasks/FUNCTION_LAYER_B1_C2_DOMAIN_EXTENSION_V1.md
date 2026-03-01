# FUNCTION_LAYER_B1_C2_DOMAIN_EXTENSION_V1

| Field | Value |
| :--- | :--- |
| Extension ID | `function_domain_extension_b1_c2_v1` |
| Status | Draft for B1-C2 pipeline integration |
| Scope | Domain extension only; does not replace A1/A2 survival map |
| Paraphrase Policy | Split into `F-PARAPHRASE-REPAIR` and `F-PARAPHRASE-MEDIATION` to avoid cross-domain duplicate IDs |

## Domain Summary

| Domain | B1-B2 Function IDs | C1-C2 Function IDs |
| :--- | :--- | :--- |
| Information Exchange | F-QUALIFY, F-HEDGED-INFORM, F-COMMITMENT-CALIBRATE | F-EPISTEMIC-CALIBRATE, F-EVIDENTIAL-INFORM, F-COUNTER-STANCE |
| Social Relations | F-EMPATHY, F-COMPLIMENT, F-HESITATION-MANAGE | F-FACE-SAVE, F-SOCIAL-REPAIR, F-RELATIONAL-BOUNDARY |
| Action Management | F-SOFTENED-REQUEST, F-POLITE-REFUSAL, F-CONDITIONAL-PERMISSION | F-NEGOTIATE-TRADEOFF, F-ALIGN-CONSTRAINTS, F-ESCALATE-DEESCALATE |
| Discourse Management | F-TURN-TAKING, F-TOPIC-SHIFT, F-OPENING-CLOSING | F-REGISTERED-SHIFT, F-RHETORICAL-PAUSE, F-FRAME-RECONTEXTUALIZE |
| Opinion and Argument | F-HEDGING, F-PRO-CLAIM, F-CON-CLAIM | F-REFUTE-WITH-EVIDENCE, F-CONCEDE-THEN-PIVOT, F-ABSTRACT-GENERALIZE |
| Planning and Coordination | F-SCHEDULE-COORD, F-PRIORITIZE, F-CONTINGENCY-PLAN | F-STAKEHOLDER-ALIGN, F-DECISION-SYNTHESIZE, F-ACTION-OWNER-ASSIGN |
| Repair and Survival | F-ASK-CLARIFY, F-CHECK-UNDERSTANDING, F-PARAPHRASE-REPAIR | F-SELF-REPAIR, F-META-COMMENT, F-INTERACTION-RECOVERY |
| Mediation | F-PARAPHRASE-MEDIATION, F-SUMMARIZE-FOR-OTHER, F-REGISTER-SIMPLIFY | F-NEUTRALIZE, F-BIAS-FLAG, F-CONFLICT-MEDIATE |
| Pragmatics and Politeness | F-SOFTENING-MODAL, F-SOFTENING-PAST, F-SOFTENING-PHRASE | F-INDIRECT-DISAGREE, F-DIPLOMATIC-DECLINE, F-STATUS-SENSITIVE-ASK |
| Narrative and Reflection | F-PAST-SEQUENCE, F-CAUSE-EFFECT-NARRATE, F-LESSON-LEARNED | F-SELF-CRITIQUE, F-PERSPECTIVE-SHIFT, F-META-REFLECTION |
| Professional and Academic | F-STATUS-REPORT, F-RISK-HIGHLIGHT, F-REQUEST-INPUT | F-CONCEPT-DEFINE, F-THEORETICAL-COMPARE, F-METHODOLOGY-DEFEND |
| Culture and Interpersonal Nuance | F-NORM-CHECK, F-REGISTER-CHECK, F-INTENT-SAFEGUARD | F-CULTURAL-BRIDGE, F-MEANING-NEGOTIATE, F-INTERPRET-NUANCE |

## Integration Notes

1. `level_range` is required on every subdomain for generator-side filtering.
2. Keep function IDs globally unique across domains in this extension file.
3. `F-PARAPHRASE-REPAIR` is consumed by repair flows; `F-PARAPHRASE-MEDIATION` is consumed by mediation flows.
4. For B1+ pattern mapping, bind these function IDs to target-language pattern libraries by level band.
