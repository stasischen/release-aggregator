# PRG-004: Prototype Production Assembler Contract Specification

> Current status: aspirational contract for post-promotion PRG.
> The current implementation is `scripts/prg/assembler_prototype.py` and remains a prototype until promotion gates pass.

## Goal

Define the target role and responsibilities of the **Production Assembler** in the Production Release Gating (PRG) framework.

## 1. Primary Responsibility

The Production Assembler MUST ONLY package lessons and units that are explicitly allowlisted in the **Release Manifest**. In production mode, it MUST NOT directly scan raw content repositories, `content-pipeline/dist`, or raw staging directories. It must consume Phase 1 `global_manifest.json` or a typed candidate inventory derived from Phase 1 staging.

## 2. Inbound Data Flow

- **Release Manifest (`prd.release_manifest.json`)**: The ONLY source of release decisions.
- **Phase 1 Staging Index (`global_manifest.json`)**: The source of validated artifact paths, hashes, and provenance.
- **Staging Candidate Artifacts**: The validated JSON files, audio, and metadata referenced by `global_manifest.json`.

## 3. Strict Gating Rules

1. **Explicit Inclusion**: If a lesson ID is NOT in the Release Manifest, it MUST NOT enter any production package.
2. **Release Status Filter**: Only entries with `release_status: production` and `staging_only: false` are eligible for production bundling.
3. **QA Requirement**: The Assembler should ideally check if `qa_gate_passed: true` before bundling, but it should fail-fast if a `staging_only` lesson is found in its production target.
4. **No Raw Source Scanning In Production**: The Assembler should never perform `ls` or recursive scans on `core/dialogue/` or `core/video/` to discover "new lessons" in strict production mode. Discovery happens during Phase 1 staging, and selection happens during the **Release Manifest** phase.

## 4. Final Outputs

The current prototype outputs the following files into `staging/prototype_output/`. The future post-promotion target is `lingo-frontend-web/assets/content/production/`.

1. **`manifest.json`**: An asset manifest of JSON file paths for allowlisted lessons.
2. **`lesson_catalog.json`**: An instructional metadata file containing units and their allowlisted lessons.
3. **`production_plan.json`**: A review artifact containing gaps, allowlisted lessons, and packaged artifact hash/provenance from Phase 1.

Asset bundle output is future scope and must not be assumed until implemented and tested.

## 5. Fail-Safe Strategy

- **Empty Manifest**: If the Release Manifest is empty, the production bundle should be empty (or ideally fail with a clear "empty manifest" error).
- **Missing Source**: If a lesson in the manifest references a source that is missing from staging candidates, the assembler MUST fail with a clear error rather than releasing a broken bundle.

## Summary

The Production Assembler is a **Filtering and Packaging tool**, not a discovery tool.
Its current prototype contract is: `Allowlist (Manifest) + global_manifest.json candidates -> frontend-compatible manifest/catalog + production_plan`.
