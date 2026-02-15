# Frontend Repo Split Migration Record (2026-02-13)

## Summary

- Migration type: `git subtree split`
- Source monorepo: `git@github.com:stasischen/Lingourmet_universal.git` (local workspace monorepo)
- Source prefix: `lingourmet_universal/`
- Split branch (initial): `split-frontend-v1`
- Split branch (fixed): `split-frontend-v2`
- Target repo: `git@github.com:stasischen/lingo-frontend-web.git`
- Target branch: `main`
- Status: `COMPLETED (v2 stabilized)`

## Commands Executed

```bash
git subtree split --prefix=lingourmet_universal -b split-frontend-v1
git -C /Users/ywchen/Dev/Lingourmet_universal push git@github.com:stasischen/lingo-frontend-web.git split-frontend-v1:main

# v2 fix for missing production assets
git add .gitignore lingourmet_universal/assets/content/9_production/packages
git commit -m "Track frontend production package assets for split"
git subtree split --prefix=lingourmet_universal -b split-frontend-v2
git push git@github.com:stasischen/lingo-frontend-web.git split-frontend-v2:main --force-with-lease
```

## Push Result

- Initial push:
  - `split-frontend-v1 -> main` (accepted, but production assets were incomplete)
- Stabilized push:
  - `split-frontend-v2 -> main` (accepted)
- Final split head:
  - `bc8e43c5b763ee310e38c11c7c76ef4ddbb1c3ae`

## Ownership and Scope

- New frontend canonical repository:
  - `git@github.com:stasischen/lingo-frontend-web.git`
- Monorepo keeps historical origin and planning/docs context.
- Frontend code changes should be made in new repo by default.

## Ongoing Operating Rules

1. Content/Pipeline repo(s):
   - build and validate `assets/content/9_production` artifacts.
2. Frontend repo (`lingo-frontend-web`):
   - consumes artifacts only.
   - does not run content production pipeline as source-of-truth.
3. Monorepo (`Lingourmet_universal`):
   - planning, migration records, and cross-repo coordination.
   - no daily frontend feature development.

## Post-Migration Verification Checklist

- [x] Remote repo exists and is reachable.
- [x] Branch `main` created from split payload.
- [x] Fresh clone baseline check completed:
  - `flutter pub get`
  - smoke regression bundle:
    - `test/dictionary_overlay_logic_test.dart`
    - `test/core/asset_integrity_test.dart`
    - `test/services/config_loader_test.dart`
    - `test/content/content_validation_test.dart`
  - targeted integration/widget checks:
    - `test/repositories/event_repository_integration_test.dart`
    - `test/widgets/immersive_dictionary_overlay_test.dart`
- [ ] CI baseline configured in new repo.

## Rollback Plan

This migration is non-destructive for monorepo history.

If rollback is needed:

1. Keep monorepo as source of truth temporarily (no history loss).
2. Stop merging feature work into the split repo.
3. Continue development from monorepo `master`.
4. Optionally delete split branch/repo only after team confirmation.

## Notes

- Root cause of early failures:
  - repo-level ignore rule (`**/content/9_production/`) in monorepo blocked tracking of most production assets.
- Fix applied:
  - explicit unignore for `lingourmet_universal/assets/content/9_production/**` in monorepo `.gitignore`.
- Stabilization tasks should be tracked in frontend repo issue/task board.
