# AGG-GEN-021 — Agent Work-Order Templates (HTML Mockup Modularization + Scale-out)

## Goal

Provide copy-paste-ready agent work orders and a unified delivery report template for:

- HTML mockup modularization
- renderer registry contracts
- unit blueprint scaffolding
- fixture QA/lint hardening
- multi-unit viewer scale-out

This document is for PM/product to assign work without ad-hoc oral handoff.

## Usage

1. Pick a stream (`M1..M5`) below.
2. Paste the shared preface + stream prompt to the agent.
3. Require the agent to reply using the delivery report template in this file.
4. Validate against the stream checklist.

## Shared Preface (Paste Before Any Stream Prompt)

```text
Task scope is ONLY release-aggregator content-candidate mockup work (AGG-GEN). Do not modify learner app production code.

Repo:
- /Users/ywchen/Dev/lingo/release-aggregator

Baseline references:
- docs/tasks/mockups/agg_gen_017_a1_u04_unit_mockup.html
- docs/tasks/mockups/a1_u04_unit_blueprint_v0.json
- docs/tasks/mockups/unit_blueprint_v0.schema.json
- docs/tasks/AGG_GEN_019_UNIT_MOCKUP_FRONTEND_TRANSFER_PLAN.md
- docs/tasks/AGG_GEN_020_FRONTEND_TRANSFER_TEST_PLAN.md

Rules:
- Make concrete file changes (not only proposals).
- Keep HTML mockup playable.
- Preserve Korean/Chinese toggle, TTS behavior, localStorage progress unless the task explicitly changes them.
- Report using the AGG-GEN delivery template.
```

## Stream Prompts

### M1 — HTML Mockup Modularization

```text
You are Stream M1 (HTML Mockup Modularization).

Goal:
Refactor the single-file playable mockup into a modular viewer structure (shell / state / storage / TTS / renderers) while preserving behavior parity.

Tasks:
1. Split the current viewer into modular files under docs/tasks/mockups/viewer/.
2. Preserve feature parity: bilingual toggle, TTS (Yuna preference), node progress, interaction state, localStorage.
3. Keep fixture path configurable.
4. Add fallback-safe behavior for unsupported content_form/output_mode.

Deliverables:
- modular viewer files
- migration note (single html -> modular viewer)
- parity verification summary
```

### M2 — Renderer Registry Contract

```text
You are Stream M2 (Renderer Registry + Contracts).

Goal:
Define and implement explicit renderer registry contracts for content_form and output_mode to support future unit types and frontend adapter alignment.

Tasks:
1. Add content renderer registry and interaction renderer registry.
2. Define renderer context contract (state, helpers, TTS, bilingual flag, persistence callbacks).
3. Implement fallback renderer(s) with debug-friendly messages.
4. Document supported forms/modes and extension steps.

Deliverables:
- registry modules
- renderer contract doc
- supported matrix (content_form/output_mode/learning_role)
```

### M3 — Unit Blueprint Scaffolding + Authoring Templates

```text
You are Stream M3 (Unit Blueprint Scaffolding + Authoring Templates).

Goal:
Make unit content production scalable via scaffold tools/templates for unit_blueprint_v0 fixtures.

Tasks:
1. Create a scaffold generator for new unit fixtures (e.g. A1-U03 / A1-U06).
2. Generate a standard node skeleton (input/structure/output/review).
3. Create authoring checklist templates (required bilingual fields, QA checks).
4. Keep generated fixtures schema-compatible.

Deliverables:
- scaffold script
- skeleton template fixture(s)
- authoring checklist doc
```

### M4 — Fixture QA / Lint Hardening

```text
You are Stream M4 (Fixture QA and Lint Hardening).

Goal:
Prevent fixture data drift before PM reviews it in the HTML viewer.

Tasks:
1. Extend fixture validation to support multiple fixtures.
2. Add checks for mixed-script corruption, canonical-field drift, unsupported forms/modes, and lightweight payload key checks.
3. Provide a unified mockup-check command/script.
4. Produce clear error output with node_id + path.

Deliverables:
- improved validation scripts
- usage doc (pre-commit / pre-review)
- optional hook snippet
```

### M5 — Multi-Unit Viewer Shell

```text
You are Stream M5 (Multi-Unit Viewer Shell for PM Trial).

Goal:
Allow PM to switch between multiple unit fixtures in the same HTML viewer without code changes.

Tasks:
1. Add fixture index JSON + fixture selector UI.
2. Load selected fixture dynamically.
3. Keep localStorage namespaces isolated per unit.
4. Preserve path-node interactions and TTS behavior after fixture switching.

Deliverables:
- fixture index format + sample
- viewer fixture selector UI
- docs for state/reset behavior across units
```

## Unified Delivery Report Template (Required)

```text
# AGG-GEN Mockup Work Report

## 0) Task Info
- Stream: (M1 / M2 / M3 / M4 / M5)
- Baseline commit:
- This commit:
- Scope summary (1-2 sentences):

## 1) Completed Items (Against Goal)
- [ ] Goal A
- [ ] Goal B
- [ ] Goal C
- Actual completion summary:
  1.
  2.
  3.

## 2) Modified Files
- `/absolute/path/file1`
  - purpose:
- `/absolute/path/file2`
  - purpose:

## 3) User-visible Behavior Changes
- Before:
- After:
- Affected nodes/features:

## 4) Verification (Required)
- JSON/schema checks:
  - command:
  - result:
- mockup smoke checks:
  - command:
  - result:
- manual checks (>=3):
  1.
  2.
  3.

## 5) Regression Checklist (Required)
- [ ] bilingual toggle OK
- [ ] TTS / Korean voice picker OK (if viewer touched)
- [ ] localStorage persistence OK (if viewer touched)
- [ ] chunk_assembly / response_builder / review_retrieval not broken (if interactions touched)
- [ ] unsupported content_form/output_mode fallback does not crash (if registry touched)

## 6) Contract/Data Changes (Important)
- Changed fixture/schema/contract? (yes/no)
- If yes:
  - added fields:
  - deprecated fields:
  - canonical field names:
  - backward-compat strategy:
  - renderer usage locations:

## 7) Known Limits / TODO
- Limit 1:
- Limit 2:
- Next-step suggestions (max 3):
  1.
  2.
  3.

## 8) PM Validation Path (Short)
- Open:
- Click:
- Expected result:
```

## Stream-specific Acceptance Add-ons

### M1 Add-on

- file/folder structure diff (before vs after)
- parity checklist (what was tested)
- remaining single-file legacy pieces (if any)

### M3 Add-on

- scaffold command example
- generated fixture path(s)
- generated fixture validation result
- which fields are required vs placeholder-safe

### M4 Add-on

- new validation rules list (error / warning)
- trigger example for each rule (1-line)
- example failure output

### M5 Add-on

- fixture index format
- localStorage namespace rule
- PM test path for switching units (`A1-U04 -> another -> back`)

## PM Review Notes (Optional)

- If an agent changes fixture/schema, require them to explicitly list:
  - canonical field names
  - fallback aliases (if any)
  - exact renderer functions that consume the new fields
- This prevents "fixture has data but UI never reads it" regressions.
