# Deploy and Rollback

Active reference runbook:
- `docs/runbooks/release_cut_and_rollback.md`

Operational rule:
1. Every release cut must have a rollback target.
2. Rollback uses prior known-good release package.
3. Always verify schema and runtime compatibility before production cut.
