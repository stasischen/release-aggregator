# PRG Phase 2 Review Decision

Date: 2026-05-02
Scope: `scripts/prg/assembler_prototype.py`, `scripts/prg/seed_release_manifest.py`, release runbook, PRG contracts.

## Verdict

Promote later.

PRG is the right architectural direction for a future `staging -> production` gate, but it is not ready to replace or be renamed into the production release path.

`scripts/release.py` remains the Phase 1 ingestion and provenance gate:

- validates a source manifest
- copies opaque pipeline artifacts into staging
- hashes artifacts
- writes `global_manifest.json`
- validates the manifest against `core-schema`

PRG should become Phase 2 only after it consumes Phase 1 staging artifacts, preserves the provenance boundary, and passes promotion-readiness drift checks.

## Review Findings

### P0: PRG can bypass hardened staging provenance

At the time of this review, `scripts/prg/assembler_prototype.py` defaulted its candidate source to a legacy `content-ko` staging directory when that directory existed.

That bypasses:

- `content-pipeline` release handoff
- `scripts/release.py` source-manifest check
- artifact hashing
- `global_manifest.json`
- core-schema manifest validation

Status: fixed in code after this review. Strict mode now requires an explicit Phase 1 `global_manifest.json` or equivalent manifest-backed source and rejects raw directory scanning.

### P1: PRG contract and implementation disagree

The PRG contract says the production assembler should not discover releasable content by recursively scanning `core/dialogue` or `core/video`.

Current implementation still has a directory scanner adapter in `CandidateInventory.scan_directory`.
This is acceptable for planning-mode analysis, but not for production promotion.

Status: fixed in code after this review. Strict CLI rejects raw directory scanning; planning mode may still use the scanner for analysis.

### P1: PRG output is frontend production-shaped, not release-aggregator provenance-shaped

`assembler_prototype.py` writes:

- `manifest.json`
- `lesson_catalog.json`
- `production_plan.json`

Those are useful Phase 2 outputs. The script now preserves Phase 1 artifact hash and provenance from `global_manifest.json` into `production_plan.json`.
Promotion still needs final output ownership and bundle generation decisions before the prototype is renamed or wired as a production command.

## Architecture Decision

Use a two-phase release model:

1. Phase 1: `content-pipeline -> release-aggregator staging`
   Owner: `scripts/release.sh` and `scripts/release.py`.
   Output: validated staged artifacts and `global_manifest.json`.

2. Phase 2: `release-aggregator staging -> production candidate bundle`
   Future owner: PRG assembler after contract hardening.
   Output: allowlisted production manifest, lesson catalog, production plan, and bundles.

Do not rename `assembler_prototype.py` yet.
Do not replace `release.py`.
Do not make PRG the default release command until the P0/P1 gaps above are fixed.

## Codex-Ready Next Tasks

1. Done: add a PRG strict mode guard that rejects raw `content-ko` candidate sources.
2. Done: add support for reading `release.py` staging output through `global_manifest.json`.
3. Done: add provenance carry-through from `global_manifest.json` into `production_plan.json`.
4. Done: add tests with a minimal staged release fixture.
5. Remaining: align docs/Makefile validation and decide final promotion target before renaming the script.

## Needs Gemini / DeepSeek Before Implementation

Ask Gemini to map the exact current frontend production manifest and lesson catalog contract before changing PRG outputs.
Ask DeepSeek to inventory all PRG docs and task files for path/schema drift before promoting the prototype.
