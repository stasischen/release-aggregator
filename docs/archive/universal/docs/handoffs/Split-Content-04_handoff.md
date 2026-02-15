# Split-Content-04: Release Aggregator

**Status**: ✅ DONE
**Commit**: (See final commit)
**Date**: 2026-02-14

## 1. Overview
Created `release-aggregator` to package artifacts into a global release with provenance.
Updated `core-schema` to support provenance metadata in `manifest.schema.json`.

## 2. Release Flow
1. **Input**: `content-pipeline/dist` (Built artifacts) + Source Metadata
2. **Process**:
   - Collect artifacts (JSONs)
   - Hash content (SHA256)
   - Generate `global_manifest.json` with provenance
3. **Output**: `staging/{version}/`

## 3. Provenance Data
Added to `manifest.schema.json`:
```json
"provenance": {
  "source_repo": "...",
  "source_commit": "...",
  "built_at": "..."
}
```

## 4. Usage
```bash
# Run release
python3 scripts/release.py \
    --pipeline-dist ../content-pipeline/dist \
    --output staging/v1.0.0 \
    --core-schema ../core-schema \
    --source-repo content-ko \
    --source-commit $(git -C ../content-ko rev-parse HEAD)
```

## 5. Deliverables
- `release-aggregator/scripts/release.py`
- `core-schema/schemas/manifest.schema.json` (Updated)

## 6. Next Steps
- `Split-Content-05` (Frontend Integration): Update app to consume this new global manifest structure.
