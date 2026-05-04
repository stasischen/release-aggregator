# Codex Task

## Instructions
Implement the task in three narrow slices.

## Slice A
- Inspect video source and v2/staging atomized assets.
- Update the video frontend sync bridge to emit runtime-compatible `content.atoms`.
- Prefer v2 inventory/staging when complete enough; otherwise merge canonical atomized sidecars into the existing runtime package without changing source content.
- Add a gate in frontend asset integrity tests.

## Slice B
- Add atoms to Sentence Bank DTO/domain model.
- Map artifact atoms into frontend domain.
- Add UI affordance to inspect sentence atoms through the existing dictionary content surface.

## Slice C
- Add or update tests for:
  - video runtime assets contain atoms
  - sentence-bank DTO/domain retains atoms
  - sentence-bank UI exposes atom interaction

## Constraints
- Do not change lesson data format.
- Do not modify `content-ko` unless validation proves the source is missing.
- Do not touch `content-pipeline` surfaces unrelated to video frontend sync.
- Keep UI changes compatible with dark mode.

