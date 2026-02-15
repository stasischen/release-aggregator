# Korean Tokenization Profile (KO)

## Scope
Defines Korean-specific tokenization and mapping behavior used in STAGE-02.

## Policy
- Use rule-based parsing first (no JVM dependency required).
- Apply layered resolution:
  1. exact mapping
  2. heuristic parsing
  3. conflict queue (human review)
- Every accepted mapping must pass reconstruction check.

## Canonical ID Policy
- Business IDs: colon format (example `ko:n:학생`, `ko:e:ㅂ니다`).
- Filesystem-safe IDs: double underscore format for pathing only.
- `fs_safe_id` must not be used for dictionary/runtime lookup.

## Required Fields per Accepted Mapping
- `surface`
- `source_ref`
- `candidate_atom_ids`
- `final_atom_id` or `final_atom_ids`
- `rule_id`
- `confidence`
- `reconstruction_pass`
- `resolver` (`auto` or reviewer id)

## Hard Gates (KO)
- `duplicate_final_atom_id == 0`
- `unresolved_ratio <= 0.10`
- `reconstruction_pass_rate >= 0.98`

## Reconstruction Rules
- Reconstruction is mandatory for `accepted` rows.
- If reconstruction fails, row must go to `mapping_conflicts`.
- Allowed exceptions must be listed explicitly in exception table.

## Confidence Guidance
- High: exact rule + reconstruction pass + no ambiguity.
- Medium: heuristic rule + reconstruction pass + single candidate.
- Low: multi-candidate or weak heuristic; route to conflict queue.
