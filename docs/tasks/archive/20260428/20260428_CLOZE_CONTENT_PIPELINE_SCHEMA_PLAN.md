# Implementation Plan - Cloze Content Pipeline Schema

Implement the content-authoring / build-artifact side for `cloze` review cards in the Modular Study architecture.

## User Review Required

> [!IMPORTANT]
> - **Deterministic Generation**: All choices will be frozen at build time. No randomization at runtime.
> - **Artifact Contract**: Cloze nodes in the artifact will contain **fully-formed `ReviewCardPayload`** JSON.
> - **Pipeline Fallback**: If cloze generation fails quality checks, the node will **downgrade to `typing_practice`** instead of being dropped, maintaining lesson structure.

## Proposed Changes

### [core-schema]
#### [NEW] [review_card_payload.schema.json](file:///Users/ywchen/Dev/lingo/core-schema/schemas/review_card_payload.schema.json)
- Define `ReviewCardPayload` structure.
- **Cloze Contract**: Require `choices`, `expectedAnswer`, and `metadata` containing `clozeTarget` (Atom ID), `clozeIndex` (token index), and `sourceSentenceId`.

### [content-pipeline]
#### [NEW] [cloze_generator.py](file:///Users/ywchen/Dev/lingo/content-pipeline/pipelines/cloze_generator.py)
- Implement `ClozeGenerator`.
- **Output Contract**: Emits **fully-formed `ReviewCardPayload`** JSON.
- **Distractor Generation Strategy**:
  - **Rule 1 (Lesson Context)**: Pick tokens with matching POS from current lesson's sentences.
  - **Rule 2 (Global Fallback)**: Pick from top 2000 frequent atoms (POS match).
  - **Rule 3 (Quality Gate & Fallback)**: If fewer than 3 distractors are found after Rule 2, **downgrade the node to `output_mode: typing_practice`** using the same sentence, rather than dropping it entirely. This ensures lesson structure remains stable.
- **Integration**: Inject nodes into `lesson_content.v1.json` with the appropriate `output_mode`.

### [lingo-frontend-web]
#### [MODIFY] [modular_lesson_adapter.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/data/adapters/modular_lesson_adapter.dart)
- **Mapping**: Map `output_mode == 'cloze_practice'` to `contentForm == 'cloze_practice'`.
- **Hard Short-circuit Bypass**: Add an explicit guard at the top of `_enrichPayload`: `if (contentForm == 'cloze_practice') return payload;`. This ensures pre-built frozen payloads are never modified by runtime logic.

#### [NEW] [ulv_cloze_renderer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/ulv/ulv_cloze_renderer.dart)
- Dedicated UI for cloze cards with choice buttons.
- **Semantic Skip Flow**:
  - If a payload is invalid, show a "Skip" button.
  - Action: Call **`onEffort(success: false, errorCode: 'ERR_CLOZE_MALFORMED_SKIP')`** to record the failure, then call **`onComplete(true)`** to advance the lesson. This distinguishes deadlock avoidance from pedagogical success.
- Passive component: emits `onEffort` and `onComplete`.

#### [MODIFY] [modular_node_viewer.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/widgets/modular_node_viewer.dart)
- **Routing**: Route `case 'cloze_practice':` to `UlvClozeRenderer`.

## Verification Plan

### Automated Tests
- `python -m pytest tests/test_cloze_generation.py`: Verify Rule 3 (fallback to typing_practice) and provenance metadata.
- `flutter test`: Verify hard short-circuit in `ModularLessonAdapter` (no enrichment for cloze).
- `flutter test`: Verify "Skip" flow emits `success: false` effort but `true` completion.

### Manual Verification
- Verify `lesson_content.v1.json` includes `cloze_practice` nodes or downgraded `typing_practice` nodes.
- Verify in-app skip behavior and effort reporting.
