You are working on `release-aggregator` for CMOD-014.

Goal:
Lock CMOD-011 anchor-linking behavior with regression coverage, while keeping the current multi-level-overlap behavior intact.

Current baseline:
- Positive fixture already exists at `docs/tasks/assets/mockups/regression/anchor_multilevel_overlap_allowed.json`.
- `mockup_check.py` already allows identical spans across different anchor levels, and rejects exact same-level duplicates.

Tasks:
1. Add a companion negative regression fixture for exact same-level duplicate anchors.
   - Suggested path: `docs/tasks/assets/mockups/regression/anchor_duplicate_same_level_rejected.json`
   - It should fail with `CMOD_DUPLICATE_ANCHOR`.
2. Update `docs/tasks/assets/UNITFAC_004_MOCKUP_CHECK_USAGE.md` to document both anchor regression fixtures.
3. If any documentation or task-index entry is now stale, update it in the same change.
4. Do not change the allowed multi-level overlap behavior unless you discover a real validator bug.

Validation:
- Run `scripts/mockup_check.py` on the positive fixture and confirm it passes.
- Run `scripts/mockup_check.py` on the negative fixture and confirm it fails for the duplicate-anchor rule.

Delivery expectations:
- Make concrete file changes.
- Report the exact fixture paths and validation commands.
- Keep the output concise and implementation-focused.
