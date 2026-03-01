# TLG-014: Reading Rubric Specification (Reading Assessment)

This specification defines the evaluation logic for reading comprehension tasks within the Target Language Generator pipeline. It builds upon the Reading Skeleton Spec (`TLG-013_READING_SKELETON_SPEC.md`) and establishes a rubric distinct from speaking/writing evaluations, prioritizing comprehension and inference over production mechanics.

## 1. Distinction from Speaking/Writing Rubrics

While productive skills (speaking/writing) assess grammar, vocabulary usage, pronunciation, and fluency, reading evaluation focuses purely on *receptive processing*.

The core difference: **We are not scoring how well they say it, but how accurately they understood it, and whether they can justify that understanding.**

## 2. Reading Assessment Metrics

The reading rubric evaluates three primary dimensions:

### 2.1 Comprehension Accuracy (`comprehension_accuracy`)
*   **Definition**: The basic correctness of the learner's response to literal or inferential questions.
*   **Applicability**: Multiple-choice, True/False, Fill-in-the-blank (from text).
*   **Scoring**: Binary (Correct/Incorrect) or Partial (e.g., selecting 2 out of 3 correct options).

### 2.2 Evidence Location (`evidence_location`)
*   **Definition**: The learner's ability to precisely locate the specific span of text that justifies their answer.
*   **Applicability**: Highlights, drag-and-drop text snippets, explicit line/paragraph references.
*   **Scoring**:
    *   3: Precise identification of the necessary span only.
    *   2: Broad identification containing the relevant span but also extraneous text.
    *   1: Identifies related but incorrect evidence.
    *   0: Incorrect or missing evidence mapping.

### 2.3 Inference Validity (`inference_validity`)
*   **Definition**: When answering inferential questions, how logical is the conclusion drawn from the provided text?
*   **Applicability**: Short-answer reading questions, evaluative tasks (e.g., "Why did the author say X?").
*   **Scoring (LLM Assessed)**:
    *   3: Logically sound, explicitly linking background knowledge or context clues to textual evidence.
    *   2: Plausible inference but lacks strong textual grounding.
    *   1: Weak or illogical inference unrelated to the text's core message.
    *   0: Literal misinterpretation or completely off-topic.

## 3. Rubric Matrix by Question Type

The evaluation logic shifts slightly depending on the `question_blueprint` category (defined in TLG-013).

| Question Category | Primary Assessment Dimension | Secondary Assessment Dimension | Required Action |
| :--- | :--- | :--- | :--- |
| **literal** | Comprehension Accuracy (100%) | N/A | Find matching fact |
| **inferential** | Comprehension Accuracy (50%) | Inference Validity (50%) | Connect clues |
| **evaluative** | Inference Validity (70%) | Comprehension Accuracy (30%) | Assess tone/intent |
| **structure/cohesion**| Evidence Location (80%) | Comprehension Accuracy (20%) | Identify referents |

## 4. Error Analytics and Diagnostics

Reading errors provide specific diagnostic feedback for personalized learning paths.

*   **Error Type: Vocabulary Misunderstanding** -> Triggers review of specific lexical items.
*   **Error Type: Syntactic Confusion** -> Triggers review of grammar structures (e.g., missed relative clauses).
*   **Error Type: Faulty Inference** -> Suggests difficulty integrating information across sentences; prompts simpler cohesion exercises.
*   **Error Type: Evidence Mismatch** -> Correct answer chosen, but wrong evidence cited. Indicates guessing or shallow skimming instead of scanning.

## 5. Integration with the Generator

When evaluating free-text responses to reading tasks, the LLM prompt must strictly isolate comprehension. It must *ignore* the learner's grammatical mistakes in their response, provided the underlying understanding of the source text is clear. The assessment prompt demands mapping the learner's reasoning back to the `evidence_mapping` provided during the task generation phase.

## 6. Alignment with TLG-003

This reading rubric is a **skill-specific extension** and does not replace TLG-003 output-mode rubrics.

Alignment rules:

1. Keep TLG-003 hard-valid threshold range (`0.50 <= pass_threshold <= 1.00`).
2. Store reading weights in reading overlay payload (`comprehension_accuracy_weight`, `evidence_location_weight`, `inference_validity_weight`).
3. For mixed-mode tasks, use TLG-003 as base pass logic and apply this reading rubric as a sub-score profile.

## 7. Suggested Checker Rules (TLG-006 Reading Gate)

### Blockers
- `ERR_TLR_MISSING_EVIDENCE_MAPPING`: question lacks evidence span mapping.
- `ERR_TLR_EVIDENCE_QUESTION_MISMATCH`: question_id in blueprint not found in evidence mapping.
- `ERR_TLR_RUBRIC_WEIGHT_INVALID`: reading weight values out of [0,1] range.
- `ERR_TLR_PASS_THRESHOLD_INVALID`: pass threshold out of [0.5,1.0].

### Warnings
- `WARN_TLR_LITERAL_WITHOUT_EVIDENCE_SCORE`: literal question missing evidence-based scoring dimension.
- `WARN_TLR_INFERENCE_WITHOUT_VALIDITY_SCORE`: inferential/evaluative item has no inference validity weight.
