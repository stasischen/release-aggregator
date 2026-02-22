# S3: Build + Validate (`content-pipeline`)

## Goal
Build release-ready assets in `dist/`.

## Main Work
1. Read canonical source from content repo.
2. Produce target artifacts under `dist/`.
3. Run build-time validations.

## Output
- `content-pipeline/dist/**`

## Exit Gate
- Dist output complete and ready for release aggregation.
