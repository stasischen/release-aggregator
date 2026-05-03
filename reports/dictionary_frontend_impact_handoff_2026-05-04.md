# Dictionary Frontend Impact Handoff

Date: 2026-05-04

Scope: P0 exact dictionary pollution cleanup for `ko:n:밤`, `ko:n:명단`, and `ko:n:문구`, plus regression fixture coverage. This handoff is for the parallel `FRONTEND_V2_INTAKE_COMPLETION` thread.

## Dictionary Contract Changes

No runtime contract shape change was introduced in this dictionary review thread.

- `atom_id` format remains stable: `ko:{pos}:{lemma}`.
- Entry identity remains `atom_id` plus `definitions.zh_tw[].entry_no` / `sense_id`.
- `mapping_v2.entries[*].entry_refs` remains structurally stable.
- `mapping_v2.entries[*].sense_refs` remains structurally stable.
- Hanja/source-origin metadata remains available through definition-level metadata when applicable.
- Row-level `metadata.hanja` should be treated as diagnostic/fallback only, not as the authoritative per-entry origin when definition-level metadata exists.

## Changed Files / Paths

Changed in `content-ko`:

- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl`
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/2026-04-30-fix/manifest.json`
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/2026-05-04/n.jsonl`
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/2026-05-04/manifest.json`
- `/Users/ywchen/Dev/lingo/content-ko/content_v2/inventory/dictionary/manifest.json`
- `/Users/ywchen/Dev/lingo/content-ko/docs/handoffs/regression_fixtures/dictionary_forbidden_glosses_2026-05-03.json`

Changed in `release-aggregator`:

- `/Users/ywchen/Dev/lingo/release-aggregator/reports/dictionary_frontend_impact_handoff_2026-05-04.md`

Generated but not committed in this thread:

- `/Users/ywchen/Dev/lingo/content-pipeline/dist/ko/packages/core/dictionary_core.json`
- `/Users/ywchen/Dev/lingo/content-pipeline/dist/ko/packages/i18n/dict_ko_zh_tw.json`
- `/Users/ywchen/Dev/lingo/content-pipeline/dist/ko/packages/i18n/mapping.json`
- `/Users/ywchen/Dev/lingo/content-pipeline/dist/ko/packages/i18n/mapping_v2.json`

## ID / Lookup Key Changes

No atom IDs were renamed or removed.

- `ko:n:밤` remains `ko:n:밤`.
- `ko:n:명단` remains `ko:n:명단`.
- `ko:n:문구` remains `ko:n:문구`.

Corrected active runtime export behavior:

- `밤` now maps only to the night/evening sense. The polluted `예` glosses are forbidden by regression fixture.
- `명단` now has `entry_no: 1`, `sense_id: s1`, and definition-level `hanja: 名單`.
- `문구` now has `entry_no: 1`, `sense_id: s1`, and definition-level `hanja: 文句`.

`문구` was not expanded to include `文具`; current source evidence confirms `문구01 / 文句`, while `문구점` separately covers `文具店`.

## Frontend-Breaking Risks

- Frontend code must not assume `entry_no` is globally stable across rebuilds. It is stable within a given exported atom, but data cleanup can normalize polluted single-entry rows back to `entry_no: 1`.
- Frontend lookup should prefer `mapping_v2` candidates over legacy `mapping.json` when disambiguation or origin display matters.
- Frontend display should prefer definition-level `sense_refs[].origin` / `entry_refs[].origin` over row-level origin fields.
- A single surface can still map to multiple candidates by POS or homograph. UI disambiguation should be candidate-based, not string-only.
- No frontend runtime code was changed in this thread.

## Required Frontend Adapter Assumptions

- `mapping_v2.entries[surface]` is the stable public lookup entry point for V2 dictionary intake.
- `entry_refs` and `sense_refs` are stable as field names and shapes.
- `origin.hanja` may appear on `sense_refs` or `entry_refs`; use it for per-entry display.
- `row_origin` or top-level candidate origin should be treated as less precise than entry/sense origin.
- Legacy `mapping.json` remains a lossy surface-to-first-atom fallback.
- `dictionary_core.json` remains the source of atom definitions and should be used when richer detail is required.

## Validation Commands Run

In `/Users/ywchen/Dev/lingo/content-ko`:

```bash
python scripts/ops/audit_dictionary_regressions.py --fail-on-error --inventory-root content_v2/inventory/dictionary/2026-05-04
python -m unittest tests/test_build_dictionary_inventory.py -v
```

In `/Users/ywchen/Dev/lingo/content-pipeline`:

```bash
make export-bridge-dictionary
```

In `/Users/ywchen/Dev/lingo/release-aggregator`:

```bash
python scripts/sync_frontend_assets.py --include-dictionary --dry-run
```

The aggregator dry-run invoked frontend asset validation:

```bash
make validate-assets
```

Result: Flutter asset integrity tests passed (`00:00 +6: All tests passed!`).

Runtime spot-check after export:

- `dictionary_core.json` contains clean `밤`, `명단`, and `문구` definitions.
- `mapping_v2.json` contains `entry_refs.entry_no: 1` for `명단` and `문구`.
- `mapping_v2.json` carries `origin.hanja: 名單` for `명단`.
- `mapping_v2.json` carries `origin.hanja: 文句` for `문구`.

## Open Questions For FRONTEND_V2_INTAKE_COMPLETION

- Should dictionary UI display entry-level origin from `entry_refs.origin` directly, or resolve back into `dictionary_core.definitions` for full sense details?
- Should the frontend hide row-level origin entirely when `entry_refs.origin` exists?
- Should search result grouping use `homograph_key` as the UI candidate key?
- Should legacy `mapping.json` be deprecated from runtime lookup once `mapping_v2` adapter is complete?

## Frontend Intake Response

Frontend commit: `5abcc31c feat: load dictionary mapping v2 candidates`

The frontend adapter now treats `mapping_v2.json` as the primary lookup source and retains the full candidate model. This matches the dictionary-side contract assumptions above.

Frontend implementation notes:

- `mapping_v2.json` is primary.
- `mapping.json` is fallback only when `mapping_v2.json` is missing from the manifest or fails to load.
- Candidate lists are preserved; the adapter no longer collapses lookup to a single atom ID internally.
- `entry_refs`, `sense_refs`, `homograph_key`, `origin`, and `row_origin` are parsed and retained.
- Existing UI APIs remain compatible by returning candidates in `mapping_v2` order.
- `entry_no` is not treated as a global ID.

Dictionary-side answers to frontend open questions:

- `homograph_key`: The current `content-pipeline/scripts/export_bridge_dictionary.py` exporter emits `homograph_key` for every candidate as `{surface}|{pos}|{atom_id}`. Frontend fallback to `atom_id` is still appropriate defensive behavior for older or malformed fixture data.
- `entry_no`: Treat as string/number tolerant at intake. Source inventory is intended to normalize entry numbers as integers, but the public contract should allow either JSON number or string because historical fixtures and hand-authored patches have used both.
- `sense_id`: Treat as atom-local only. It is stable within one atom definition, but must not become a global lookup key. Use it together with `atom_id` and, when relevant, `entry_no`.

Additional adapter assumptions after frontend intake:

- Candidate identity should prefer `homograph_key` when present, otherwise fall back to `atom_id`.
- UI disambiguation should operate over candidate lists, not over raw surface strings.
- Per-entry display should prefer `entry_refs.origin` / `sense_refs.origin`; row-level origin remains a fallback only.

## Core Origin Migration Plan

Decision: dictionary origin metadata belongs to the Korean lexical core, not to locale i18n payloads.

New canonical direction:

- `dictionary_core.json` / inventory rows carry language-neutral `entries[]` and `senses[]`.
- `entries[].origin` is the authoritative place for entry-level Hanja/source metadata.
- `senses[]` links `sense_id` to `entry_no`.
- `definitions.zh_tw[]` remains the Traditional Chinese translation/gloss block.
- `mapping_v2.entry_refs.origin` and `mapping_v2.sense_refs.origin` remain derived runtime cache fields during the transition.

Compatibility removal timing:

- Phase 1, current: add `entries[]` / `senses[]` to inventory output and teach exporter to prefer core entries. Keep existing `mapping_v2` origin cache.
- Phase 2: frontend adapter joins origin from `dictionary_core.entries[]` and treats `mapping_v2` origin as optional.
- Phase 3: add a validation gate proving frontend tests pass when `mapping_v2` origin fields are absent.
- Phase 4: remove exporter denormalization of origin into `mapping_v2`.
- Phase 5: remove definition-level origin fallback after no active inventory shard relies on `definitions.<locale>[].hanja/origin`.

Do not remove the compatibility cache before Phase 3 passes. The current user-visible dictionary overlay depends on fast candidate metadata, and the data cleanup work is still active.
