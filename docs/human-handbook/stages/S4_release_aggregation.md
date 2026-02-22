# S4: Release Aggregation (`release-aggregator`)
# S4：發版聚合（`release-aggregator`）

## Goal / 目標
Aggregate build artifacts into staging and generate validated manifest.
聚合建置產物到 staging，並產生通過驗證的 manifest。

## Prerequisites / 前置條件
- S3 output exists: `../content-pipeline/dist/`
- 已有 S3 輸出 `../content-pipeline/dist/`
- `../core-schema` has validator and manifest schema
- `../core-schema` 含 validator 與 manifest schema

## Inputs / 輸入
- `../content-pipeline/dist/**`
- `../core-schema/validators/validate.py`
- `../core-schema/schemas/manifest.schema.json`

## Commands (Current) / 現行命令
```bash
./scripts/release.sh --version vX.Y.Z --source-commit <sha>

./scripts/release.sh \
  --output /tmp/release-staging \
  --pipeline-dist ../content-pipeline/dist \
  --core-schema ../core-schema \
  --source-repo content-pipeline \
  --source-commit <sha>
```

## Outputs / 輸出
- `staging/<version>/**`
- `staging/<version>/global_manifest.json`

## Exit Gate / 驗收門檻
1. Manifest validation passes.
1. manifest 驗證通過。
2. Staging has expected JSON/audio artifacts.
2. staging 含預期 JSON/音檔。
3. `global_manifest.json` has non-empty `packages` with valid provenance.
3. `global_manifest.json` 的 `packages` 非空且 provenance 合法。

## Troubleshooting / 排錯
1. `Pipeline dist path not found`:
1. 找不到 dist：
   - Fix `--pipeline-dist`
   - 修正 `--pipeline-dist`
2. `Validator not found` or `Manifest schema not found`:
2. 找不到 validator/schema：
   - Fix `--core-schema`
   - 修正 `--core-schema`
3. `No artifacts found to release`:
3. 無可發版產物：
   - Return to S3 and rebuild
   - 回 S3 重新建置

## Rollback / 回滾
1. Revert staged manifest/package files to previous stable hash.
1. 將 staging manifest/包檔回退至上一穩定 hash。
2. Re-point downstream intake to previous release folder.
2. 將下游 intake 指回上一版資料夾。
