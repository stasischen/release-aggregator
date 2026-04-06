# Implementation Plan - Knowledge Lab Batch 001 Review

Review the completed Wave 1 Batch 001 migration (37 items) for content quality, schema compliance, and status synchronization.

## User Review Required

> [!IMPORTANT]
> The review will focus on the following 37 claimed items: 15 Grammar, 12 Connectors, and 10 Patterns.
> I will verify the state at commits `content-ko`: `5be2e2de` and `release-aggregator`: `0503b2f`.

## Proposed Review Steps

### 1. Content Quality Sampling (6-10 items)
I will inspect 3-5 items from each category for:
- OCR artifacts (e.g., weird characters from scanning).
- Mixed-script errors (e.g., English/Chinese accidentally mixed into Korean strings).
- Forbidden internal fields (e.g., `media_id`, `source_ref` if not allowed).

**Target Samples:**
- **Grammar (15 total):**
    - `kg.grammar.particle.subject.json`
    - `kg.grammar.particle.topic.json`
    - `kg.grammar.particle.object.json`
- **Connectors (12 total):**
    - `kc.connector.clausal.reason_because.json`
    - `kc.connector.clausal.sequential_and.json`
- **Patterns (10 total):**
    - `kp.pattern.question.asking_name.json`
    - `kp.pattern.social_basic.self_intro_name.json`

### 2. Schema & Contract Check
- [ ] Run `grep` or `rg` across all 37 changed items to ensure no `media_id` or other unauthorized fields exist.
- [ ] Verify `id` field matches filename.

### 3. Aggregator Task Sync
- [ ] Update `release-aggregator/docs/tasks/TASK_INDEX.md` progress for `KNOWLEDGE_LAB_ENRICHMENT`.
- [ ] Update `release-aggregator/docs/tasks/KNOWLEDGE_LAB_ENRICHMENT_TASKS.json` to mark `KLAB-003` as `done`.

### 4. Final Findings Report
- [ ] Generate the report following the `knowledge-lab-review` skill format.

## Open Questions
- None.

## Verification Plan

### Automated Checks
- `rg -i "media_id" content/core/learning_library/knowledge/`
- `rg -i "TODO" content/i18n/zh_tw/learning_library/knowledge/`

### Manual Verification
- Visual check of the JSON structure of samples.
