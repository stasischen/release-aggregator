# S4: Release Aggregation (`release-aggregator`)

## Goal
Aggregate build artifacts into release staging and produce validated manifest.

## Main Work
1. Run `scripts/release.sh`.
2. Internally run `scripts/release.py` to copy artifacts and compute hashes.
3. Generate `global_manifest.json`.
4. Validate manifest via `core-schema/validators/validate.py`.

## Key Commands
```bash
./scripts/release.sh --version vX.Y.Z --source-commit <sha>
```

## Output
- `staging/<version>/**`
- `staging/<version>/global_manifest.json`

## Exit Gate
- Manifest validation passes.
- Staging directory contains expected JSON/audio artifacts.
