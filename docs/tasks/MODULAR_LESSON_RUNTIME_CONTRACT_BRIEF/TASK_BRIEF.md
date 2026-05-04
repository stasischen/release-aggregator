# MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF

## Objective

Define the decision surface for modular lesson runtime production readiness before any article/support/video renderer implementation.

This task is brief-first. It must collect options, risks, route exposure, and smoke-test requirements without changing lesson data format or frontend code.

## Context

Previous task:

- `MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF` completed code-only UI copy cleanup.
- Remaining blockers are contract/product decisions:
  - Article renderer behavior is not final.
  - Support panel ownership is not final.
  - Video renderer finalization must not be inferred from optional builder behavior.
  - Preview/testbed route exposure needs product routing review.

## Required Decisions

1. Article surface minimum production behavior
   - Pure article read view
   - Paragraph/chunk-level interaction
   - Dictionary/grammar overlay behavior
   - Empty/malformed article fallback policy

2. Support panel ownership
   - Pattern support
   - Usage support
   - Vocab support
   - Whether to reuse Knowledge Lab / Dictionary / Sentence Bank components or build lesson-local renderers

3. Video runtime finalization
   - Required builder/data dependencies
   - Fallback policy when video data is missing
   - Whether video runtime should be route-driven, artifact-driven, or injected via runtime builders

4. Fail-soft policy
   - Which states can be visible in development/testbed routes
   - Which states must be blocked by validation before production route exposure

5. Route exposure
   - Which modular routes are user-facing
   - Which routes are preview/internal/testbed only
   - Whether Beta/Experimental labels should remain or be hidden behind dev navigation

6. Smoke gate
   - Minimal tests required before article/support/video runtime surfaces are treated as production-ready

## Non-Goals

- Do not modify lesson schema or data format.
- Do not edit frontend code.
- Do not touch `content-ko` or `content-pipeline`.
- Do not collapse domain adapter semantics into one generic adapter.
- Do not remove compatibility or cache behavior such as mapping_v2 origin cache.

## Output Contract

The next accepted output should be a reviewed brief with:

- Decision matrix
- Recommended contract option per surface
- Deferred items with reasons
- Code task split after decisions
- Smoke-test matrix
