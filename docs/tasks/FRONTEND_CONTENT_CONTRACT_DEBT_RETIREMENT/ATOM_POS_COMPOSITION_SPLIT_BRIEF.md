# Atom POS Composition Split Brief

Date: 2026-05-06
Task: `fccdr-10`
Repos: `lingo-frontend-web`, `content-pipeline`, `content-ko`, `release-aggregator`

## Decision

Keep Korean chunk composition intact, but separate learner-facing POS display
from backend atom composition.

Current `LingoAtom.pos` has two incompatible meanings:

1. Displayable POS key: `n`, `v`, `adj`, `p`, `e`, `adv`, `pron`
2. Backend composition/debug chain: `adj+e+e`, `v+e`, `n+cop+e`,
   `prop+cop+e`, etc.

The `+` composition is intentional and should remain available for Korean
chunking, atom validation, dictionary lookup, and QA. The contract issue is only
that learner-facing UI currently receives the same field and must guess whether
it is safe to display.

The frontend should not parse `+` or `:` to derive teaching labels. The content
contract should make the display label explicit or provide a shared
composition-to-display-label mapping.

## Current Findings

From current bundled frontend assets:

- Video core atoms expose 54 unique `pos` values.
- Sentence Bank atoms expose 158 unique `pos` values.
- Many values are technical composition chains, for example:
  - `adj+e+e`
  - `v+e`
  - `n+cop+e`
  - `adj+e+vx+e`
  - `xnum+n+cop+e+e`

Frontend already has defensive UI code:

- `SentenceDetailScreen._safeAtomPosLabel()` hides POS containing `+` or `:`.
- `DictionaryContent` treats `pos.contains('+')` as composite and hides top
  badges for those cases.

That means UI is already compensating for a contract problem. The fix should not
re-segment the content; it should add a display-label layer.

## Target Atom Contract

Recommended atom fields, without changing composite ids or segmentation:

```json
{
  "id": "ko:v:먹다+ko:e:어요",
  "text": "먹어요",
  "pos": "v+e",
  "display_pos_key": "verb_form",
  "composition": ["v", "e"],
  "debug_pos_composition": "v+e",
  "components": [
    {
      "id": "ko:v:먹다",
      "text": "먹",
      "display_pos_key": "v"
    },
    {
      "id": "ko:e:어요",
      "text": "어요",
      "display_pos_key": "e"
    }
  ]
}
```

### `display_pos_key`

Learner-facing and i18n-safe. Frontend may pass this key into POS label
localization.

Allowed examples:

- `n`
- `v`
- `adj`
- `adv`
- `p`
- `e`
- `cop`
- `aux`
- `pron`
- `det`
- `num`
- `count`
- `phrase`
- `verb_form`
- `adjective_form`
- `noun_phrase`
- `predicate_form`
- `marked_phrase`
- `number_phrase`

Most display labels can be derived automatically from the existing composition.
They do not require manual review of every segmentation.

### `composition`

Backend/pipeline validation structure. It describes the morphological
composition as an array, not a display string.

Allowed examples:

- `["v", "e"]`
- `["adj", "e", "e"]`
- `["n", "cop", "e"]`

### `debug_pos_composition`

Optional debug-only string for diagnostics and artifact QA. It may preserve the
old `v+e` shape, but frontend learner-facing UI must not consume it.

### `pos`

During migration, `pos` may continue to carry the existing composition string
because downstream content already uses it. Long term, either:

- `pos` becomes a simple lexical/display POS key and composition moves to
  `composition`, or
- `pos` remains legacy composition and UI always uses `display_pos_key`.

The important rule is: UI display labels must not be inferred by splitting
`pos` at `+`.

## Composition-to-Display Mapping

Use an automated mapping layer first; only unknown or ambiguous compositions
need review.

Suggested initial mapping:

| Composition Pattern | Display POS Key | Notes |
| --- | --- | --- |
| `v+e`, `v+e+e`, `v+e+vx+e` | `verb_form` | Verb plus endings / auxiliary endings |
| `adj+e`, `adj+e+e`, `adj+e+vx+e` | `adjective_form` | Descriptive verb/adjective inflection |
| `n+cop+e`, `prop+cop+e`, `pron+cop+e` | `predicate_form` | Noun/proper/pronoun predicate form |
| `n+p`, `pron+p`, `prop+p`, `n+p+p` | `marked_phrase` | Nominal phrase with particles |
| `xnum+count`, `num+count`, `xnum+n` | `number_phrase` | Number/counting phrase |
| single `n`, `v`, `adj`, `p`, `e`, etc. | same key | Simple lexical POS |

Pipeline should emit an `unknown_display_pos_key` or validation report for
unmapped compositions. Review only that report, not the whole segmentation set.

## Compatibility Rule

Because the app is not launched, use a direct migration for runtime assets once
the pipeline emits the new fields.

Short-term frontend behavior may keep hiding raw `pos` values containing `+`,
but that is a temporary safety net, not the contract. New UI should prefer:

1. `display_pos_key`
2. dictionary inventory `pos` for a resolved component atom
3. no POS label

It should never display `composition` or `debug_pos_composition`.

## Content Pipeline Changes

1. Emit `display_pos_key` for every atom shown in learner-facing token UI.
2. Emit `composition` as an array when the atom is a composed form.
3. Emit `debug_pos_composition` only for diagnostics if needed.
4. Add an automated composition-to-display mapping table.
5. Emit a review report only for unknown/ambiguous compositions.
6. Preserve dictionary atom POS as a simple lexical POS key.

## Frontend Changes

### Data Models

- Add optional `displayPosKey` to atom DTO/domain models.
- Add optional `composition` or `debugPosComposition` only if frontend validators
  need it. Learner UI should not render it.
- Keep `pos` as legacy composition input during the migration slice.

### UI

- Sentence Detail token labels use `displayPosKey`.
- Dictionary component rows use dictionary inventory POS or atom
  `displayPosKey`.
- Remove UI rules that inspect `pos.contains('+')` once strict artifacts are
  required.
- Add regression tests ensuring technical strings such as `v+e` and
  `adj+e+e` are not visible.

### Dictionary Resolver

Resolver candidates may keep candidate `pos` as a lexical POS key. If candidate
composition is needed, use `composition`, not `pos`.

## Validation Gates

### Runtime Asset Gates

- Do not reject `+` in composition fields or composite ids.
- Require `display_pos_key` when an atom is shown as a tappable learner token.
- Reject `display_pos_key` values containing `+` or `:`.
- Require every composition string used by learner-facing atoms to have a
  mapping or an explicit review status.
- If `composition` exists, require it to be an array of POS keys.
- If `debug_pos_composition` exists, require it not to be consumed by UI tests.

### UI Gates

- Sentence Detail and Dictionary popup tests must not find strings matching:
  - `v+e`
  - `adj+e`
  - `adj+e+e`
  - `n+cop+e`
- POS label localization tests should use `display_pos_key`, not raw
  composition.

## Suggested Implementation Slices

### Slice A: Contract And Validator

- Add atom contract doc/schema for `display_pos_key`, `composition`, and
  `debug_pos_composition`.
- Add validator checks in release-aggregator.

### Slice B: Pipeline Emission

- Emit new fields for video atoms and Sentence Bank atoms.
- Add the composition-to-display mapping table.
- Keep old `pos` composition during transition if needed.
- Emit an unknown/ambiguous mapping report for review.

### Slice C: Frontend Consumption

- Add fields to Flutter atom models.
- Switch UI to `displayPosKey`.
- Keep strict tests preventing technical composition display.

### Slice D: Remove Temporary Filtering

- Remove `contains('+')` / `contains(':')` learner UI guards after artifacts
  provide `display_pos_key` coverage and validators enforce it.

## Acceptance Criteria

- Learner UI never displays backend composition strings.
- Atom models no longer overload one `pos` field with two meanings.
- Validators fail if `display_pos_key` contains composition strings.
- Composition strings and composite ids remain valid for Korean chunking.
- Existing dictionary lookup, video atom lookup, and Sentence Bank token lookup
  continue working.

## Non-Goals

- Do not redesign the visible POS label taxonomy in this slice.
- Do not remove `+` composition.
- Do not re-segment Korean atoms or require full manual segmentation review.
- Do not change lesson runtime format.
- Do not collapse dictionary and sentence atom semantics.
- Do not block current UI testing on full pipeline migration; keep temporary UI
  filtering until strict artifacts exist.
