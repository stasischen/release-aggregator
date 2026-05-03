# GPT Decision

Task: `FRONTEND_V2_INTAKE_COMPLETION`
Date: 2026-05-04
Status: approved

## Decision

Approved with a narrow implementation scope.

Use a minimal study-owned `FrontendContentContractResolver` for the next slice. The resolver should sit in the study data layer, not global core, because the immediate problem is study lesson discovery/body path resolution. Dictionary, grammar, and learning-library already have their own specialized contracts and should not be pulled into a broad global facade yet.

## Inputs

- `TASK_BRIEF.md`
- `EXECUTION_PLAN.md`
- `DEEPSEEK_INVENTORY.md`
- Frontend dictionary mapping v2 commit: `lingo-frontend-web@5abcc31c`

## Approved Contract

Create a resolver under:

- `lingo-frontend-web/lib/features/study/data/repositories/frontend_content_contract_resolver.dart`

The resolver should own:

- loading `assets/content/production/manifest.json`
- resolving `files.study_discovery`
- resolving lesson metadata by `lesson_id` / `level_id`
- resolving lesson body path from `manifest.lessons[].path`
- exposing compatibility fallback only when a legacy lesson has no manifest path

## Approved Rules

1. `manifest.lessons[].path` is authoritative for lesson body loading when present.
2. `files.study_discovery` is authoritative for study catalog/discovery.
3. `modular_lessons.json` must not be an independent truth source; it can only be a compatibility input if listed by manifest or explicitly allowed.
4. `StudyContentLocator` should move behind the resolver as fallback only.
5. No Flutter runtime should read raw `content-ko/content_v2` paths.
6. Dictionary mapping v2 candidate intake is accepted as current dictionary baseline unless dictionary review thread changes contract.
7. Grammar and learning-library should remain unchanged in the next slice.

## Required API Shape

Keep the first implementation intentionally small:

```dart
class FrontendContentContractResolver {
  Future<Map<String, dynamic>> loadManifest();
  Future<String?> resolveStudyDiscoveryPath();
  Future<Map<String, dynamic>?> findLessonEntry(String lessonId);
  Future<String?> resolveLessonBodyPath(String lessonId);
}
```

Notes:

- `findLessonEntry()` should match both `lesson_id` and `level_id`.
- `resolveLessonBodyPath()` should return `manifest.lessons[].path` first.
- Any fallback path must be explicitly marked compatibility behavior.
- Do not add dictionary/grammar/learning-library methods to this resolver in this slice.

## Fallback Policy

Allowed:

- For video/core legacy lessons with no manifest `path`, call `StudyContentLocator.corePath()` inside the resolver only.
- For existing i18n overlay behavior, keep `I18nOverlayService` unchanged in this slice unless tests force a small compatibility adjustment.

Not allowed:

- New UI-facing repositories should not call `StudyContentLocator` directly.
- Do not read `content-ko/content_v2` raw paths from Flutter runtime.
- Do not use `modular_lessons.json` as an independent registry in new code.

## Rejected Alternatives

### Keep fixing `StudyContentLocator`

Rejected because it preserves a path-builder as the public mental model.

### Wait for PRG promotion first

Rejected because frontend can already remove its own runtime coupling while PRG output contract is finalized separately.

## Resolved Open Questions

1. Resolver location: `lib/features/study/data/repositories/`.
2. First output shape: path strings plus parsed manifest entry maps; typed model can follow after tests stabilize.
3. Legacy i18n overlay: keep in `I18nOverlayService` for this slice.
4. Fixture target: choose one manifest-listed Korean production lesson that has a valid `path`; prefer a small grammar-heavy lesson already present in production assets.

## Codex Implementation Instruction

For `frontend-v2-intake-03`, implement the resolver and migrate only study discovery/body path resolution call sites that are necessary to prove the boundary:

1. Add `FrontendContentContractResolver`.
2. Update `LessonRegistryRepository` to use it for manifest, study discovery path, and lesson body path.
3. Stop using `modular_lessons.json` as an independent truth source in `LessonRegistryRepository`; only use manifest/catalog entries in this slice.
4. Add targeted tests for manifest path precedence and fallback behavior.
5. Run targeted Flutter tests and `flutter analyze`.
