# PRG-005: Production Release Gating - Pilot 1 (Strict Reality)

Establish a small pilot allowlist slice using **exactly-matched** content from the current staging candidate. This pilot explicitly avoids cross-level shims (e.g. mapping A1 to A2) and focuses on the "clean" path where manifest entries perfectly align with staging assets.

## User Review Required

> [!IMPORTANT]
> **Chosen Pilot Scope**:
> I have selected **2 Video Lessons** from the `bonus_video` unit.
> 1. `ko_v1_vlog_IGEj-oDKyw8_conv_store` (Unit: `bonus_video`)
> 2. `ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson` (Unit: `bonus_video`)

> **Rationale**: These lessons represent the "perfect match" reality. Both are present in `prd.release_manifest.seed.json` and `content-pipeline/staging/ko/core/video/` with matching IDs and types.
>
> **Exclusions**:
> - **A1 Dialogues**: Excluded because they are currently missing in staging.
> - **A2 Dialogues**: `A2-01.json` exists in staging, but no corresponding `ko_l2_dialogue_a2_01` exists in the current seeded manifest (it likely starts at A2-05). To avoid "guessing" or "shimming," I am excluding dialogue from the first pilot run unless an exact mapping is established.

## Proposed Changes

### [Release Aggregator]


#### [NEW] [pilot_allowlist.json](file:///e:/Githubs/lingo/release-aggregator/staging/prg_pilot/pilot_allowlist.json)

- Machine-readable manifest containing only the 2 selected video lessons.

#### [MODIFY] [PRODUCTION_RELEASE_GATING_TASKS.json](file:///e:/Githubs/lingo/release-aggregator/docs/tasks/PRODUCTION_RELEASE_GATING_TASKS.json)

- Update `PRG-005` to `in_progress`.
---

## Verification Plan

### Automated Tests

- Run `assembler_prototype.py --release-manifest staging/prg_pilot/pilot_allowlist.json --candidate-source ... --planning`.
- Run in `--strict` mode.
- **Success Criteria**: `strict mode` passes with 0 gaps for the 2 selected lessons.
