# Source Of Truth Policy

## Purpose

The repos currently contain mixed generations of content:

- raw `content_v2` inventory
- legacy `content/core`
- legacy `content/i18n`
- generated `content-pipeline/dist`
- frontend runtime assets
- old frontend package aliases
- test fixtures and seed mocks

This policy prevents frontend and pipeline work from accidentally reading old data or old
schemas while debugging.

## Golden Rule

Runtime code must read only promoted/exported runtime artifacts.

Legacy and raw inventory paths are allowed only in pipeline/export code, and only behind a
named bridge with a retirement condition.

## Runtime Truth Table

| Domain | Frontend Runtime Source Of Truth | May Read Legacy Directly? | Notes |
| :--- | :--- | :--- | :--- |
| Dictionary runtime | `assets/content/production/packages/{lang}/packages manifest -> core/i18n/resolver modules` | No | Current package layout still needs resolver-module hardening. |
| Video runtime | `assets/content/production/packages/{lang}/video/core` plus declared i18n overlays | No | Frontend must not inspect `content_v2` or legacy `content/i18n`. |
| Learning Library | `assets/artifacts/learning_library/{lang}/library_manifest.json` | No | Do not use stale `packages/{lang}/manifest.json` learning_library aliases as truth. |
| Knowledge Bank UI | composed Learning Library snapshot | No | Screens should not merge raw core/i18n themselves. |
| Sentence Evidence UI | composed Learning Library snapshot | No | `shared_bank` is temporary until artifact metadata models it. |
| Lesson/modular runtime | current lesson package contract only | No | Lesson schema is not final; do not infer final contract from pilot runtime. |

## Pipeline Truth Table

| Pipeline Stage | Allowed Source | Legacy Allowed? | Gate |
| :--- | :--- | :--- | :--- |
| v2 dictionary export | `content_v2/inventory/dictionary/{version}` | Only for explicit bridge patches | dictionary output shape test |
| Learning Library core export | `content_v2/inventory/learning_library` and `content_v2/inventory/example_sentence` | No for core | referential integrity |
| Learning Library i18n export | canonical v2 i18n sidecar, then named legacy bridge | Yes, temporary | i18n coverage floor |
| Video runtime sync | canonical atomized video sidecars/runtime packages | No hidden fallback | atom coverage gate |

## Legacy Quarantine Rules

Legacy paths are not deleted yet, but they must be quarantined by usage rules.

Allowed:

- `content-pipeline` may read legacy paths only through named bridge functions.
- A bridge must have a task id, test coverage, and retirement condition.
- Debug scripts may inspect legacy paths if the output is a report, not a runtime artifact.

Disallowed:

- Frontend repositories importing or reading `content-ko/content/...` directly.
- Frontend runtime building asset paths from legacy folder conventions.
- Tests passing because seed/mock data hides production artifact failures.
- Treating `assets/content/production/packages/ko/manifest.json` Learning Library aliases
  as the Learning Library source of truth.
- Adding new `*_index.json` aliases except canonical `sources_index.json`.
- Reintroducing per-word dictionary runtime files under frontend assets.

## Required Lookup Order For Agents

When debugging missing text, atoms, routes, or dictionary results, use this order:

1. Check the runtime artifact actually consumed by frontend.
2. Check the runtime manifest that declares that artifact.
3. Check frontend loader/composer tests.
4. Check pipeline output in `content-pipeline/dist`.
5. Check pipeline source selection and bridge functions.
6. Only then inspect legacy `content/core` or `content/i18n` as source material.

Do not start by grepping legacy source files and assuming frontend sees them.

## Gate Recommendations

### Frontend

- A test that fails if Learning Library runtime loads stale `*_index.json` aliases.
- A test that fails if dictionary runtime packages include per-word atom file trees.
- A test that uses production assets for representative video dictionary lookup.
- A test that verifies Learning Library i18n baseline coverage from synced assets.

### Pipeline

- A test that fails if `dist/ko/core/dictionary/atoms` is emitted.
- A test that fails if Learning Library i18n coverage drops below accepted baseline.
- A test that lists every legacy bridge read with task id and owner.
- A manifest validation that declared module paths exist and match the frontend contract.

## Migration Target

Eventually, each domain should have exactly one exported manifest as the source of truth:

```text
content-ko raw/staging
  -> content-pipeline export
    -> production package/artifact manifest
      -> frontend loader/composer
        -> UI
```

No frontend screen should know whether a record originated from legacy, staging, v2
inventory, or manual bridge. That provenance belongs in metadata and validation reports,
not UI loader logic.
