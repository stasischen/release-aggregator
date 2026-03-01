# TLG-013: Reading Comprehension Architecture (Reading Skeleton Spec)

This specification defines the dedicated architecture for reading comprehension tasks within the Target Language Generator pipeline. It extends the core function layer to handle reading-specific metrics and structures, separating them from the conversational/dialogue-focused elements.

## Rationale

The existing `survival/dialogue` architecture is optimized for real-time interaction, spoken patterns, and communicative tasks. Reading comprehension requires a distinct approach emphasizing text analysis, progressive understanding, and evidence-based inference. This document specifies the `Reading Comprehension Architecture` layer.

## 1. Core Structure Overview

The reading architecture acts as a parallel track to the conversational track, sharing the base generator pipeline but utilizing distinct node profiles and evaluation metrics.

### 1.1 The Shared Layer (Inherited from TLG-001/002)

Reading content inherits the core metadata structure:
*   `function_id`: Identifier for the primary communicative purpose (e.g., F-DESCRIBE-PROCESS).
*   `can_do`: The underlying CEFR "Can Do" statement alignment.
*   `level_range`: Target proficiency band (e.g., B1-B2).
*   `rubric_reference`: Pointer to base competencies.

### 1.2 The Reading-Specific Layer (New)

The reading track introduces a new metadata block to govern text properties and question generation.

#### A. Text Profile (`text_profile`)

Defines the parameters of the reading passage itself.
*   **`genre`**: Text type (e.g., `article`, `email`, `announcement`, `story`, `report`).
*   **`length_words`**: Target word count range (e.g., `150-200`).
*   **`lexical_coverage`**: Target percentage of vocabulary drawn from the target CEFR level (e.g., `90% A2, 10% B1`).
*   **`syntactic_density`**: Constraint on sentence complexity (e.g., `clauses_per_sentence`, `max_passive_voice`).

#### B. Reading Skill Targets (`reading_skill_targets`)

Specifies the cognitive skills being tested. A single passage usually addresses multiple skills.
*   `skimming`: Identifying the main idea / gist.
*   `scanning`: Locating specific facts or details.
*   `inference`: Deducing meaning not explicitly stated.
*   `reference`: Identifying what pronouns or cohesive devices refer to.
*   `cohesion`: Understanding structural relationships between sentences/paragraphs.

#### C. Question Blueprint (`question_blueprint`)

Categorizes the types of questions generated for the text.
*   `literal`: Answers explicitly found in the text (often tests scanning).
*   `inferential`: Requires combining information or background knowledge (tests inference).
*   `evaluative`: Requires assessing the author's purpose, tone, or overall argument.
*   `structure`: Questions about text organization or cohesive devices (tests cohesion).

#### D. Evidence Mapping (`evidence_mapping`)

Crucial for auto-generation and validation. Every question must be mapped to a specific `span` in the source text that justifies the correct answer.

## 2. Reading Task Flow (Skeleton)

Reading tasks follow a standardized three-phase structure within a unit.

### Phase 1: Pre-read
*   **Purpose**: Activate background knowledge (schema) and introduce critical vocabulary necessary for basic comprehension.
*   **Common Activity Types**: Vocabulary preview (matching), predicting content from titles/images, activating questions.

### Phase 2: While-read
*   **Purpose**: Guided engagement with the text, targeting specific reading skills.
*   **Common Activity Types**:
    1.  **First Pass (Gist)**: Skimming tasks (e.g., "What is the main topic?").
    2.  **Second Pass (Detail/Inference)**: Scanning and inference questions (literal and inferential question types).
    3.  **Third Pass (Discourse)**: Focus on structure, vocabulary in context, and discourse markers.

### Phase 3: Post-read
*   **Purpose**: Synthesize understanding, evaluate stance, and bridge to productive skills (speaking/writing).
*   **Common Activity Types**: Summary generation, author stance evaluation, "transfer" prompts (e.g., "Write a reply to this email based on the information provided").

## 3. Integration with Generation Pipeline

Input JSONs driving the TLG-005 generator for reading tasks must specify the `text_profile` and request a mix of questions adhering to the `question_blueprint`, requiring the LLM to output explicit `evidence_mapping` indices alongside answers.

**(See `docs/tasks/schemas/tlg005_reading_generator_input_v1.schema.json` for technical schema details.)**

## 4. Alignment with Existing TLG Contracts

To avoid creating a parallel pipeline, this reading architecture is treated as an **overlay layer** on top of existing contracts:

1. Base sequence stays under `TLG-002` (core nodes unchanged).
2. Mastery thresholds remain compatible with `TLG-003` threshold policy (`0.50-1.00` pass threshold).
3. Pattern/function alignment still references `TLG-004` where applicable.
4. Node integration follows `docs/tasks/schemas/tlg_layer_overlay_matrix_v1.json`:
   - Reading primary nodes: `L3`, `R1`, `X2`

## 5. Definition of Done (TLG-013)

TLG-013 is complete when:

1. This document is committed and references generator schema contract.
2. `tlg005_reading_generator_input_v1.schema.json` validates as JSON and is consumable by TLG-005.
3. Reading overlays are explicitly mapped to `L3/R1/X2` without breaking core sequence.
