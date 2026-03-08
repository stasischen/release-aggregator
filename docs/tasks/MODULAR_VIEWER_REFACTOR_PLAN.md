# MODULAR_VIEWER_REFACTOR

## Goal

Refactor the modular viewer so it can consume `lingo-curriculum-source` build artifacts as the primary lesson input, instead of relying on preview-era fixture assumptions.

## Why

Current state:

- viewer can load source-build lessons, but only partially
- `renderers.js` is too large and mixes shell logic, adapter fallback, and learner-facing rendering
- many renderer paths still assume preview-only fields or legacy `*_zh_tw`
- source-build lessons and hand-authored preview fixtures are being treated as if they were equivalent

This creates drift, mixed-language UI, and renderer failures whenever curriculum-source contracts evolve.

## Scope

In scope:

- viewer adapter contract for source-build lessons
- renderer modularization
- i18n-first rendering cleanup
- source-build regression validation
- preview fixture deprecation strategy

Out of scope:

- frontend app integration outside mockup viewer
- curriculum-source lesson content redesign
- schema redesign for lesson authoring

## Target Architecture

```text
curriculum-source build artifact
  -> viewer adapter
    -> normalized unit/node view model
      -> renderer registry by content_form / interaction mode
        -> shell / navigation / learner UI
```

## Key Decisions

1. `lesson_content.v1.json` from curriculum-source build becomes the canonical viewer input for modular lessons.
2. Hand-authored preview fixtures remain only for renderer prototyping or historical comparison.
3. Learner-facing rendering must be i18n-first.
4. Legacy `*_zh_tw` fields may exist only as adapter fallback, not as direct renderer dependencies.
5. Source-build fallback logic belongs in adapter helpers, not spread across renderer bodies.

## Deliverables

1. Source-build adapter contract
2. Split renderer modules
3. i18n-first rendering pass
4. Source-build fixture compatibility for lesson_01~03
5. Preview deprecation note
6. Regression check instructions

## Done Definition

This task is done when:

1. lesson_01~03 source-build fixtures render without crash
2. zh_tw / en locale switch works on learner-facing renderer paths
3. grammar_summary / practice_card / review_card / pattern_lab no longer depend on preview-only assumptions
4. `renderers.js` is no longer the single dumping ground for all rendering logic
5. preview fixtures are explicitly marked as non-source-of-truth
