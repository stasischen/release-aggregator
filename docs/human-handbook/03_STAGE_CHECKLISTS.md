# Stage Checklists (Execution)
# 階段執行清單

Use this as the one-page run checklist for S1-S6.
本頁為 S1-S6 一頁式執行清單。

## S1 Ingestion (`content-ko`)
## S1 匯入正規化

1. `cd ../content-ko`
2. Run dry-run / 執行預演：`python3 scripts/import_lllo_raw.py --dry-run`
3. Review report / 檢查報告：`content/staging/reports/missing_mapping_candidates.json`
4. Run write mode / 執行寫入：`python3 scripts/import_lllo_raw.py`
5. Run audit / 執行稽核：`python3 scripts/audit_tokens.py`
6. Confirm / 驗收：
   - `content/source/ko/core/dictionary/atoms/**` updated
   - `content/staging/reports/token_audit_gaps.json` has no blocking gaps

## S2 Segmentation + Mapping (`content-ko`)
## S2 分詞與映射

1. `cd ../content-ko`
2. Run generation / 執行產生：`python3 scripts/import_lllo_raw.py`
3. Run audit / 執行稽核：`python3 scripts/audit_tokens.py`
4. Confirm / 驗收：
   - token/mapping artifacts exist under `content/source/ko/**`
   - audit report has no blocking errors

## S3 Build + Validate (`content-pipeline`)
## S3 建置與驗證

1. `cd ../content-pipeline`
2. Run build / 執行建置：`python3 pipelines/build_ko_zh_tw.py`
3. Confirm / 驗收：
   - `dist/**` exists
   - expected JSON/audio artifacts are present

## S4 Release Aggregation (`release-aggregator`)
## S4 發版聚合

1. `cd /Users/ywchen/Dev/lingo/release-aggregator`
2. Standard release / 標準發版：
   - `./scripts/release.sh --version vX.Y.Z --source-commit <sha>`
3. Explicit path mode / 指定路徑模式：
   - `./scripts/release.sh --output /tmp/release-staging --pipeline-dist ../content-pipeline/dist --core-schema ../core-schema --source-repo content-pipeline --source-commit <sha>`
4. Confirm / 驗收：
   - `staging/<version>/global_manifest.json` exists
   - manifest validation passed
   - staged JSON/audio files are complete

## S5 Frontend Intake (`lingo-frontend-web`)
## S5 前端接收

1. `cd ../lingo-frontend-web`
2. Sync/copy assets to `assets/content/production/`
   同步或複製資產到 `assets/content/production/`
3. Run contract test / 執行契約測試：`npm run test:content`
4. Confirm / 驗收：
   - no missing asset path errors
   - representative lessons render correctly

## S6 Deploy + Rollback
## S6 部署與回滾

1. Confirm S5 passed and previous stable package exists
   確認 S5 通過且前一穩定版本可用
2. Pre-cut validation / 上線前驗證：
   - `cd ../lingo-frontend-web`
   - `npm run test:content`
3. Perform production cut via frontend/ops mechanism
   透過前端或營運流程執行上線
4. Confirm rollback target is executable
   確認回滾目標可立即執行
5. Record release/rollback metadata
   記錄上線與回滾資訊

## Rollback Quick Path
## 回滾快速路徑

1. In `release-aggregator`, revert staged manifest/package files to previous stable hash.
1. 在 `release-aggregator` 將 staged manifest/包檔回退至上一穩定 hash。
2. In frontend intake, point sync back to previous release folder.
2. 在前端接收流程將同步目標改回上一版資料夾。
