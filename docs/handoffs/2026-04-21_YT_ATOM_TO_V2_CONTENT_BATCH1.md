# Handoff: YouTube Atom to V2 Content Conversion - Batch 1

- **Date**: 2026-04-21
- **Task ID**: `YT_ATOM_TO_V2_CONTENT`
- **Target Machine**: `home`
- **Status**: `ready_for_worker`

## Purpose
Prepare a small, reproducible pilot batch for YouTube atom conversion from V5 to Content V2 (`content_item.v1`) so a worker machine can execute without relying on the current machine's memory-heavy context.

## Current Decision
- Use `eF65dUUDcEQ` as the pilot video.
- Convert only the first 20 turns in Batch 1.
- Recreate the pilot output from source instead of trusting the existing staging artifact.

## Scope
### In scope
- Finalize `content-ko/.agent/skills/yt-atom-v2-conversion/SKILL.md`.
- Generate Batch 1 pilot output from V5 source.
- Run coverage verification.
- Record orphans in a review ledger if any are found.

### Out of scope
- Full-video conversion.
- Mass conversion of the remaining videos.
- Frontend changes.

## Spec
### Input
- `content-ko/content/core/video_atoms/eF65dUUDcEQ_atoms.json`

### Output
- `content-ko/content_v2/staging/content_assets/video/eF65dUUDcEQ_pilot.json`

### Conversion rules
- Preserve V5 Eojeol-based blocks as V2 atom blocks.
- If an atom has a joined ID such as `joined_id_a+joined_id_b`, keep it as one atom block and allow the `+` syntax through the coverage gate.
- Keep the pilot limited to turns 1-20.
- Keep output reproducible by regenerating from source rather than editing the staging file by hand.

## Batch 1 Execution Steps
1. Create or finalize the conversion skill at `content-ko/.agent/skills/yt-atom-v2-conversion/SKILL.md`.
2. Load `content-ko/content/core/video_atoms/eF65dUUDcEQ_atoms.json`.
3. Convert turns 1-20 into the V2 staging file.
4. Run `scripts/ops/check_atom_coverage.py` on the result.
5. If any orphans exist, classify them in a manual review ledger.

## Hard Gates
- Coverage check must pass, or return a complete orphan audit.
- Output must contain only the first 20 turns.
- Output must remain within the staging path above.
- Do not change unrelated content files.

## Review Notes
- POS differences between V5 and V2 are expected and must be resolved explicitly.
- Canonical endings and contractions may need explicit normalization decisions.
- Keep the worker batch small enough to avoid hallucination drift.

## Worker Prompt
```text
You are the worker for YT_ATOM_TO_V2_CONTENT Batch 1.

Read:
1. release-aggregator/docs/handoffs/2026-04-21_YT_ATOM_TO_V2_CONTENT_BATCH1.md
2. release-aggregator/docs/tasks/YT_ATOM_TO_V2_CONTENT_TASKS.json
3. release-aggregator/docs/tasks/MACHINE_STATUS.md
4. release-aggregator/docs/tasks/YT_ATOM_TO_V2_CONTENT_PLAN.md

Execute only Batch 1:
- source: content-ko/content/core/video_atoms/eF65dUUDcEQ_atoms.json
- output: content-ko/content_v2/staging/content_assets/video/eF65dUUDcEQ_pilot.json
- turns: 1-20 only

Stop if coverage fails. If orphans exist, classify them and report them.
Do not expand to the full video.
```
