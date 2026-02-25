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

### 1. Universal E2E Build (New) / 通用 E2E 建置（新）
Used for verifying language engine logic and dynamic loading.
用於驗證語言引擎邏輯與動態載入。

```bash
cd ../content-pipeline
python pipelines/build.py \
  --content-repo ../content-ko \
  --lang ko \
  --output ../release-aggregator/staging/sep_test \
  --sample-lesson A1-01
```

### 2. Packaging Build (Legacy) / 產物封裝（舊）
Used for final Release packaging of existing Korean mapping files.
用於現有韓語映射檔的最終 Release 封裝。

```bash
cd ../content-pipeline
python pipelines/build_ko_zh_tw.py \
  --input ../content-ko \
  --output ./dist \
  --core-schema ../core-schema
```

## Outputs / 輸出
- `../content-pipeline/dist/**` (Release assets)
- `../release-aggregator/staging/sep_test/lessons/*.jsonl` (E2E tokens)
- `../content-ko/reports/qa_report_*.md` (QA findings)

## Exit Gate / 驗收門檻
1. Build exits successfully.
1. 建置成功結束。
2. `dist/` contains expected JSON/audio artifacts.
2. `dist/` 含預期 JSON/音檔。
3. QA Report shows acceptable resolution ratio (>95% for gold).
3. QA 報告顯示可接受的解析率（金標 >95%）。

## Known Limitations & Gaps / 已知限制與具體缺漏
Discovered during `CONTENT_PIPELINE_SEPARATION` (SEP-04):

1. **Yarn Support**: The universal `build.py` currently only processes `.json` dialogue sources. It needs to be extended to handle `.yarn` scripts.
2. **Multi-file Mapping Logic**: While the engine tokenizes text, the logic for splitting atoms across multiple POS-specific mapping files (e.g., `mapping_n.json`, `mapping_v.json`) and checking for orphan atoms is still in the legacy `content-ko` scripts.
3. **Lemma Suffix Heuristics**: The `KoreanEngine` currently defaults to a `+다` suffix for unresolved lemmas in `resolve_lemma`, which may be incorrect for punctuation or symbols.
4. **Validation Integration**: The packaging logic in `build_ko_zh_tw.py` and the engine logic in `build.py` are currently separate. Full integration is required for a single unified command.

## Troubleshooting / 排錯
1. Build entrypoint changed:
1. build 入口變更：
   - Check `../content-pipeline/pipelines/` and update handbook
   - 檢查後同步更新手冊
2. Dist is empty:
2. dist 為空：
   - Verify S1-S2 artifacts, then rebuild
   - 先確認 S1-S2 產物再重建
