# Duplicate Resolution Note - '這裡可以坐嗎？' (sit_here)

This note clarifies the duplicate state of the sentence `여기 앉아도 돼요?` in the `content-ko` example bank and proposes a canonical resolution path.

## Current State

The surface `여기 앉아도 돼요?` exists twice in the `example_sentence` bank under different classification paths:

1.  **Grammar Path**: `ex.ko.grammar.permission.sit_here.v1`
    - **Source**: `youtube_reference`
    - **Refs**: `["kg.grammar.permission.allow"]`
    - **Translation**: "這裡可以坐嗎？"
2.  **Pattern Path**: `ex.ko.pattern.social_basic.sit_here.v1`
    - **Source**: `survival_library`
    - **Refs**: `["kp.pattern.social_basic.permission"]`
    - **Translation**: "可以坐在這裡嗎？"

## Candidate Comparison

| Metric | Grammar Candidate | Pattern Candidate |
| :--- | :--- | :--- |
| **ID** | `ex.ko.grammar.permission.sit_here.v1` | `ex.ko.pattern.social_basic.sit_here.v1` |
| **Surface** | `여기 앉아도 돼요?` | `여기 앉아도 돼요?` |
| **Level** | A2 | A2 |
| **Existing Refs** | Referenced by `kg.grammar.permission.allow` | Not currently referenced by any `example_sentence_refs` |
| **Pedagogical Focus** | Grammar rule application (`~어도 되다`) | Functional survival pattern |

## Recommended Canonical Decision

**Canonical ID**: `ex.ko.grammar.permission.sit_here.v1`

### Rationale
- **Reference Depth**: The grammar ID is already formally linked in the `kg.grammar.permission.allow` Knowledge Item as part of a curated example set.
- **Structural Alignment**: The grammar rule is the fundamental anchor for this specific morphology. The "pattern" usage is a functional subset that can effectively share the same example record.
- **Naming Convention**: `sit_here` is appropriately descriptive for both contexts.

## Follow-up Action Plan

> [!IMPORTANT]
> This plan identifies the necessary steps but should NOT be executed until formal approval.

1.  **Merge Metadata**:
    - Update `ex.ko.grammar.permission.sit_here.v1` (Core) to include both Knowledge Item references in `knowledge_refs`:
      ```json
      "knowledge_refs": [
        "kg.grammar.permission.allow",
        "kp.pattern.social_basic.permission"
      ]
      ```
2.  **ID Consolidation**:
    - Update the Bucket C1 extraction manifest in `release-aggregator` to point to the canonical Grammar ID.
3.  **Cleanup**:
    - [DELETE] `content/core/learning_library/example_sentence/ex.ko.pattern.social_basic.sit_here.v1.json`
    - [DELETE] `content/i18n/zh_tw/learning_library/example_sentence/ex.ko.pattern.social_basic.sit_here.v1.json`

## Risks
- **Broken References**: Any external (non-core) systems relying exclusively on the `pattern` ID will experience a 404. However, a grep search shows no active references to the pattern ID in the `knowledge` directory.

---
```yaml
task_id: kg-mig-010-sit-here-duplicate-resolution-plan
touched_repos: [release-aggregator]
execution_mode: classic_stage
```
