# PRG-004: Production Assembler Contract Specification

## Goal

Define the new role and responsibilities of the **Production Assembler** in the Production Release Gating (PRG) framework.

## 1. Primary Responsibility

The Production Assembler MUST ONLY package lessons and units that are explicitly allowlisted in the **Release Manifest**. It MUST NOT directly scan `content-ko` repositories or candidates to determine "what to release."

## 2. Inbound Data Flow

- **Release Manifest (`prd.release_manifest.json`)**: The ONLY source of release decisions.
- **Staging Candidate Artifacts**: The source of validated JSON files, audio, and metadata.

## 3. Strict Gating Rules

1. **Explicit Inclusion**: If a lesson ID is NOT in the Release Manifest, it MUST NOT enter any production package.
2. **Release Status Filter**: Only entries with `release_status: production` and `staging_only: false` are eligible for production bundling.
3. **QA Requirement**: The Assembler should ideally check if `qa_gate_passed: true` before bundling, but it should fail-fast if a `staging_only` lesson is found in its production target.
4. **No Raw Source Scanning**: The Assembler should never perform `ls` or recursive scans on `core/dialogue/` or `core/video/` to discover "new lessons." Discovery happens during the **Candidate Build** (Staging) phase, and selection happens during the **Release Manifest** phase.

## 4. Final Outputs

The Production Assembler outputs the following files into the production directory (e.g., `lingo-frontend-web/assets/content/production/`):
1. **`manifest.json`**: An asset manifest of JSON file paths for allowlisted lessons.
2. **`lesson_catalog.json`**: An instructional metadata file containing units and their allowlisted lessons.
3. **Asset Bundles**: The actual JSON artifacts and audio referenced by the allowlisted lessons.

## 5. Fail-Safe Strategy

- **Empty Manifest**: If the Release Manifest is empty, the production bundle should be empty (or ideally fail with a clear "empty manifest" error).
- **Missing Source**: If a lesson in the manifest references a source that is missing from staging candidates, the assembler MUST fail with a clear error rather than releasing a broken bundle.

## Summary

The Production Assembler is a **Filtering and Packaging tool**, not a discovery tool.
Its contract is: `Allowlist (Manifest) + Candidates (Staging) -> Production Assets`.
