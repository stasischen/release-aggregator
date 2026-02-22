# S6: Deploy + Rollback
# S6：部署與回滾

## Goal / 目標
Complete production cut with rollback safety.
完成正式上線並確保可立即回滾。

## Prerequisites / 前置條件
- S5 passed
- S5 已通過
- Previous stable package retained
- 前一穩定版本仍可用

## Inputs / 輸入
- Current validated release package
- 目前已驗證發版包
- Previous stable package/tag
- 前一穩定包或 tag

## Commands (Current) / 現行命令
```bash
cd ../lingo-frontend-web
npm run test:content
# deploy command is frontend/ops specific
```

## Rollback Commands (Current) / 回滾命令（現行）
```bash
# release-aggregator: revert staged manifest/package to previous stable hash
# frontend: point intake/sync back to previous release folder
```

## Outputs / 輸出
- Production release state
- 正式環境上線狀態
- Verified rollback target
- 已驗證可用的回滾目標

## Exit Gate / 驗收門檻
1. Production cut completed.
1. 正式上線完成。
2. Rollback path verified.
2. 回滾路徑可用。
3. Release/rollback metadata recorded.
3. 已記錄上線/回滾資訊。

## Troubleshooting / 排錯
1. Runtime regression after deploy:
1. 上線後 runtime 回歸：
   - Trigger rollback immediately
   - 立即觸發回滾
2. Rollback target unavailable:
2. 無可用回滾目標：
   - Stop rollout and recover prior stable reference
   - 停止擴散並先恢復前一穩定參照

## Runbook / 參考手冊
- `docs/runbooks/release_cut_and_rollback.md`
