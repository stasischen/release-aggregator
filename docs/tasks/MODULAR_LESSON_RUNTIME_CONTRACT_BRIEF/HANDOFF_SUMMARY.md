# MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF Handoff

## Status

Contract brief reviewed. Gemini inventory has been converted into accepted implementation boundaries in `CONTRACT_DECISION.md`.

## Current Boundary

This was a brief-first task. The next step may be implementation, but only within the approved boundaries in `CONTRACT_DECISION.md`.

## Inputs

- `MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF` completed UI copy cleanup.
- Remaining work is article/support/video runtime contract definition.

## Expected Next Step

Create implementation tasks for:

1. Article runtime surface using `ArticleContentLayout` plus local payload mapper.
2. Support drawer stabilization and direct canonical vocab support.
3. Video runtime smoke gate.
4. Route exposure guard.

## Do Not Do Yet

- Do not implement article renderer.
- Do not implement support panel renderers.
- Do not finalize video renderer assumptions.
- Do not remove Beta/Experimental labels unless route exposure is decided.
- Do not change lesson format.

## Accepted Decisions

- Article uses existing `ArticleContentLayout` with local frontend mapper; no schema change.
- Support remains drawer-based and reuses existing Learning Library / Knowledge Lab side-panel renderers.
- Video remains owned by `UlvVideoRenderer`; no external route-driven playback.
- Modular routes remain internal/pilot until article/support/video smoke gates pass.
