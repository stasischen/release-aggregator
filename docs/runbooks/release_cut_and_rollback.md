# Runbook: Release Cut and Rollback

Procedures for aggregating build artifacts and preparing production releases.

## Steps

### 1. Aggregate Artifacts
- **Repo**: `release-aggregator`
- **Command (standard)**:
  - `./scripts/release.sh --version vX.Y.Z --source-commit <content-pipeline-commit>`
- **Command (explicit paths)**:
  - `./scripts/release.sh --output /tmp/release-staging --pipeline-dist ../content-pipeline/dist --core-schema ../core-schema --source-repo content-pipeline --source-commit <content-pipeline-commit>`
- **Required inputs**:
  - `pipeline-dist` (預設 `../content-pipeline/dist`)
  - `core-schema` (預設 `../core-schema`)
  - `source-repo`
  - `source-commit`
- **Action**: The script copies JSON artifacts into staging and generates `global_manifest.json`, then validates the manifest via `core-schema/validators/validate.py`.

### 2. Frontend Intake
- **Repo**: `lingo-frontend-web`
- **Action**: Sync the aggregated folder to `assets/content/9_production/`.

### 3. Validation
- **Command**: `npm run test:content` (in frontend)
- **Check**: Verify all `atom_id` references in grammar files exist in the dictionary.

## Rollback
- **Emergency Action**: Revert staged `global_manifest.json` and package files in `release-aggregator` to the previous stable git hash.
- **Frontend**: Point the asset sync tool to the previous release folder.
