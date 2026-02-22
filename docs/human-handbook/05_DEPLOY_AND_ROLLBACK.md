# Deploy and Rollback
# 部署與回滾

Active runbook:
現行操作手冊：
- `docs/runbooks/release_cut_and_rollback.md`

Operational rules:
操作原則：
1. Every release cut must have a rollback target.
1. 每次上線都必須有回滾目標。
2. Rollback uses previous known-good package.
2. 回滾使用前一個已驗證穩定包。
3. Validate schema and runtime compatibility before production cut.
3. 上線前必須完成 schema 與 runtime 相容性驗證。
