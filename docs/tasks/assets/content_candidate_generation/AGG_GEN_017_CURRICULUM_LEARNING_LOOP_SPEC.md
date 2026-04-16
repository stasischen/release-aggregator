# AGG-GEN-017 Curriculum Learning-Loop Design Spec (Draft v1)

Status: Draft v1 (ready for schema/brief integration in `AGG-GEN-018`)
Scope: content candidate generation/review framework only (`release-aggregator`)

Related tasks:
- `AGG-GEN-016` multilingual curriculum architecture blueprint
- `AGG-GEN-017` curriculum learning-loop design
- `AGG-GEN-018` schema/brief extensions (taxonomy + review cadence metadata)

Reference full unit example:
- `AGG_GEN_017_A1_U04_SURVIVAL_FULL_UNIT_EXAMPLE.md`
- `AGG_GEN_019_UNIT_MOCKUP_FRONTEND_TRANSFER_PLAN.md`
- `AGG_GEN_020_FRONTEND_TRANSFER_TEST_PLAN.md`

## 1. Goal

Define a course-design framework so candidate generation produces curriculum components with clear learning roles, not just isolated content pieces.

The framework must support:
- immersive learning (`Immersion`)
- spaced review / retrieval (`Spaced Review`)
- structured learning (`Structure`: sentence patterns + minimal grammar)

Primary product direction (v1):
- `zh-TW` pedagogy-first review and planning
- target languages start with `ko` but design must generalize

## 2. Core Design Principles

1. Task-first, not grammar-chapter-first
- Units are organized by survival tasks/scenarios.
- Grammar exists to enable output, not as an isolated lecture track.

2. Output-heavy early learning (with scaffolding)
- Beginners should produce language early.
- Initial output is chunk/pattern assembly, not free composition.

3. Multi-form input, not only dialogue/article
- Use `content_form taxonomy` to avoid overconcentration in dialogue.

4. Retrieval and transfer are first-class content
- Review nodes are generated/planned as curriculum components (`path_node`), not treated as optional extras.

5. Unit-role clarity for every candidate
- Every candidate should declare a course role (`learning_role`) and expected output mode (if any).

## 3. Unit Skeleton (A1/A2 Default)

Recommended base sequence for each unit:

1. `immersion_input`
- Situation onboarding (dialogue / monologue / message / notice)
- Goal: comprehension + task awareness

2. `structure_pattern`
- Core sentence frames and reusable chunks
- Goal: enable first controlled output

3. `structure_grammar`
- Minimal grammar note required for the unit's task
- Goal: prevent output failure, avoid lecture overload

4. `controlled_output`
- Chunk assembly / frame fill / response builder / guided role-play
- Goal: reliable sentence production

5. `immersion_output`
- Contextual task completion (speaking or writing, often both)
- Goal: complete a survival task using target patterns

6. `review_retrieval` (same day)
- Low/medium prompt recall of key patterns and responses
- Goal: immediate retrieval strengthening

7. `cross_unit_transfer` (`+1 unit`, `+3 units`)
- Reuse old patterns in new scenarios
- Goal: transfer and retention, not re-exposure

## 4. Four-Skill Integration with Output-Heavy Bias

Design rule:
- Every input segment should lead to an output hook.

Recommended time split (A1/A2 baseline):
- `Input (listening + reading)`: `30-35%`
- `Structure (patterns + minimal grammar)`: `20-25%`
- `Output (speaking + writing)`: `40-50%`

Output should be staged:
- `controlled` -> `guided` -> `open_task` / `retell` / `transform`

Beginner note:
- Replace "writing" with "written output" in early units.
- Accept short replies, message responses, and sentence assembly as valid writing outputs.

## 5. Content Taxonomy (v1)

This taxonomy is used by generation briefs, QA, and review station planning.

### 5.1 `content_form` enum (v1)

- `dialogue`
- `monologue`
- `message_thread`
- `notice`
- `form_profile`
- `schedule_timetable`
- `howto_steps`
- `comparison_card`
- `mini_story`
- `article_short`
- `faq_qa`
- `announcement_broadcast`
- `image_prompt`

### 5.2 `learning_role` enum (v1)

- `immersion_input`
- `structure_pattern`
- `structure_grammar`
- `controlled_output`
- `immersion_output`
- `review_retrieval`
- `cross_unit_transfer`

### 5.3 `skill_focus` enum (v1)

- `listening`
- `speaking`
- `reading`
- `writing`
- `integrated`

### 5.4 `output_mode` enum (beginner-friendly v1)

- `none`
- `chunk_assembly`
- `frame_fill`
- `response_builder`
- `pattern_transform`
- `guided`
- `open_task`
- `retell`
- `transform`
- `review_retrieval`

## 6. Candidate Type Mapping (Framework)

### `lesson`

Use for immersion and applied task content. Must not be treated as dialogue-only.

Recommended forms:
- `dialogue`
- `monologue`
- `message_thread`
- `notice`
- `schedule_timetable`
- `comparison_card`
- `mini_story`
- `article_short`
- `faq_qa`
- `announcement_broadcast`

### `grammar_note`

Use for minimal-necessary structure support:
- pattern clarification
- grammar constraint that blocks output
- examples tied to current unit task

Should declare links to:
- source forms seen in unit
- at least one output node consuming the grammar/pattern

### `dictionary_pack`

Use for:
- functional phrases
- collocations
- scenario bundles
- response chunks (not only isolated nouns/verbs)

### `path_node`

Preferred for:
- controlled output
- retrieval review
- cross-unit transfer
- mixed-skill checkpoints
- output challenges

## 7. QA Balance Rules (Draft v1)

Use these as curriculum-level QA checks (unit or batch scope):

1. `NON_DIALOGUE_INPUT_MISSING`
- Each unit should include at least 1 non-dialogue input item.

2. `WRITING_OUTPUT_MISSING`
- Each unit should include at least 1 writing-oriented output (can be scaffolded).

3. `OPEN_OR_RECALL_OUTPUT_MISSING`
- Each unit should include at least 1 of:
  - `open_task`
  - `retell`
  - `transform`
  - `review_retrieval`

4. `DIALOGUE_OVERWEIGHT`
- Dialogue should not exceed ~60% of input-heavy items in a unit.

5. `GRAMMAR_NOTE_DISCONNECTED`
- Every `grammar_note` should map to at least one output node.

6. `CROSS_UNIT_REVIEW_SOURCE_MISSING`
- `cross_unit_transfer` nodes must declare source unit(s) reused.

7. `OUTPUT_LADDER_GAP`
- Unit should include at least two output scaffolding levels before fully open output (or justify omission).

## 8. Beginner Survival Course Blueprint (Korean in Korea, A0-A1+/A2-)

This blueprint is the first reference profile for v1.

### 8.1 Course Outcome

Learners should be able to complete common survival tasks in Korea:
- greetings + self-introduction
- numbers/time/price
- transit and wayfinding
- ordering food and paying
- shopping basics
- accommodation check-in and requests
- messaging for scheduling changes
- pharmacy/basic symptoms
- communication repair and asking for help
- reading signs/notices/UI text
- comparing choices and giving short reasons

### 8.2 Suggested Core Units (12)

1. Arrival and first-day greetings
2. Numbers / time / dates / prices
3. Transit and directions
4. Cafe/restaurant ordering
5. Shopping and payment
6. Accommodation (check-in / requests)
7. Messaging and scheduling changes
8. Symptoms and pharmacy survival
9. Emergency help and communication repair
10. Signs/notices/UI text comprehension
11. Planning/comparison/decision + reasons
12. Integrated survival mission (mixed task flow)

### 8.3 Per-Unit Minimum Package (A1/A2)

- 1x immersion `lesson` (`dialogue` or `monologue`)
- 1x non-dialogue input `lesson`
- 1-2x `grammar_note` (minimal)
- 1x `dictionary_pack` (functional phrases/collocations)
- 1x `path_node` controlled output
- 1x `path_node` guided/open output
- 1x `path_node` same-day retrieval
- cross-unit review node(s) scheduled for `+1` / `+3` units

## 9. Detailed Example: A1-U04 Cafe/Restaurant Ordering (Survival)

This example is the canonical design sample for `AGG-GEN-017`.

### 9.1 Unit Goal

Learner can order food/drinks, answer basic staff questions, and complete payment in a cafe/restaurant context.

### 9.2 Can-do Outcomes (zh-TW review-ready style)

- 能用簡短句子點餐並指定品項與數量
- 能回應店員詢問（內用/外帶、冰/熱、尺寸）
- 能確認金額與付款方式
- 能用訊息和朋友約吃飯並確認時間/地點（簡短）

### 9.3 Required Pattern Functions

- requesting / ordering (`我要...`, `請給我...`)
- choices (`內用/外帶`, `冰/熱`)
- quantity (`一個/兩杯/...`)
- confirmation (`是這個嗎？`, `一共多少？`)
- payment (`刷卡可以嗎？`)
- preference/constraint (`不要...`, `少冰/去冰` style equivalents)

### 9.4 Minimal Grammar (Output-Serving)

Only include grammar that directly supports the unit task:
- polite request forms (minimal)
- negation for preference/avoidance
- quantity/classifier pattern basics
- question endings for confirmation

Avoid:
- long historical grammar explanations
- unrelated morphology deep dives

### 9.5 Content Components (Recommended Candidate Mix)

1. `lesson` / `dialogue` / `immersion_input`
- Staff-customer ordering dialogue
- Skill focus: `listening` + `speaking`

2. `lesson` / `notice` / `immersion_input`
- Store notice/menu policy (e.g., takeout, refill, peak time note)
- Skill focus: `reading`

3. `lesson` / `message_thread` / `immersion_input`
- "Where/when to meet?" cafe meetup chat
- Skill focus: `reading` + `writing`

4. `grammar_note` / `structure_pattern`
- ordering sentence frames and option slots

5. `grammar_note` / `structure_grammar`
- minimal polite request / negation pattern note

6. `dictionary_pack`
- menu items, quantity units, payment phrases, preference chunks

7. `path_node` / `controlled_output`
- `chunk_assembly`: assemble order sentences

8. `path_node` / `controlled_output`
- `response_builder`: answer staff prompts

9. `path_node` / `immersion_output`
- `guided`: complete a role-play order with 3 constraints

10. `path_node` / `immersion_output`
- `guided` or `open_task`: send a short meetup/order-related message

11. `path_node` / `review_retrieval`
- same-day recall of key ordering and response patterns

12. `path_node` / `cross_unit_transfer` (scheduled)
- transfer request/confirmation patterns to another service context (e.g. hotel or pharmacy)

### 9.6 Output Ladder (Beginner-Friendly)

Recommended progression inside U04:

1. `chunk_assembly`
- Build: item + quantity + request

2. `frame_fill`
- Fill slot values for temperature/size/takeout

3. `response_builder`
- React to clerk questions with valid short responses

4. `pattern_transform`
- Change quantity / item / politeness / dine-in vs takeout

5. `guided` speaking task
- Complete ordering with prompt cards (budget, item, preferences)

6. `guided` writing task
- Write a 1-2 line meetup/order confirmation message

7. `review_retrieval`
- Recall key phrases with minimal prompts

### 9.7 Suggested Generation Brief Targets (for This Unit)

For a single-unit content-candidate batch (`A1-U04`) baseline:

```json
{
  "target_units": ["A1-U04"],
  "candidate_types": ["lesson", "grammar_note", "dictionary_pack", "path_node"],
  "content_form_targets": {
    "dialogue": 1,
    "notice": 1,
    "message_thread": 1,
    "comparison_card": 1
  },
  "learning_role_targets": {
    "immersion_input": 3,
    "structure_pattern": 1,
    "structure_grammar": 1,
    "controlled_output": 2,
    "immersion_output": 2,
    "review_retrieval": 1
  },
  "output_mode_targets": {
    "chunk_assembly": 1,
    "response_builder": 1,
    "guided": 2,
    "review_retrieval": 1
  },
  "output_ratio_target": 0.45
}
```

Notes:
- `comparison_card` can compare menu choices/price/size and feed a decision-output node.
- If only one batch is generated, `cross_unit_transfer` may be scheduled as a later batch artifact.

## 10. Metadata Requirements for AGG-GEN-018 (Schema/Brief Extensions)

`AGG-GEN-018` should add or document the following fields (v1.1 or metadata extension):

Required/strongly recommended:
- `target_language`
- `learner_locale_source`
- `content_form`
- `learning_role`
- `skill_focus`
- `output_mode`

Recommended for review cadence:
- `revisit_after_units` (e.g. `[1, 3]`)
- `review_window_days` (e.g. `[0, 2, 7]`)
- `recycle_from_units` (for transfer/review nodes)

Recommended for curriculum linking:
- `depends_on_candidate_ids`
- `consumes_grammar_focus`
- `consumes_pattern_focus`
- `produces_can_do_tags`

Recommended for frontend adapter contract stability (adapter-first, non-UI):
- `is_optional`
- `unlock_behavior`
- `resource_links` (`lesson_ids`, `grammar_note_ids`, `dictionary_terms`)
- `adapter_hints` (`entry_surface`, `completion_mode`, optional renderer override keys)

Reference:
- `AGG_GEN_018_SCHEMA_BRIEF_EXTENSION_SPEC.md` (adapter contract requirements + unit blueprint alignment)

## 11. Definition of Done for AGG-GEN-017

This task is considered complete when:
- the unit skeleton and learning-loop design are documented
- content taxonomy + supporting axes are documented
- QA balance rules are enumerated
- at least one A1 sample unit is fully specified
- generation brief implications are explicit enough for schema integration
