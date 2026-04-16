# KO Dictionary Layering Plan V1

## Goal

Rebuild the Korean dictionary into explicit frequency bands so the common core stays clean:

- `1-1000` => base dictionary
- `1001-2000` => extension dictionary
- `2001+` => tail / review-only
- polluted or uncertain rows => quarantine

This plan exists to stop legacy mapping contamination from flowing back into the base dictionary.

## Source Scope

Primary sources:

- `content-ko/docs/vocabulary/TOPIK_I_VOCABULARY.md`
- `content-ko/docs/vocabulary/TOPIK_1000_VOCABULARY.md`
- `content-ko/docs/vocabulary/TOPIK_2000_VOCABULARY.md`
- `content-ko/docs/vocabulary/TOPIK_3000_VOCABULARY.md`
- `content-ko/content/mappings/*.json`
- `content-ko/content/core/video_atoms/XknpI48lT-g_atoms.json`

## Non-goals

- Do not rewrite the current legacy mappings in place as the first step.
- Do not force low-confidence or inflected-only rows into the base band.
- Do not use polluted mapping files as the authority for rank assignment.
- Do not modify atom labels in order to hide dictionary gaps.

## Operating Principles

1. The vocabulary docs define the frequency bands.
2. Existing mapping files are seed data only.
3. POS hints may be inherited from seed mappings, but they must be revalidated.
4. Composite atoms are split into components for verification, not collapsed into one guessed row.
5. Any item with a wrong split, wrong POS, or ambiguous canonical form goes to quarantine.
6. Base mapping must remain small, clean, and stable under rerun.

## Task Breakdown

### KO-DICT-LAYER-001

Inventory current mappings and vocabulary sources.

Deliverables:

- ranked vocabulary inventory manifest
- legacy mapping seed extract
- pollution candidate list

### KO-DICT-LAYER-002

Define base, extension, tail, and quarantine policy.

Deliverables:

- dictionary layering policy
- quarantine policy note
- rank-band routing rules

### KO-DICT-LAYER-003

Derive POS assignment rules from current seeds.

Deliverables:

- POS routing matrix
- seed-derived POS extract
- polysemy review list

### KO-DICT-LAYER-004

Build clean base dictionary for rank band `1-1000`.

Deliverables:

- clean base mapping files
- base-layer build report
- base-layer diff summary

### KO-DICT-LAYER-005

Build extension dictionary and quarantine outputs for rank band `1001-2000`.

Deliverables:

- extension mapping files
- quarantine report
- extension diff summary

### KO-DICT-LAYER-006

Validate layered dictionaries against `XknpI48lT-g_atoms.json`.

Deliverables:

- validation audit table
- mismatch summary
- quarantine confirmation

## Execution Order

1. Build the ranked vocabulary inventory.
2. Extract legacy mapping POS seeds.
3. Freeze routing rules for base / extension / tail / quarantine.
4. Generate clean base mapping.
5. Generate extension and quarantine outputs.
6. Re-run the atom audit against the layered dictionary.

## Acceptance Criteria

- The base dictionary only contains verified common-band items.
- The extension dictionary contains mid-frequency items without polluting base.
- Quarantine captures uncertain or conflicting rows explicitly.
- Composite atoms are verified component-by-component.
- `XknpI48lT-g_atoms.json` audits cleanly against the layered design, with residual mismatches clearly classified.

## Verification Plan

### Automated

- Generate a ranked lexicon from the vocabulary docs.
- Compare each candidate row against the legacy mapping seed.
- Re-run the atom audit and emit a mismatch report grouped by `base`, `extension`, and `quarantine`.

### Manual

- Review a sample of dual-POS items such as `보다`, `오다`, `주다`, and `있다`.
- Review a sample of known polluted rows before any promotion.
- Confirm that no polluted row is written back into base during the first pass.

