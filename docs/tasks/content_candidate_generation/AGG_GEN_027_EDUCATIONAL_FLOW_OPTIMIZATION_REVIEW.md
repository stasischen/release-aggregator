# AGG-GEN-027 — Educational Flow Optimization Review (Unit Sequencing Mockup)

## Scope

This review focuses on the educational design of the current unit sequencing flow (A1/A2 survival style):

- immersion input
- structured pattern/grammar support
- controlled output
- guided output
- retrieval review
- cross-unit transfer

This document does **not** redesign the learner app UI and does **not** change the content generation framework implementation directly. It documents optimization points that should feed into:

- `AGG-GEN-018` (schema/brief extensions)
- `AGG-GEN-024` (unit blueprint scaffolding/templates)
- future unit fixture QA rules

## Current Strengths (Keep)

1. **Three-track integration is correct**
- Immersion + Structure + Review is combined in one unit flow, not split into disconnected courses.

2. **Output-heavy direction is appropriate**
- `chunk_assembly` + `response_builder` + `guided` supports beginner output without jumping to full free writing.

3. **Node-level sequencing works well**
- `candidate_type`, `content_form`, `output_mode`, `learning_role` together create a scalable course "node engine" model.

4. **Review is already retrieval-oriented**
- `review_retrieval` is stronger than passive summary review.

## Optimization Areas (Educational)

### 1) Add a micro comprehension check after immersion input

**Issue**
- Current flow can move from input (dialogue/notice/message) directly into structure without confirming comprehension.

**Recommendation**
- Add a short non-scored comprehension checkpoint after the first immersion input block.

**Good formats (A1/A2)**
- key info extraction (time / price / location)
- intent identification ("What is the speaker trying to do?")
- order/sequence check

**Why**
- Prevents learners from relying only on zh-TW translation and skipping input processing.

### 2) Add an explicit "pattern transform" layer between controlled and guided output

**Issue**
- Jumping from chunk assembly / response selection directly to guided output can still feel large for beginners.

**Recommendation**
- Add a transform layer:
  - ice -> hot
  - dine-in -> take-out
  - card -> cash
  - cafe -> restaurant

**Why**
- This is the key step from memorizing a sentence to using a pattern productively.

### 3) Split review retrieval targets (form vs function)

**Issue**
- Current review retrieval tends to mix all recall into one type.

**Recommendation**
- Tag review nodes with retrieval focus:
  - `form` (how to say it)
  - `function` (how to respond in context)
  - `mixed`

**Why**
- Survival learning needs both expression recall and response-speed recall.

### 4) Add repair/recovery practice (high educational value for survival)

**Issue**
- Current unit flow emphasizes ideal outputs but not recovery when communication fails.

**Recommendation**
- Add at least one repair micro-node per unit (practice or path node):
  - "Please say that again."
  - "I don't understand."
  - "Not this one, I want ___."
  - "Can I pay cash?"

**Why**
- Increases real-world survivability and reduces learner anxiety.

### 5) Push dictionary packs further toward usable chunks/collocations

**Issue**
- Even with good vocabulary grouping, packs can drift toward "word lists."

**Recommendation**
- Ensure each section includes:
  - item/phrase
  - common frame/collocation
  - replaceable slots

**Why**
- Vocabulary should directly support output, not become isolated memorization.

### 6) Make scheduled followups task-specific (not reminder-only)

**Issue**
- Followups can become generic reminders instead of transfer tasks.

**Recommendation**
- Encode the transfer pattern + target scenario explicitly.

**Example**
- U04 -> Accommodation: use `주세요` to request towel / Wi-Fi password
- U04 -> Pharmacy: use `말고` to ask for an alternative item

**Why**
- Spaced review becomes "reuse in a new context" instead of "repeat old content."

## Proposed `unit_blueprint v0.x` Field Additions (Backward-safe Proposal)

These are **proposals** for fixture/template evolution. Do not break current `unit_blueprint_v0` fixtures.

### Node-level educational metadata

- `learning_objective_type`
  - enum (proposed): `comprehension | production | repair | retrieval | transfer`

- `difficulty_scaffold_level`
  - enum (proposed): `high | medium | low`
  - especially useful for beginner output nodes

- `completion_evidence`
  - array (proposed), examples:
    - `viewed`
    - `attempted`
    - `draft_saved`
    - `self_checked`
    - `manually_marked`

### Review node-specific metadata

- `retrieval_target`
  - enum (proposed): `form | function | mixed`

### Transfer / followup metadata

- `transfer_pattern_refs`
  - array of pattern IDs or strings, e.g. `["주세요", "할게요", "말고"]`

- `transfer_task_hint_zh_tw`
  - short Chinese task instruction for followup placement/review

### Comprehension check payload hint (new content form or mode extension)

- `comprehension_check` (proposed content_form or practice subtype)
  - `questions[]`
  - `question_type`
  - `answer_key` (optional for mockup; may remain hidden)

## Suggested Template Defaults for `AGG-GEN-024`

For each beginner survival unit skeleton, require at least:

1. `immersion_input` x1 (`dialogue` or `monologue`)
2. `non-dialogue input` x1 (`notice` / `message_thread` / `comparison_card` etc.)
3. `comprehension_check` x1 (non-scored)
4. `structure_pattern` x1
5. `structure_grammar` x1
6. `dictionary_pack` x1 (chunk-oriented)
7. `controlled_output` x2 (`chunk_assembly`, `response_builder`)
8. `pattern_transform` x1 (can be `practice_card`)
9. `guided output` x1 (speaking or writing)
10. `repair practice` x1
11. `review_retrieval` x1
12. `scheduled_followups` with transfer pattern refs

## QA Checklist (Educational Quality) — Candidate/Fixture Review

Use these checks in addition to schema/lint checks:

1. **Input comprehension check exists**
- Unit has at least one non-scored comprehension checkpoint after immersion input.

2. **Output progression exists**
- Unit contains controlled -> transform -> guided progression (not only chunk assembly + guided).

3. **Repair practice exists**
- Unit includes at least one repair/recovery response node.

4. **Review target is explicit**
- Review node marks `retrieval_target` (or equivalent metadata).

5. **Transfer followup is task-specific**
- Followups mention what pattern is being transferred and to what scenario.

6. **Dictionary supports production**
- Dictionary pack includes collocations/frames, not only nouns.

## Mapping to Existing AGG-GEN Tasks

- `AGG-GEN-018`
  - add/adopt educational metadata in schema/brief extensions
- `AGG-GEN-024`
  - bake these requirements into scaffold templates and authoring checklists
- `AGG-GEN-025`
  - add QA/lint warnings for missing educational structure (lightweight)

## Priority Recommendations (What to Implement First)

1. Add `pattern_transform` and `repair practice` to the unit template (`AGG-GEN-024`)
2. Add `retrieval_target` + `transfer_pattern_refs` metadata proposal to `AGG-GEN-018`
3. Add educational QA warnings (not blockers yet) in `AGG-GEN-025`

## Notes

- This proposal is intentionally backward-safe: current A1-U04 mockup can remain playable while templates/metadata evolve.
- Do not overfit to Korean; the same educational structure should remain target-language-agnostic.
