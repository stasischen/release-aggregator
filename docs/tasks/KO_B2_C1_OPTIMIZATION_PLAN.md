# KO B2/C1 Optimization Plan

## Objective
Enhance and finalize the Korean B2 and C1 curriculum in the LLLO repository. This includes character persona updates (C1), tone auditing (B2), translating content to Traditional Chinese, and creating comprehensive grammar guides.

## Scope
- **Target Levels**: Korean B2 (Management Phase) and C1 (Analytical Phase).
- **Deliverables**: 
    - Updated `dialogue.yarn` for C1 (Characters).
    - Tone-verified `dialogue.yarn` for B2 (Formal).
    - 50 new translation CSVs (B2: 25, C1: 25).
    - 50 new grammar guide MDs (B2: 25, C1: 25).
    - Integration with `content-ko` V5 pipeline.

## Implementation Strategy

### Phase 1: Infrastructure & Spec Definition
- **Persona Lifecycle**: Defined in `persona_governance.md`.
    - B2: Manager Kim & Director Lee (Formal tone).
    - C1: Professor Park & Critic Choi (Sophisticated tone).
- **Tracking**: `KO_B2_C1_OPTIMIZATION_TASKS.json`.

### Phase 2: B2 Management Phase Optimization
- **Tone Audit**: Ensure all B2 dialogues use `-(스)ㅂ니다` correctly in business contexts.
- **Production**: Generate `zh-TW` locales and Grammar MDs batch by batch (5 lessons per batch).

### Phase 3: C1 Analytical Phase Optimization
- **Character Overhaul**: Migrate from A1 placeholders (Jisu/Minsu) to C1 personas.
- **Complexity Check**: Ensure vocabulary and sentence structures meet C1 standards (abstract nouns, complex connectors).
- **Production**: Generate `zh-TW` locales and Grammar MDs.

### Phase 4: Pipeline Ingestion
- Move content to `content-ko` for atomic segmentation and V5 tagging.
- Validate via `content-pipeline`.

## Task Index Reference
- Epic: `ko-b2-c1-optimization`
- Plan File: `release-aggregator/docs/tasks/KO_B2_C1_OPTIMIZATION_PLAN.md`
- Tasks File: `release-aggregator/docs/tasks/KO_B2_C1_OPTIMIZATION_TASKS.json`
