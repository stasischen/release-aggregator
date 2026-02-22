# S5: Frontend Intake (`lingo-frontend-web`)
# S5：前端接收（`lingo-frontend-web`）

## Goal / 目標
Import staged release assets into frontend runtime.
將 staging 發版資產導入前端執行環境。

## Prerequisites / 前置條件
- S4 completed and validated
- S4 完成且已驗證
- Repo exists: `../lingo-frontend-web`
- 已有 `../lingo-frontend-web`

## Inputs / 輸入
- Staged release folder from `release-aggregator`
- 來自 `release-aggregator` 的 staging 發版資料夾

## Commands (Current) / 現行命令
```bash
cd ../lingo-frontend-web
# sync/copy staged assets into assets/content/production/
npm run test:content
```

## Outputs / 輸出
- `../lingo-frontend-web/assets/content/production/**`

## Exit Gate / 驗收門檻
1. Intake has no missing asset path errors.
1. intake 無缺失資產路徑錯誤。
2. `npm run test:content` passes.
2. `npm run test:content` 通過。
3. Representative lessons render correctly.
3. 代表課程渲染正常。

## Troubleshooting / 排錯
1. Missing asset path errors:
1. 缺資產路徑：
   - Verify S4 staged folder completeness and resync
   - 確認 S4 完整後重同步
2. Content contract test fails:
2. 契約測試失敗：
   - Check `atom_id` references and upstream mapping consistency
   - 檢查 `atom_id` 參照與上游 mapping 一致性
