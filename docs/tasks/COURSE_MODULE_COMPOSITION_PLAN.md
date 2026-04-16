# COURSE_MODULE_COMPOSITION — Content/Interaction/Review Module Plan

## Goal

在既有 scaffold 模組化基礎上，建立可量產且可擴充的三層課程組裝模型：

1. Content module（教什麼）
2. Interaction module（怎麼答）
3. Review module（什麼時候回收、怎麼回收）

本計畫目標不是新增更多 content forms，而是讓同一內容能掛載多種回答方式與複習策略。
同時要維持 `dialogue/video` 作為 input carriers，並讓 knowledge-layer 的 `source_refs` / `teaching_blocks` 只負責溯源與教學結構，不承擔 UI 角色。

## Why This Task Exists

目前系統已有：

- `content_form` registry（內容渲染）
- `output_mode` registry（互動渲染）
- `learning_role` sequencing（教學節奏）

但尚缺：

- 一致的 multi-answer-path contract（同節點多回答模式）
- 明確的 review policy contract（Anki-style schedule and card source）
- completion rules contract（完成判準一致）
- `teaching_blocks` 與 `grammar_note.sections` 的 migration boundary

## Current Foundation (Already Implemented)

- Viewer modular registry:
  - `docs/tasks/mockups/modular/js/renderers.js`
- Unit skeleton and sequencing:
  - `docs/tasks/UNITFAC_002_A1_A2_UNIT_SKELETON_SPEC.md`
- Authoring templates:
  - `docs/tasks/UNITFAC_005_AUTHORING_TEMPLATES.md`
- Quality gate:
  - `scripts/mockup_check.py`

## Three-Layer Model

### 1) Content module

**Definition**
- The pedagogical payload and scenario context.
- 回答前的學習材料與情境資訊。

**Existing contract anchors**
- `candidate_type`
- `content_form`
- `learning_role`

**Examples**
- `dialogue`, `video`, `notice`, `message_thread`, `pattern_card`, `grammar_note`, `functional_phrase_pack`

### 2) Interaction module

**Definition**
- The learner response mechanism and interaction flow.
- 學習者如何產出回答（選擇、組句、打字、口說）。

**Existing contract anchors**
- `output_mode`

**Examples**
- `chunk_assembly`
- `response_builder`
- `frame_fill`
- `pattern_transform`
- `guided`
- `review_retrieval`

### 3) Review module

**Definition**
- Retrieval and spacing strategy; post-unit followup policy.
- 複習回收目標與間隔排程策略。

**Existing contract anchors**
- `review_card` + `review_retrieval`
- `scheduled_followups`

**Missing anchors (to propose)**
- `review_policy`
- `followup_goal_type`
- card source tags / scheduling profile
- `source_refs` indexing flow for knowledge-to-source traceability

## Proposed Contract Additions (Draft for UNITFAC-001 Input)

### interaction_modes

Purpose:
- allow one content node to support multiple answer paths
- e.g., same node offers selection + typing + speaking variants

Draft shape:

```json
{
  "interaction_modes": ["response_builder", "guided_typing", "guided_speaking"],
  "default_interaction_mode": "response_builder"
}
```

### review_policy

Purpose:
- attach Anki-style review strategy without coupling to UI implementation

Draft shape:

```json
{
  "review_policy": {
    "enabled": true,
    "card_types": ["recognition", "recall", "response"],
    "schedule_profile": "same_day_plus_1_plus_3",
    "card_source_refs": ["U05-G1", "U05-P1", "U05-P5"]
  }
}
```

### teaching_blocks

Purpose:
- define the future canonical pedagogical payload for a single knowledge item
- keep `grammar_note.sections` as a transitional shape until migration is ready

Draft shape:

```json
{
  "teaching_blocks": [
    {
      "title": "string",
      "content_md": "string",
      "usage_tag": "form_rule"
    }
  ]
}
```

### completion_rules

Purpose:
- make completion criteria explicit and consistent across guided output nodes

Draft shape:

```json
{
  "completion_rules": {
    "required_modes": ["chunk_assembly", "guided_typing"],
    "min_attempts": 1,
    "pass_policy": "manual_mark_after_required_modes"
  }
}
```

### segmentation_anchor_links

Purpose:
- let course/video sentence chunks expose canonical anchors for dictionary and knowledge lab navigation
- keep the segmentation result separate from the UI, but preserve enough refs for inline click-through

Draft shape:

```json
{
  "segmentation_anchor_links": {
    "enabled": true,
    "anchor_types": ["token", "chunk", "sentence"],
    "link_targets": ["dictionary_atom_ref", "topic_ref", "grammar_ref"],
    "fallback_policy": "show_surface_only_when_no_canonical_target_exists"
  }
}
```

Scope note:
- This belongs under `COURSE_MODULE_COMPOSITION`, not `KNOWLEDGE_LAB_ENRICHMENT` alone.
- Knowledge Lab supplies the canonical refs; course composition decides how the lesson surface exposes them.
- `source_refs` should be treated as one-way knowledge-to-source traceability, not as a UI routing mechanism.

## Node Usage Mapping (Practical)

### Immersion/Input nodes

- Content: high
- Interaction: low or none
- Review: none at node level

Good combinations:
- `dialogue + none`
- `video + none`
- `notice + none`
- `message_thread + none`
- `comprehension_check + none`

### Structure nodes

- Content: medium/high
- Interaction: low/medium (controlled)
- Review: optional source tagging

Good combinations:
- `pattern_card + frame_fill`
- `grammar_note + none`
- `functional_phrase_pack + chunk_assembly`
- `grammar_note.sections` should remain compatible with the future `teaching_blocks` shape during migration

### Drill nodes

- Content: medium
- Interaction: high
- Review: high value as card source

Good combinations:
- `practice_card + chunk_assembly`
- `practice_card + response_builder`
- `practice_card + pattern_transform`

### Task output nodes

- Content: medium (scenario constraints)
- Interaction: high (guided output)
- Review: high (extract mistakes/chunks for later cards)

Good combinations:
- `roleplay_prompt + guided`
- `message_prompt + guided`
- `dialogue + guided`
- `video + guided`

### Review nodes

- Content: medium
- Interaction: medium
- Review: explicit

Good combinations:
- `review_card + review_retrieval`
- `scheduled_followups` with `followup_goal_type`
- review cue source should prefer primary carriers, then example evidence

## Practice Layer Ownership

以下分工用來對齊後續練習設計，不重新定義三層模型，只標記每種練習主要由哪個 task 負責。

### Anki-style review cards

- 主責：`CMOD-004`
- 對應範圍：字卡型複習、間隔排程、卡片來源與 review cue priority
- 對應實體：`review_card`, `review_retrieval`, `scheduled_followups`

### Sentence assembly / typing / response selection

- 主責：`CMOD-003` + `CMOD-012`
- `CMOD-003`：定義 `interaction_modes`，描述同一內容節點可支援的回答路徑
- `CMOD-012`：定義 `pattern_frame + slot_bank`，描述組句、替換、填空這類 controlled substitution drills
- 對應實體：`chunk_assembly`, `response_builder`, `frame_fill`, `pattern_transform`

### Shadowing / repeat / type / sentence practice

- 主責：`CMOD-013`
- 對應範圍：跟讀、重播、打句子、逐句模仿、sentence practice action contract
- 對應實體：`listen`, `repeat`, `shadow`, `type`

### Boundary Reminders

- `CMOD-001` 先定義 Content / Interaction / Review 邊界
- `CMOD-002` 再把 node taxonomy 映射到三層模型
- `CMOD-003` 定義回答路徑，不決定單一練習的最終 UX
- `CMOD-004` 定義 review 元數據，不決定前端卡面樣式
- `CMOD-012` 定義 controlled substitution drills，不取代 `CMOD-003`
- `CMOD-013` 定義 sentence-level actions，不取代 `CMOD-004`

## Work Breakdown

### CMOD-001 — Three-layer canonical model spec

Deliverable:
- `docs/tasks/CMOD_001_THREE_LAYER_MODEL_SPEC.md`

Acceptance:
- clearly defines responsibilities and boundaries between content/interaction/review
- treats `dialogue` and `video` as peer input carriers

### CMOD-002 — Node taxonomy mapping

Deliverable:
- `docs/tasks/CMOD_002_NODE_MAPPING_MATRIX.md`

Acceptance:
- each existing node type has a three-layer mapping and expected role
- mapping distinguishes knowledge payload from support surface and review surface

### CMOD-003 — interaction_modes proposal

Deliverable:
- contract note for `interaction_modes` / `default_interaction_mode`

Acceptance:
- supports MCQ/assembly/typing/speaking/transform variants without adding new content_form
- explicitly covers selection, assembly, typing, and speaking answer paths

### CMOD-004 — review_policy proposal

Deliverable:
- contract note for `review_policy` and card source metadata

Acceptance:
- supports same-day/+1/+3 scheduling semantics
- review cue source priority is documented without coupling to implementation
- explicitly covers Anki-style review cards and followup spacing policy

### CMOD-005 — completion_rules proposal

Deliverable:
- contract note for completion rules metadata

Acceptance:
- guided output completion no longer ambiguous

### CMOD-006 — Contract mismatch cleanup

Deliverable:
- patch list and fixes for mismatches across spec/template/checker

Known mismatch examples:
- `repair_practice` mention vs checker allowlist alignment
- followup semantics consistency
- mockup-check command path references
- `source_refs` naming consistency across knowledge-layer docs
- `grammar_note.sections` versus `teaching_blocks` transitional wording

### CMOD-007 — Template integration

Deliverable:
- update `UNITFAC_005_AUTHORING_TEMPLATES.md`

Acceptance:
- authors see explicit sections for content/interaction/review metadata

### CMOD-008 — Checker integration (warning-first)

Deliverable:
- update `scripts/mockup_check.py` with warning-first checks for new metadata

Acceptance:
- no regressions to current PR fixtures

### CMOD-009 — A1-U05 pilot metadata application

Deliverable:
- apply selected metadata to `a1_u05_unit_blueprint_v0.json`

Acceptance:
- fixture remains playable and checkable
- pilot demonstrates `dialogue/video` as carriers and `grammar_note.sections` as transitional structure

### CMOD-010 — Freeze recommendation

Deliverable:
- `docs/tasks/CMOD_010_FREEZE_RECOMMENDATION.md`

Acceptance:
- clear include/defer list for UNITFAC-001 contract freeze
- explicitly separates frozen carrier/structure boundaries from deferred migration details

## Recommended Execution Order

1. `CMOD-001` + `CMOD-002`
2. `CMOD-003` + `CMOD-004` + `CMOD-005`
3. `CMOD-006`
4. `CMOD-007` + `CMOD-008`
5. `CMOD-009`
6. `CMOD-010`

## Definition of Done

This task can be closed when:

- three-layer model is explicit in docs and templates
- checker can detect missing modular metadata (warning-first)
- at least one PR-ready unit demonstrates metadata usage
- UNITFAC-001 has a clear include/defer recommendation for freeze
