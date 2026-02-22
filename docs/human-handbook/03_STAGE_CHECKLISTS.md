# Stage Checklists

Use this as the practical gate before moving to next stage.

## S3 -> S4 (Build to Aggregation)

1. Confirm `content-pipeline/dist/` exists and has `.json` / audio files.
2. Confirm `core-schema/schemas/manifest.schema.json` exists.
3. Run `scripts/release.sh --version <tag> --source-commit <sha>`.
4. Verify output `staging/<tag>/global_manifest.json` exists.
5. Confirm manifest validation passed.

## S4 -> S5 (Aggregation to Frontend Intake)

1. Confirm staged release directory is complete.
2. Confirm hash and path entries in `global_manifest.json` match files.
3. Sync required assets to frontend intake path.
4. Perform runtime contract check in frontend environment.

## S5 -> S6 (Intake to Deploy)

1. Verify app loads new assets.
2. Smoke test representative lessons.
3. Keep rollback target (previous release tag) available.
4. Record release cut + rollback notes.
