# AGG-GEN-020 Detailed Test Plan for Flutter Frontend Transfer (A1-U04 Mockup)

Status: Draft v1
Audience: Gemini implementation streams (parallel execution)
Scope: tests/specs for porting the A1-U04 unit mockup sequencing into existing Flutter frontend with minimal redesign.

## 1. Test Objective

Validate that the frontend can render and run a mixed-form, output-heavy unit sequence (A1-U04) without breaking existing lesson assumptions.

Primary concerns:
- sequence rendering by `learning_role`
- `content_form` diversity support
- controlled/guided output interactions
- review node behavior
- adapter stability between aggregator schema and frontend model

## 2. Test Layers (Recommended)

1. Contract tests (adapter / parsing)
2. Widget tests (node renderers)
3. Flow integration tests (unit sequence progression)
4. Golden tests (visual regression for key node types)
5. Manual QA scripts (PM/Product validation)

## 3. Test Fixtures

Source fixtures (aggregator side):
- `../mockups/agg_gen_017_a1_u04_unit_mockup_data.json`

Frontend test fixtures to create (Gemini Stream A):
- `test/fixtures/a1_u04_unit_blueprint.json` (frontend-adapter target shape)
- `test/fixtures/nodes/*.json` (one fixture per form/node type)

Versioning rule:
- freeze fixtures per sprint (`v0`, `v1`) to avoid schema churn breaking unrelated tests

## 4. Gemini Parallel Streams (Detailed)

## Stream A — Adapter + Contract Tests

### Scope

- Parse aggregator/mockup data
- Convert into frontend node view models
- Preserve `content_form`, `learning_role`, `output_mode`

### Deliverables

- Adapter mapping spec doc
- Adapter implementation (frontend-side or shared package)
- Contract test suite

### Contract Test Cases

1. `parses_unit_metadata`
- input: mockup data JSON
- assert: `unit_id`, `target_language`, `learner_locale_source`, `output_ratio_target` preserved

2. `maps_all_sequence_items`
- assert node count matches source (`12`)
- assert ordering preserved

3. `maps_learning_role_without_loss`
- assert all roles represented exactly as source

4. `maps_output_modes_for_path_nodes`
- assert `chunk_assembly`, `response_builder`, `guided`, `review_retrieval` are preserved

5. `supports_multiskill_items`
- source item with multiple `skill_focus` values does not crash
- define fallback mapping (primary skill + metadata)

6. `ignores_unknown_metadata_safely`
- adapter should preserve or ignore unsupported fields without fatal error

7. `fallback_for_unknown_content_form`
- unknown form maps to generic renderer model instead of crash

### Risks to Watch

- enum mismatch (`reading_writing` temporary value in docs/mockup vs strict single enum schema)
- null/optional fields causing parser crashes

## Stream B — Node Renderers + Widget Tests

### Scope

Render each supported node type in Flutter using current app shell/components where possible.

### Deliverables

- renderer switch by `candidate_type` + `content_form` + `learning_role`
- placeholder/fallback renderer
- widget tests for each node type
- golden tests for key visual states

### Minimum Supported Renderers (for A1-U04)

1. `lesson:dialogue`
2. `lesson:notice`
3. `lesson:message_thread`
4. `lesson:comparison_card`
5. `grammar_note:structure_pattern`
6. `grammar_note:structure_grammar`
7. `dictionary_pack:functional phrases`
8. `path_node:chunk_assembly`
9. `path_node:response_builder`
10. `path_node:guided` (speaking prompt)
11. `path_node:guided` (writing prompt)
12. `path_node:review_retrieval`

### Widget Test Matrix

1. `renders_title_summary_and_duration`
- all node renderers show required header fields

2. `renders_dialogue_turns`
- dialogue node displays speaker lines in sequence

3. `renders_notice_bullets`
- notice node displays short policy bullets without conversation UI

4. `renders_message_thread_as_chat_bubbles_or_list`
- message thread node displays sender/message structure

5. `renders_comparison_card_two_options`
- comparison data visible and scannable

6. `renders_pattern_card_slots`
- structure pattern node shows sentence frames + slot examples

7. `renders_dictionary_pack_sections`
- grouped phrase sections visible (menu/quantity/options/payment)

8. `fallback_renderer_handles_unknown_form`
- unknown form shows generic card + does not crash

### Golden Test Targets

- dialogue node
- notice node
- comparison card
- chunk assembly node
- review retrieval node

## Stream C — Interaction Logic (Path Nodes) + Tests

### Scope

Implement text-based/selection-based interactions for output-heavy nodes (no audio capture required yet).

### Deliverables

- `chunk_assembly` interaction
- `response_builder` interaction
- `guided writing` draft entry
- `review_retrieval` prompt/reveal behavior
- state persistence within unit session (in-memory acceptable for first pass)

### Interaction Test Cases

#### `chunk_assembly`

1. `shows_chunks_and_target_area`
2. `allows_selecting_chunks_in_order`
3. `allows_resetting_attempt`
4. `completes_when_required_slots_filled`
5. `stores_attempt_state_when_navigating_next_and_back`

#### `response_builder`

6. `shows_prompt_and_response_choices_or_input`
7. `accepts_short_response_submission`
8. `does_not_require_long_sentence_for_completion`

#### `guided_writing`

9. `shows_prompt_constraints`
10. `accepts_1_to_2_line_input`
11. `marks_complete_with_minimum_length_or_required_fields`

#### `review_retrieval`

12. `shows_retrieval_prompt_before_answer`
13. `supports_reveal_hint_or_answer`
14. `records_attempt_without_auto-grading_requirement`

## Stream D — Unit Flow Integration + Regression Tests

### Scope

Validate end-to-end progression through the A1-U04 sequence.

### Deliverables

- integration tests for full unit sequence
- progress tracking assertions
- resume behavior checks (if session persistence exists)

### Integration Test Cases

1. `loads_full_unit_sequence_in_order`
- start at item 1, progress through all nodes in mockup order

2. `progress_counts_completed_nodes`
- completion counter updates across mixed node types

3. `supports_mixed_input_and_output_nodes_without_state_loss`
- complete an output node, visit input node, return to output node state preserved

4. `review_node_appears_after_immersion_output`
- sequence ordering matches curriculum design intent

5. `displays_cross_unit_transfer_as_scheduled_followup_not_inline_required`
- followups shown as future tasks, not blocking current unit completion

6. `unknown_optional_node_does_not_block_unit`
- optional/future nodes gracefully skipped if renderer unavailable

## 5. Manual QA Script (PM/Product Trial)

Use this after a runnable Flutter mock integration is available.

### Session Checklist (A1-U04)

1. 看起來不像只有「對話課」嗎？
2. 能明確感受到 `輸入 -> 結構 -> 輸出 -> 複習` 節奏嗎？
3. 拼句型與回應建構是否降低初級負擔？
4. 寫作節點是否仍屬於可完成的 1-2 句輸出？
5. 複習節點是否是回想（不是再看一次）？
6. 有看到跨單元遷移的安排嗎？

### Failure Examples (Product-facing)

- 對話占比過高，其他形式只是裝飾
- grammar note 太長，打斷任務節奏
- output node 跳太大（直接自由寫作）
- review node 退化成選擇題辨識

## 6. Suggested Work Breakdown and Sequence

### Phase 1 (parallel)

- Stream A: adapter + contract tests
- Stream B: basic renderers + fallback + goldens (input nodes first)

### Phase 2 (parallel)

- Stream C: path-node interactions + tests
- Stream B: remaining path-node renderers

### Phase 3

- Stream D: full sequence integration tests
- PM/Product manual trial using A1-U04 script

## 7. Definition of Done (AGG-GEN-020)

- detailed test matrix exists and is assignable to multiple Gemini streams
- adapter/renderer/interaction/integration test coverage is explicitly separated
- A1-U04 mockup is the common fixture across streams
- manual QA checklist is included for non-engineering review
