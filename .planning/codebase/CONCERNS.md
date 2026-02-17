# Codebase Concerns Map

## Concern 1: Release Wrapper Usability
- `scripts/release.sh` calls `python3 scripts/release.py` without forwarding CLI args.
- Impact: operator friction and mismatch with runbook examples using flags.

## Concern 2: Hardcoded Metadata in Manifest
- `scripts/release.py` uses constants for version/pipeline/schema metadata.
- Impact: provenance quality and release traceability are weaker than intended.

## Concern 3: Automation Gaps for Protocol Drift
- Conventions are robustly documented but mostly manually enforced.
- Impact: easy long-term drift between docs and actual execution habits.

## Concern 4: Cross-Repo Dependency Fragility
- Release validation depends on external path correctness for `core-schema`.
- Impact: failures may appear late if local checkouts are stale or mislocated.

## Concern 5: Testing Depth
- No repo-local automated tests around release script behavior.
- Impact: regressions in aggregation/manifest generation can slip to manual verification.

## Concern 6: Duplicate Planning Sources
- Root planning files and GSD `.planning/*` can diverge without sync policy.
- Impact: confusion about source of truth during phase execution.

## Mitigation Direction
- Consolidate active planning source and add periodic sync checks.
- Add smoke-test harness and wrapper argument passthrough.
- Incrementally automate key policy checks (links, required fields, mode tags).
