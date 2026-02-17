# Codebase Testing Map

## Current Test Surface in This Repo
- No dedicated unit test suite detected in this repository.
- Validation logic is runtime-oriented via `scripts/release.py`:
  - manifest file generation
  - schema validator invocation against external `core-schema`

## Validation Hooks Referenced in Docs
- `docs/ops/stage_contract_matrix_ko.md` defines stage-level gate expectations.
- Runbooks require smoke checks and schema checks in owning repos.
- Closeout protocols require reporting impacted tests and outcomes.

## Practical Test Strategy Observed
- Contract testing is delegated to schema/validator integration.
- End-to-end confidence depends on coordinated checks in multiple repositories.
- Manual operational verification remains a significant component.

## Gaps
- No local CI pipeline file validating docs links or script behavior.
- No synthetic fixture set for `scripts/release.py` in this repo.
- `scripts/release.sh` does not currently pass through arguments for easy scripted tests.

## Recommendations for Future Hardening
- Add minimal fixture-based test for manifest generation.
- Add lint/check command for docs link integrity.
- Add release script smoke test with temp directories.
