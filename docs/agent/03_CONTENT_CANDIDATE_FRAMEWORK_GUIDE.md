# Agent Docs: Content Candidate Framework Guide (Draft v1)

Language policy: English only.

Purpose: preserve the agreed content-form taxonomy, unit skeleton, and output-heavy learning-loop rules used by the content candidate generation/review framework.

Scope:
- `release-aggregator` content candidate generation/review framework
- Schema/brief/QA/review-bundle design inputs
- Not learner-app UI planning

Related task IDs:
- `AGG-GEN-016`
- `AGG-GEN-017`
- `AGG-GEN-018`

Formal task spec draft:
- `docs/tasks/AGG_GEN_017_CURRICULUM_LEARNING_LOOP_SPEC.md`

## Why This Exists

Do not model lesson content as only `dialogue` vs `article`.
That split is too coarse for generation balancing, gap analysis, QA, and review decisions.

Use a taxonomy so the system can:
- request specific forms in generation briefs
- detect missing forms and output modes in QA
- preserve course-role intent during review

## Default Unit Skeleton (A1/A2)

1. `immersion_input` (situation onboarding)
2. `structure_pattern` (core sentence frames)
3. `structure_grammar` (minimal grammar note)
4. `controlled_output` (substitution / guided role-play)
5. `immersion_output` (full task output in context)
6. `review_retrieval` (same-day retrieval)
7. `cross_unit_transfer` (scheduled review at `+1` / `+3` units)

## Four-Skill Integration (Output-Heavy)

Rule: every input segment should have an output hook.

Recommended A1/A2 time split:
- `Input (listening + reading)`: `30-35%`
- `Structure (patterns + grammar)`: `20-25%`
- `Output (speaking + writing)`: `40-50%`

Output ladder:
- `controlled`
- `guided`
- `open_task`
- `retell`
- `transform`

## `content_form` Taxonomy v1 (Enum)

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

## Form Usage Notes (Short)

- `dialogue`: turn-taking interaction; avoid overuse.
- `monologue`: explanation/share; good for retell tasks.
- `message_thread`: practical async communication; good for writing output.
- `notice`: short public text; add output follow-up task.
- `form_profile`: functional reading-writing integration.
- `schedule_timetable`: planning and justification tasks.
- `howto_steps`: sequence/procedural language.
- `comparison_card`: decision + reasons (high-value output form).
- `mini_story`: narrative retell/continuation.
- `article_short`: keep limited in A1/A2; attach summary/response output.
- `faq_qa`: functional Q&A patterns.
- `announcement_broadcast`: key-info listening + retell.
- `image_prompt`: high-output, low-reading-load prompt form.

## Additional Axes (Schema/Brief/QA)

### `learning_role`
- `immersion_input`
- `structure_pattern`
- `structure_grammar`
- `controlled_output`
- `immersion_output`
- `review_retrieval`
- `cross_unit_transfer`

### `skill_focus`
- `listening`
- `speaking`
- `reading`
- `writing`
- `integrated`

### `output_mode`
- `none`
- `controlled`
- `guided`
- `open_task`
- `retell`
- `transform`
- `review_retrieval`

## Candidate Type Mapping Guidance

- `lesson`: may use many forms, not only `dialogue`
- `grammar_note`: minimal grammar in support of output
- `dictionary_pack`: favor functional phrases/collocations + usage context
- `path_node`: preferred for output/review/retrieval/transfer nodes

## QA Balance Rules (Draft)

- At least 1 non-dialogue input per unit
- At least 1 writing output per unit
- At least 1 `open_task` / `retell` / `transform` output per unit
- `dialogue` should not exceed ~60% of unit input content
- Every `grammar_note` should link to at least 1 output node
- Cross-unit review nodes must declare recycled source units

## Minimum A1/A2 Unit Package (Draft)

- 1x immersion lesson (`dialogue` or `monologue`)
- 1x non-dialogue input lesson (`notice` / `message_thread` / `schedule_timetable` / etc.)
- 1-2x `grammar_note`
- 1x `dictionary_pack` (functional phrases/collocations)
- 1x `path_node` controlled output
- 1x `path_node` open output
- 1x `path_node` same-unit retrieval
- cross-unit review nodes scheduled at `+1` / `+3` units

## Multilingual Curriculum Reminder

Model content with separate axes:
- `target_language` (language being learned)
- `learner_locale` (pedagogy language)

Default v1 assumption:
- `learner_locale_source = zh-TW`

Future learner locales (`en`, `ja`, ...) should localize pedagogy overlays instead of duplicating target-language core content.
