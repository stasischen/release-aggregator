# MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF

## Objective

Separate small code-only modular runtime UI cleanup from lesson-runtime product decisions.

This task follows the frontend UI completeness QA finding that the modular lesson runtime still exposes pilot/placeholder behavior. It does not redefine the lesson data format.

## Scope

- Localize and centralize modular runtime summary/navigation UI copy that is currently hardcoded in widgets.
- Capture a product brief for lesson runtime placeholders that require contract decisions before implementation.
- Keep preview/testbed pilot labels deferred unless they are exposed through a production route.

## Non-Goals

- Do not modify lesson data format or schema.
- Do not touch `content-ko` or `content-pipeline`.
- Do not remove compatibility paths or mapping caches.
- Do not unify domain adapter semantics.
- Do not implement article/support/video renderer contracts without a separate brief approval.

## Decisions Needed Before Runtime Implementation

1. What is the minimum production behavior for `content_form: article`?
2. Should support tabs for pattern/usage/vocab reuse Knowledge Lab, Dictionary, and Sentence Bank components, or use lesson-local renderers?
3. Which fail-soft states are acceptable for malformed data, and which must never be visible in product paths?
4. Which modular preview/testbed routes are internal-only, and which routes can be reached from user-facing navigation?
5. What smoke tests must gate production exposure of article/support/video runtime surfaces?

## Current Disposition

- Fix now: modular summary/footer localized copy.
- Brief first: article surface, support surface expansion, video renderer finalization.
- Deferred: preview/testbed Beta/Experimental labels while routes remain internal.
