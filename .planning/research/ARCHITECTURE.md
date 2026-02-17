# Research: Architecture

## Components
- Control docs layer (`docs/**`).
- Planning/state layer (`.planning/**` + root state files).
- Execution layer (`scripts/**`).
- External contract layer (`core-schema`, upstream/downstream repos).

## Data Flow
1. Task selection -> protocol load.
2. Phase context/plan creation.
3. Execution outputs + summaries.
4. Verification and UAT records.
5. Closeout worklog sync and optional release staging.

## Build Order
1. Stabilize phase artifacts.
2. Tighten script ergonomics + validation.
3. Add automation checks.
