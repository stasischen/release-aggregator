# KG Pipeline 006 / Course Restructure Notes

Date: 2026-04-16

## Context

This note captures the current discussion around `kg-pipeline-006`, the schema extension proposal, and the need to reopen course-structure design before proceeding with integration work.

## Current Consensus

- `kg-pipeline-006` can remain `in_progress`.
- `KNOWLEDGE_SCHEMA_EXTENSION_PROPOSAL_V1.md` is effectively a `review-ready draft`.
- No new blocking conflicts were identified in the current proposal.
- The proposal is still a proposal, not a schema freeze.

## Schema Direction Already Aligned

- `surface_variants` tracks morphological or surface-form variants for the same knowledge item.
- `aliases_{locale}` tracks localized learner-facing search aliases.
- `source_refs` tracks concept-level traceability back to lesson/video/history sources.
- `teaching_blocks_{locale}` tracks structured pedagogical blocks for a single knowledge item.

## What Existing Data Is Doing

- `dialogue_turns` and `normalized_segments` are the primary learning surface.
- `video` is a primary surface, alongside `dialogue`, for listening and situational immersion.
- `grammar_note.sections` is the closest existing shape to future `teaching_blocks`.
- `pattern_card` and `pattern_builder` are structure and output scaffolds.
- `example_sentence_refs` are evidence links for usage examples.
- `knowledge_refs` point from examples back to knowledge items.
- `source_refs` point from knowledge items back to the teaching source.
- `dict_grammar_mapping.json` is a POS / grammar-function mapping table, not a teaching-block system.

## Key Distinctions

- `dialogue/video` = primary content carrier.
- `example_sentence` = example evidence.
- `source_refs` = source traceability.
- `teaching_blocks` = internal pedagogical organization inside one knowledge item.
- `teaching_blocks` are not evidence and not source links.
- `teaching_blocks` are the future canonical target shape; `grammar_note.sections` is still the closest existing transitional shape.

## Course Structure Direction

The course should be understood as a sequence of layers, not just as `dialogue` versus `article`.
This aligns with ULV and `COURSE_MODULE_COMPOSITION`:

- `Content/Input` provides the situation and raw material.
- `Structure` breaks the material into teachable units.
- `Interaction/Output` provides controlled and task-based practice.
- `Review` provides retrieval and spacing.
- `Cross-unit Transfer` carries prior learning into later units.

```text
Unit
├─ Goal / Theme
├─ Input
│  ├─ dialogue
│  ├─ video
│  ├─ message_thread
│  └─ notice
├─ Structure
│  ├─ pattern_card
│  ├─ grammar_note
│  └─ functional_phrase_pack
├─ Controlled Output
│  ├─ frame_fill
│  ├─ response_builder
│  ├─ chunk_assembly
│  └─ pattern_transform
├─ Task Output
│  ├─ guided
│  ├─ retell
│  ├─ transform
│  └─ open_task
├─ Review
│  ├─ review_card
│  ├─ review_retrieval
│  └─ scheduled_followups
└─ Cross-unit Transfer
   ├─ +1 unit reuse
   └─ +3 units reuse
```

## Working Interpretation

- `Input` provides the situation and raw material.
- `Structure` breaks the material into teachable units.
- `Controlled Output` is safe practice.
- `Task Output` is actual transfer into new contexts.
- `Review` is retrieval and spacing.
- `Cross-unit Transfer` carries prior learning into later units.
- `pattern_card` and `pattern_builder` remain support scaffolds, not part of the knowledge-item payload.
- `review_policy` should stay a proposed contract until the task plan explicitly adopts it.
- `dialogue` and `video` are both input carriers; neither should be treated as a default primary over the other.

## Current Architectural Reading

This aligns with the existing course-design and runtime docs:

- `COURSE_MODULE_COMPOSITION` already defines content / interaction / review as the three-layer model.
- `07_CONTENT_CANDIDATE_COURSE_DESIGN` already describes a unit skeleton with input, structure, output, and review stages.
- ULV already separates primary surfaces from support detail surfaces.

## Practical Next Discussion Points

- Should `grammar_note.sections` be formally upgraded to `teaching_blocks`?
- Where is the hard boundary between `pattern_card` and `grammar_note`?
- Should `dialogue/video` remain input carriers, or also provide review / transfer hooks?
- Do we want an explicit `review_policy` contract?
- Should the unit skeleton be fixed as `Input -> Structure -> Output -> Review`?
- Can we keep `source_refs` as the canonical name and avoid renaming it in the knowledge-item schema?
- Should `teaching_blocks` be treated as the future canonical payload while `grammar_note.sections` stays transitional during migration?

## Reusable Prompt For Another Thread

```text
I want to reopen the course-structure discussion. Please do not add new data fields yet. The goal is to redefine how units / lessons are organized.

Current consensus:
1. kg-pipeline-006 can stay in_progress; the proposal is effectively review-ready and there are no new blocking conflicts.
2. KNOWLEDGE_SCHEMA_EXTENSION_PROPOSAL_V1 is aligned on:
   - surface_variants = surface-form variants for one knowledge item
   - aliases_{locale} = learner-facing search aliases
   - source_refs = concept-level traceability back to lesson/video/history sources
   - teaching_blocks_{locale} = structured pedagogical blocks inside one knowledge item
3. Existing data roles:
   - dialogue_turns / normalized_segments = primary surface
   - video = primary surface
   - grammar_note.sections = the closest existing shape to teaching_blocks
   - pattern_card / pattern_builder = structure / output scaffolds
   - example_sentence_refs = example evidence
   - knowledge_refs = example -> knowledge links
   - source_refs = knowledge -> source traceability
4. dict_grammar_mapping.json is a POS / grammar-function mapping table, not a teaching-block system and not a full semantic graph.
5. We want to revisit the course structure around this unit skeleton:
   - Goal / Theme
   - Input
   - Structure
   - Controlled Output
   - Task Output
   - Review
   - Cross-unit Transfer

Please help me:
- redefine the hierarchy and boundaries of this course structure
- decide where dialogue/video/grammar_note/pattern_card/review belong
- explain whether grammar_note.sections should be formally upgraded to teaching_blocks
- turn this into an executable task plan
- point out any conflicts with the current docs if needed

Please stay in architecture-discussion mode first. Do not write implementation code yet.
```
