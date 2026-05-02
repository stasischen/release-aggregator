# Runbook: Release Cut and Rollback

Procedures for aggregating build artifacts and preparing production releases.

## Steps

### 1. Aggregate Artifacts To Staging
- **Repo**: `release-aggregator`
- **Command (standard)**:
  - `./scripts/release.sh --version X.Y.Z --scope <scope> --source-manifest <manifest> --pipeline-version <pipeline-version> --schema-version <schema-version> --source-commit <content-pipeline-commit>`
- **Command (explicit paths)**:
  - `./scripts/release.sh --output /tmp/release-staging --version X.Y.Z --scope <scope> --source-manifest <manifest> --pipeline-dist ../content-pipeline/dist --core-schema ../core-schema --source-repo content-pipeline --source-commit <content-pipeline-commit> --pipeline-version <pipeline-version> --schema-version <schema-version>`
- **Required inputs**:
  - `pipeline-dist` (預設 `../content-pipeline/dist`)
  - `core-schema` (預設 `../core-schema`)
  - `source-repo`
  - `source-commit`
  - `source-manifest`
  - `scope`
  - `pipeline-version`
  - `schema-version`
- **Action**: The script runs the requested quality scope, verifies artifacts against the source manifest, copies JSON/audio artifacts into clean staging, generates `global_manifest.json`, then validates the manifest via `core-schema/validators/validate.py`.

### 2. Production Gate
- **Current status**: planned Phase 2.
- **Candidate implementation**: `scripts/prg/assembler_prototype.py`.
- **Decision source**: `prd.release_manifest.json` or another explicit release allowlist.
- **Hard rule**: PRG must consume validated staging artifacts from Step 1 or a candidate inventory derived from them. It must not bypass Step 1 by reading raw source repositories as a production input.
- **Implemented guardrails**: PRG strict mode consumes Phase 1 `global_manifest.json`, rejects raw directory scanning, and carries hash/provenance into `production_plan.json`.
- **Remaining blocker**: PRG remains prototype until docs, Makefile validation, and promotion target/output ownership are aligned.

### 3. Frontend Intake
- **Repo**: `lingo-frontend-web`
- **Action**: Sync the aggregated folder to `assets/content/production/`.

### 4. Validation
- **Command**: `make test-prg` (in release-aggregator)
- **Check**: Verify PRG frontend contract, strict-mode source rules, and provenance bridge.
- **Command**: `npm run test:content` (in frontend)
- **Check**: Verify all `atom_id` references in grammar files exist in the dictionary.

## Rollback
- **Current status**: rollback is manual. `release-aggregator` prepares validated staging artifacts but does not yet implement production promotion or rollback automation.
- **Emergency Action**: restore the previous staged release folder and `global_manifest.json`, rerun manifest validation, then have `lingo-frontend-web` point its asset sync tool to the restored folder.
- **Required follow-up**: add an executable promotion / rollback workflow before treating rollback as automated release-aggregator ownership.
