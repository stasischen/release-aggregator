# AGG-GEN-018 Schema/Brief Extension Spec (Adapter Contract First)

Status: Draft v0.1  
Scope: Stabilize schema/brief metadata and mockup fixture contract so frontend can build adapters without binding directly to generation/review internals.

## 1. Why This Spec Exists

`AGG-GEN-017` and `AGG-GEN-019` proved the unit sequencing direction (`immersion -> structure -> output -> review`) and mockup interaction diversity.

Before Flutter implementation proceeds, `AGG-GEN-018` must define an adapter-facing contract that is:

- stable enough for renderer switching (`content_form`, `output_mode`)
- explicit enough for sequencing/unlock logic (`depends_on`, optionality)
- explicit enough for cross-surface integration (lesson / grammar / dictionary links)
- decoupled from review-console-only metadata

This spec does **not** define frontend UI design. It defines data contract expectations for adapter authors.

## 2. Adapter Contract Principles (v1 Target)

### 2.1 Stable Switch Keys (Required)

The frontend adapter may switch renderer/interaction by these canonical keys:

- `candidate_type`
- `content_form`
- `learning_role`
- `output_mode`

These keys must be treated as schema-level contract fields, not freeform ad-hoc labels in briefs.

### 2.2 Content vs Interaction Separation (Required)

Each node should support a two-layer rendering model:

- content layer: determined primarily by `content_form`
- interaction layer: determined primarily by `output_mode`

This allows one `content_form` (e.g. `practice_card`) to host multiple interaction modes (`chunk_assembly`, `response_builder`, `guided`).

### 2.3 Sequence Logic Must Be Explicit (Recommended in v0, Required in v1)

Adapters should not infer unlock logic only from array position.

Node-level sequencing metadata should support:

- `depends_on_ids`
- `is_optional`
- `unlock_behavior` (default `after_dependencies`)

### 2.4 Cross-Surface Links Must Be Explicit (Recommended in v0, Required for integrated units)

Adapters should not scrape titles/summaries to discover integrations.

Node-level resource linking should support:

- `lesson_ids`
- `grammar_note_ids`
- `dictionary_terms`
- optional route/tool links (for mockup-to-frontend mapping)

### 2.5 Review/QA Metadata Separation (Required)

Review-console fields (scores, reviewer annotations, agent judgments, moderation notes) may exist in canonical candidate data, but must remain outside adapter-facing node view-model defaults.

Adapter-safe fields should be clearly marked or grouped (`adapter_hints`, `resource_links`, `sequencing`).

## 3. AGG-GEN-018 Schema/Brief Requirements

### 3.1 Candidate Schema / Metadata Extension (Canonical)

Required / strongly recommended fields (already introduced by `AGG-GEN-017`, now contract-locked):

- `target_language`
- `learner_locale_source`
- `content_form`
- `learning_role`
- `skill_focus`
- `output_mode`

Recommended additions for adapter-first sequencing:

- `depends_on_candidate_ids`
- `is_optional`
- `unlock_behavior`

Recommended additions for integration:

- `resource_links.lesson_ids[]`
- `resource_links.grammar_note_ids[]`
- `resource_links.dictionary_terms[]`

Recommended additions for frontend adapter hints (non-UI-design):

- `adapter_hints.entry_surface` (e.g. `unit_flow`, `lesson_runtime`, `tool_hub`)
- `adapter_hints.completion_mode` (e.g. `view_complete`, `interaction_complete`, `manual_mark`)
- `adapter_hints.interaction_renderer_key` (optional explicit override; default from `output_mode`)

Recommended additions for review cadence (already planned):

- `revisit_after_units`
- `review_window_days`
- `recycle_from_units`

### 3.2 Generation Brief Extension (Contract-Oriented)

Generation briefs for unit sequencing should specify:

- allowed enum values for `candidate_type`, `content_form`, `learning_role`, `output_mode`
- minimum payload completeness rules per `content_form`
- whether sequence dependencies must be explicit (`depends_on_candidate_ids`)
- required resource linking coverage (e.g. output nodes must link grammar or dictionary support where applicable)
- locale display strategy (`learner_locale_source` + future localization targets)

### 3.3 Versioning / Churn Rules

- Do not repurpose existing enum values.
- New enum values require:
  - schema update
  - mock fixture example
  - adapter fallback behavior note
- `id` must remain stable within a published unit blueprint version.
- If payload semantics change materially, bump payload/schema version instead of silently changing shape.

## 4. Unit Blueprint v0 Contract Alignment (Mockup Fixture Layer)

`../mockups/unit_blueprint_v0.schema.json` should expose optional adapter-facing metadata blocks so PM mockups and frontend adapter tests can converge before canonical schema fully lands.

Recommended optional blocks per node:

- `sequencing`
- `resource_links`
- `adapter_hints`

These blocks are for mockup/frontend transfer stability and should stay lightweight.

## 5. Out of Scope

- final Flutter UI layout
- scoring engine / automated evaluation
- review-console workflow fields
- backend persistence API

## 6. Acceptance Addendum for AGG-GEN-018

AGG-GEN-018 should be considered ready for frontend adapter work when:

- schema/brief docs explicitly define adapter-safe switch keys and sequencing/linking metadata
- `unit_blueprint_v0` schema includes optional adapter-facing blocks
- at least one unit fixture demonstrates these blocks
- frontend transfer plan (`AGG-GEN-019`) can reference a stable contract without scraping mockup HTML behavior
