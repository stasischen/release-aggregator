# Runbook: Release Cut and Rollback

Procedures for aggregating build artifacts and preparing production releases.

## Steps

### 1. Aggregate Artifacts
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

### 2. Frontend Intake
- **Repo**: `lingo-frontend-web`
- **Action**: Sync the aggregated folder to `assets/content/production/`.

### 3. Validation
- **Command**: `npm run test:content` (in frontend)
- **Check**: Verify all `atom_id` references in grammar files exist in the dictionary.

## Rollback
- **Current status**: rollback is manual. `release-aggregator` prepares validated staging artifacts but does not yet implement production promotion or rollback automation.
- **Emergency Action**: restore the previous staged release folder and `global_manifest.json`, rerun manifest validation, then have `lingo-frontend-web` point its asset sync tool to the restored folder.
- **Required follow-up**: add an executable promotion / rollback workflow before treating rollback as automated release-aggregator ownership.
