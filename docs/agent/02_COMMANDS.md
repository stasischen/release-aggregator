# Agent Commands (English Only)

## S1 Ingestion
```bash
cd ../content-ko
python3 scripts/import_lllo_raw.py --dry-run
python3 scripts/import_lllo_raw.py
python3 scripts/audit_tokens.py
```

## S2 Segmentation + Mapping
```bash
cd ../content-ko
python3 scripts/import_lllo_raw.py
python3 scripts/audit_tokens.py
```

## S3 Build + Validate
```bash
cd ../content-pipeline
python3 pipelines/build_ko_zh_tw.py
```

## S4 Release Aggregation
```bash
cd /Users/ywchen/Dev/lingo/release-aggregator
./scripts/release.sh --version vX.Y.Z --source-commit <sha>
```

## S5 Frontend Intake
```bash
cd ../lingo-frontend-web
npm run test:content
```

## S6 Pre-Deploy Validation
```bash
cd ../lingo-frontend-web
npm run test:content
```

## Rollback
- Revert staged manifest/package files to previous stable hash in `release-aggregator`.
- Point frontend intake/sync back to previous release folder.
