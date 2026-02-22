# S3: Build + Validate (`content-pipeline`)
# S3：建置與驗證（`content-pipeline`）

## Goal / 目標
Build release-ready artifacts into `dist/`.
產生可發版的 `dist/` 產物。

## Prerequisites / 前置條件
- S2 completed
- 已完成 S2
- Repo exists: `../content-pipeline`
- 已有 `../content-pipeline`

## Inputs / 輸入
- Canonical source from `content-ko`
- 來自 `content-ko` 的 canonical source

## Commands (Current) / 現行命令
```bash
cd ../content-pipeline
python3 pipelines/build_ko_zh_tw.py
```

## Outputs / 輸出
- `../content-pipeline/dist/**`

## Exit Gate / 驗收門檻
1. Build exits successfully.
1. 建置成功結束。
2. `dist/` contains expected JSON/audio artifacts.
2. `dist/` 含預期 JSON/音檔。
3. Output is ready for S4.
3. 輸出可進入 S4。

## Troubleshooting / 排錯
1. Build entrypoint changed:
1. build 入口變更：
   - Check `../content-pipeline/pipelines/` and update handbook
   - 檢查後同步更新手冊
2. Dist is empty:
2. dist 為空：
   - Verify S1-S2 artifacts, then rebuild
   - 先確認 S1-S2 產物再重建
