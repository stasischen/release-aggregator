# GPT Decision Request

Task: `FRONTEND_V2_INTAKE_COMPLETION`
Date: 2026-05-04
Status: pending GPT 5.5 decision

## Decision Needed

Approve or revise the next implementation slice for frontend study v2 intake.

## Inputs

- `TASK_BRIEF.md`
- `EXECUTION_PLAN.md`
- `DEEPSEEK_INVENTORY.md`
- Frontend dictionary mapping v2 commit: `lingo-frontend-web@5abcc31c`

## Proposed Decision

Use a minimal `FrontendContentContractResolver` as the next frontend abstraction.

The resolver should own:

- loading `assets/content/production/manifest.json`
- resolving `files.study_discovery`
- resolving lesson metadata by `lesson_id` / `level_id`
- resolving lesson body path from `manifest.lessons[].path`
- exposing compatibility fallback only when a legacy lesson has no manifest path

## Proposed Rules

1. `manifest.lessons[].path` is authoritative for lesson body loading when present.
2. `files.study_discovery` is authoritative for study catalog/discovery.
3. `modular_lessons.json` must not be an independent truth source; it can only be a compatibility input if listed by manifest or explicitly allowed.
4. `StudyContentLocator` should move behind the resolver as fallback only.
5. No Flutter runtime should read raw `content-ko/content_v2` paths.
6. Dictionary mapping v2 candidate intake is accepted as current dictionary baseline unless dictionary review thread changes contract.
7. Grammar and learning-library should remain unchanged in the next slice.

## Rejected Alternatives

### Keep fixing `StudyContentLocator`

Rejected because it preserves a path-builder as the public mental model.

### Wait for PRG promotion first

Rejected because frontend can already remove its own runtime coupling while PRG output contract is finalized separately.

## Open Questions

1. Should the resolver live under `lib/core/services/` or `lib/features/study/data/repositories/`?
2. Should the resolver output a typed model now, or first return path strings plus parsed metadata?
3. Should legacy i18n overlay path resolution stay in `I18nOverlayService` for now?
4. What real Korean v2 fixture should become the stable validation target?

## Required GPT Output

- Approved / revise / reject.
- Final resolver ownership location.
- Required model/API shape for the next Codex slice.
- Explicit fallback policy for legacy video/core/i18n lessons.
- Codex implementation instruction for `frontend-v2-intake-03`.
