# S1: Ingestion (`content-ko`)
# S1：匯入正規化（`content-ko`）

## Goal / 目標
Normalize upstream materials into canonical source data.
將上游資料正規化為 canonical source。

## Prerequisites / 前置條件
- Repo exists: `../content-ko`
- 已有 `../content-ko`
- Upstream source available (default: `/Users/ywchen/Dev/lllo`)
- 上游來源可讀（預設：`/Users/ywchen/Dev/lllo`）
- Python env ready in `content-ko`
- `content-ko` Python 環境可用

## Inputs / 輸入
- Upstream lesson materials
- 上游課程內容
- Existing mapping/manual additions in `content-ko`
- `content-ko` 既有 mapping 與人工補充

## Commands (Current) / 現行命令
```bash
cd ../content-ko
python3 scripts/import_lllo_raw.py --dry-run
python3 scripts/import_lllo_raw.py
python3 scripts/audit_tokens.py
```

## Outputs / 輸出
- `../content-ko/content/source/ko/core/dictionary/atoms/**`
- `../content-ko/content/staging/reports/missing_mapping_candidates.json`
- `../content-ko/content/staging/reports/token_audit_gaps.json`

## Important Boundary: S1 Mapping Candidates vs S2 Final Mapping
## 重要邊界：S1 候選 mapping vs S2 正式 mapping

- `missing_mapping_candidates.json` is an **ingestion-gap candidate list**, not a gold-reviewed segmentation/POS truth source.
- `missing_mapping_candidates.json` 是**匯入缺口候選清單**，不是金標級分詞/POS 正確性來源。
- Do **not** blindly add surface forms that may contain segmentation/POS errors (e.g., endings/particles swallowed into one token) just to make S1 ingest pass.
- 不可為了讓 S1 匯入通過就盲補疑似切分/POS錯誤的表面詞（例如吞掉語尾/助詞的形式）。
- Segmentation/POS correctness belongs to **S2** (gold remediation/lint + surgery full-pass + QA gate), and only then should final app-facing `mapping.json` be generated/promoted.
- 切分/POS 正確性屬於 **S2**（gold remediation/lint + surgery full-pass + QA gate），之後才產生/升版正式 `mapping.json`。

## Exit Gate / 驗收門檻
1. Dry-run report generated.
1. 有產生 dry-run 報告。
2. Write mode completed without fatal errors.
2. 寫入模式無致命錯誤。
3. Token audit has no blocking gaps.
3. token audit 無阻斷缺口。
4. Artifacts ready for S2.
4. 產物可進入 S2。

## Troubleshooting / 排錯
1. Missing mapping candidates increase unexpectedly:
1. 若 missing mapping 候選異常增加：
   - Update `../content-ko/content/staging/manual_mapping_additions.json`
   - 更新人工補充檔後重跑
2. Audit shows broken references:
2. 若 audit 出現斷鏈：
   - Fix mapping/source in `content-ko`, rerun audit
   - 修正後重跑 audit

## Rollback / 回滾
```bash
cd ../content-ko
git checkout content/source/ko
```
