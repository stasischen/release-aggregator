# MODULAR_LESSON_RUNTIME_IMPLEMENTATION

## Objective

Implement the approved modular lesson runtime production-readiness slice from `MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF`.

This task is limited to frontend runtime wiring and tests. It must not change lesson schema or content pipeline behavior.

## Scope

- Article runtime surface using existing `ArticleContentLayout` and a frontend-local payload mapper.
- Support drawer stabilization with a shared fallback widget and canonical vocab support.
- Video runtime smoke coverage using the existing `UlvVideoRenderer` ownership model.
- Route exposure guard proving production navigation does not route into modular runtime yet.

## Non-Goals

- Do not modify lesson data format.
- Do not touch `content-ko` or `content-pipeline`.
- Do not make modular runtime production-facing from curriculum/path navigation.
- Do not remove Beta/Experimental labels from internal routes.
- Do not implement pattern/usage semantics until canonical ownership is decided.
- Do not collapse domain adapter semantics.

## Acceptance Criteria

- Article modular nodes render real paragraph UI and no longer show `Fail-Soft: Article surface placeholder`.
- Malformed article payloads show a stable fallback instead of crashing.
- Direct canonical `kv.` vocab support can render through the drawer.
- Pattern/usage support surfaces show stable unsupported fallback without "coming soon" copy.
- Modular video smoke test verifies player initialization and support/anchor callback wiring.
- Route guard test confirms production lesson path still uses preview and not modular runtime.
- Targeted tests and `flutter analyze` pass.
