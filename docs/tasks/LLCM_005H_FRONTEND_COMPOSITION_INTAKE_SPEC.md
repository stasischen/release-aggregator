# LLCM-005h - Frontend Composition Intake Spec

## Goal

Define the frontend intake contract for the new Learning Library vNext packaging model:

- load `target-language core` first
- load the selected `support-language i18n` pack second
- compose a runtime snapshot in the repository/data layer

This is a frontend contract document. It does not change the pipeline output contract defined by `LLCM-005g`.

## Current State

The frontend still behaves like a single snapshot consumer.

Observed shape:

- `LearningLibraryContentRepository` selects either seed or artifact data source
- `LearningLibraryLookup` works over one `LearningLibraryDataSnapshot`
- `SourceDetailScreen` reads from the snapshot and renders directly from lookup results
- `ArtifactLearningLibraryDataSource` currently loads one bundle-shaped artifact set into one snapshot

That means the frontend is not yet composed as `core + i18n` at intake time.

## Desired Intake Flow

```text
target core pack
  -> composition repository
    -> selected support-language i18n pack
      -> composed LearningLibraryDataSnapshot
        -> lookup/service layer
          -> UI screens
```

Required order:

1. Load target core pack
2. Load selected support-language i18n pack
3. Compose them into a single runtime snapshot
4. Expose only the composed snapshot to screens and lookup helpers

## Responsibility Split

### Repository

The repository is the composition boundary.

Responsibilities:

- choose source mode
- load the core pack
- load the selected i18n pack
- compose them into the runtime snapshot
- fail clearly if either pack is missing or incompatible

### Data Source

The data source should be a pack loader, not a UI concern.

Responsibilities:

- load pack files from the agreed asset paths
- parse the pack schema
- return typed pack DTOs or an equivalent normalized model

The data source should not decide how the UI merges fields.

### Mapper / Composer

The mapper/composer owns field ownership rules.

Responsibilities:

- apply core/i18n field resolution
- merge localized display fields into the runtime snapshot
- preserve canonical ids and refs from core
- reject field leakage across the `core` / `i18n` boundary

### UI Screens

UI screens must not perform merge logic.

Rules:

- screens may read the composed snapshot
- screens may render fallback text
- screens may not join core and i18n packs themselves
- screens may not become a second mapper layer

## Field Ownership Boundary

### Core Owns

- canonical ids
- source type
- media metadata
- sentence surface
- refs and graph relationships
- knowledge/topic/vocab canonical structure

### I18n Owns

- display title
- summary
- explanation
- translation
- learner-facing labels
- teaching notes

### Do Not Cross

- core must not depend on support-language text to be structurally valid
- i18n must not create new canonical ids
- i18n must not be treated as source truth

## Suggested Loader Naming

Use loader names that reflect the composition boundary:

- `loadLearningLibraryCorePack`
- `loadLearningLibraryI18nPack`
- `composeLearningLibrarySnapshot`

If the current code keeps a single data source interface, the internal helper names should still express the same flow:

- `loadCoreThenI18n`
- `composeSnapshotFromPacks`

Avoid names that imply a single finalized blob is still the source of truth.

## Staging Compare Boundary

`seed compare mode` remains valid for parity checks.

Allowed in staging:

- compare seed snapshot vs composed core+i18n snapshot
- inspect list/detail parity
- record mismatch notes

Not allowed:

- hiding composition failures by silently falling back from artifact mode to seed mode
- letting UI screens merge packs to "make it work"
- mixing support languages in one composed snapshot without explicit selection

## Fail-Soft / Fail-Fast Rules

### Fail Fast

The composition layer must fail fast when:

- the selected core pack is missing
- the selected i18n pack is missing
- pack ids do not align
- canonical refs cannot be resolved
- the selected support language pack is incompatible with the target core pack

### Fail Soft

The UI may fail soft only after a valid composed snapshot exists.

Allowed fail-soft behavior:

- missing optional display fields use adapter fallback text
- unknown labels render as placeholders
- partial staging metadata is shown as debug info

## Intake Contract

The frontend intake contract is:

```text
core pack + selected i18n pack -> composed snapshot -> lookup -> UI
```

The snapshot must remain the single read model for screens.

Screens should not know whether a field came from core or i18n.

## Minimal Acceptance Criteria

`LLCM-005h` is done when:

1. frontend intake explicitly supports `core + selected i18n`
2. repository/composer owns the merge logic
3. screens do not merge packs themselves
4. seed compare still works for staging verification
5. missing/invalid artifact packs fail clearly instead of silently degrading to seed mode

## Next Step

After `LLCM-005h`, the next operational step is `LLCM-006a`:

- wire the staging switch in `lingo-frontend-web`
- keep seed compare mode available
- point artifact mode to the new composition flow

## Reference Files

- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/data/repositories/learning_library_content_repository.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/data/services/learning_library_lookup.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/presentation/screens/source_detail_screen.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/data/sources/artifact_learning_library_data_source.dart`
