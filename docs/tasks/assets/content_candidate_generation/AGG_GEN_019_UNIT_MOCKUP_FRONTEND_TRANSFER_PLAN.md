# AGG-GEN-019 Unit Mockup + Frontend Transfer Plan (A1-U04)

Status: Draft v1
Scope: mock experience for course sequencing + migration planning to existing Flutter frontend (`lingo-frontend-web`) without committing to UI redesign.

## 1. Goal

Provide a tangible mockup that PM/product can "experience" to validate unit sequencing and output-heavy progression before implementing full frontend support.

This task is not a frontend redesign. It is a transition planning artifact.

## 2. Deliverables

- Mockup data: `../mockups/agg_gen_017_a1_u04_unit_mockup_data.json`
- Mockup viewer: `../mockups/agg_gen_017_a1_u04_unit_mockup.html`
- This plan doc (mapping + migration notes)

## 3. How To Experience the Mockup

### Option A (preferred)

Serve `docs/tasks/mockups/` with a local static server, then open:
- `agg_gen_017_a1_u04_unit_mockup.html`

Examples:
- `python3 -m http.server` (from `../mockups/`)
- any local static preview extension/server

### Option B

Open the HTML file directly. If browser blocks local `fetch()` under `file://`, use Option A.

## 4. What the Mockup Validates (and What It Does Not)

### Validates

- unit sequencing rhythm (`immersion -> structure -> output -> review`)
- output ratio feel (time + node count)
- `content_form` diversity (not only dialogue)
- path-node role in controlled output / retrieval
- cross-unit transfer scheduling visibility

### Does Not Validate

- production audio/video UX
- final frontend navigation
- response scoring engine behavior
- backend persistence/API

## 5. Frontend Transfer Strategy (Flutter-Friendly)

Goal: minimize risk when porting this structure into the existing Flutter frontend.

### 5.1 Keep Existing Page Shell, Add "Node Renderer"

Do not start with a new course page. Start by adding a render layer that can display a `unit_blueprint` / `path_node` sequence inside the current lesson flow shell.

Suggested approach:
- Keep existing route/screen structure
- Add a new sequence renderer widget:
  - `UnitNodeSequenceView`
- Render each node by `candidate_type` + `content_form` + `learning_role`

### 5.2 Use Adapter Layer (Do not bind UI directly to generation schema)

Recommended mapping:

- Canonical candidate / unit blueprint (aggregator-oriented)
  -> `FrontendLessonNode` / `FrontendPracticeNode` (frontend view model)

Reason:
- front-end can evolve independently
- review/generation metadata can stay in `metadata`
- avoids leaking QA fields into UI widgets

### 5.3 Progressive Support Order (Implementation)

Implement rendering support in this order:

1. `dialogue` lesson
2. `notice` lesson
3. `message_thread` lesson
4. `comparison_card` lesson
5. `grammar_note` (pattern-first)
6. `path_node` controlled output (`chunk_assembly`, `response_builder`)
7. `path_node` guided output (speaking/writing)
8. `path_node` review retrieval

This order matches A1-U04 mockup and gives a realistic end-to-end unit demo early.

### 5.4 State Model Requirements (for Flutter)

Minimum runtime state to support this mockup:

- current node index
- per-node completion state
- output attempts (draft text / selected chunks)
- revealed hints state
- review retrieval attempts

Optional later:
- scoring feedback
- spaced review scheduling sync
- analytics events

## 6. Data Contract Suggestions for Frontend Adapter

Minimal front-end view-model fields per node:

- `node_id`
- `node_kind` (`lesson` | `grammar_note` | `dictionary_pack` | `practice`)
- `content_form`
- `learning_role`
- `title`
- `summary_zh_tw`
- `duration_min`
- `sample_content` (typed payload)
- `expected_output_hint`
- `interaction_mode` (`read`, `listen`, `chunk_assembly`, `response_builder`, `guided_write`, etc.)

Keep these out of the UI model (but preserve in raw):
- QA flags
- generation scores
- agent recommendation
- review-only annotations

## 7. Migration Risks and Mitigations

1. Risk: front-end assumes "lesson = dialogue"
- Mitigation: introduce `content_form` switch in renderer and fallback placeholder UI.

2. Risk: front-end assumes linear content without review nodes
- Mitigation: treat `learning_role` as a first-class sequencing hint.

3. Risk: output nodes require interaction types not present in current widgets
- Mitigation: start with text-based mock interactions (`chunk_assembly`, `response_builder`) before audio capture.

4. Risk: schema churn breaks UI iteration
- Mitigation: lock an adapter interface and version fixtures (`v0`, `v1`).

## 8. Gemini Work Split (High-level)

This task should be split with `AGG-GEN-020` test plan:

- Stream A: data adapter + fixtures
- Stream B: renderer widgets + fallback forms
- Stream C: path-node interactions (chunk/response/guided)
- Stream D: integration tests + golden snapshots

## 9. Exit Criteria for AGG-GEN-019

- PM can open the mockup and inspect one full unit sequence
- team can discuss sequencing quality using a shared artifact
- frontend transfer strategy is documented (adapter-first, non-redesign)
- implementation order for Flutter is explicit
