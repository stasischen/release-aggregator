# Plan: Grammar Index Bridge Sync

This task keeps the published grammar-ID bridge in sync between the dictionary-side `dict_grammar_mapping.json` and the frontend asset bridge `assets/content/grammar/grammar_index.json`.

## Goal

- Keep `G-KO-*` published grammar IDs resolvable to concrete grammar note assets.
- Ensure the dictionary chip/drawer path stays visible for all published refs already advertised by the mapping.
- Treat the bridge file as a tracked contract artifact, not an ad-hoc local fix.

## Scope

1. Inventory the published grammar IDs currently emitted by `dict_grammar_mapping.json`.
2. Diff the published IDs against `grammar_index.json` and identify gaps.
3. Update the bridge mapping and document the sync rule/source-of-truth.
4. Validate the updated bridge with targeted dictionary and grammar-note smoke tests.

## Non-goals

- Do not redesign the dictionary UI.
- Do not reintroduce lesson-scoped filename guessing as the primary contract.
- Do not modify content authoring payloads unless the published bridge itself is missing data.

## Acceptance Criteria

- `grammar_index.json` covers all currently published `G-KO-*` refs referenced by `dict_grammar_mapping.json`.
- The dictionary grammar chip remains fail-soft when a ref is genuinely unpublished.
- The bridge sync can be re-run deterministically when mappings change.
