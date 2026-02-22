# S2: Segmentation + Mapping (`content-ko`)
# S2：分詞與映射（`content-ko`）

## Goal / 目標
Produce token and mapping artifacts for downstream build.
產生下游建置需要的 token 與 mapping 產物。

## Prerequisites / 前置條件
- S1 completed
- 已完成 S1
- Updated canonical source in `../content-ko`
- `../content-ko` canonical source 已更新

## Inputs / 輸入
- S1 canonical source artifacts
- S1 的 canonical source
- Existing dictionary/mapping resources
- 既有 dictionary/mapping 資源

## Commands (Current) / 現行命令
```bash
cd ../content-ko
python3 scripts/import_lllo_raw.py
python3 scripts/audit_tokens.py
```

## Outputs / 輸出
- `../content-ko/content/source/ko/**`
- `../content-ko/content/staging/reports/token_audit_gaps.json`

## Exit Gate / 驗收門檻
1. Required token/mapping artifacts exist.
1. 必要 token/mapping 產物存在。
2. Audit has no blocking errors.
2. audit 無阻斷錯誤。
3. Artifacts are usable by S3 build.
3. 產物可被 S3 建置使用。

## Troubleshooting / 排錯
1. Audit fails:
1. audit 失敗：
   - Fix references and rerun ingestion + audit
   - 修正參照後重跑 ingestion 與 audit
2. Mapping mismatch:
2. mapping 不一致：
   - Re-check manual additions and normalization inputs
   - 重新檢查人工補充與正規化輸入
