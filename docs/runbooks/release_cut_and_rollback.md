# Runbook: Release Cut and Rollback

Procedures for aggregating build artifacts and preparing production releases.

## Steps

### 1. Aggregate Artifacts
- **Repo**: `release-aggregator`
- **Command**: `./scripts/release.sh`
- **Action**: The script collects JSON artifacts from `content-pipeline/build/` and generates a `manifest.json`.

### 2. Frontend Intake
- **Repo**: `lingo-frontend-web`
- **Action**: Sync the aggregated folder to `assets/content/9_production/`.

### 3. Validation
- **Command**: `npm run test:content` (in frontend)
- **Check**: Verify all `atom_id` references in grammar files exist in the dictionary.

## Rollback
- **Emergency Action**: Revert the `manifest.json` in `release-aggregator` to the previous stable git hash.
- **Frontend**: Point the asset sync tool to the previous release folder.
