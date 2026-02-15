# Frontend Split Preflight Checklist (2026-02-13)

**Target**: Split `lingourmet_universal/` into a dedicated repository.
**Operator**: Agent Antigravity
**Date**: 2026-02-13

## 1. Prerequisite Fixes Status

| ID | Task | Status | Verified By | Notes |
|---|---|---|---|---|
| **Fix-01a** | .gitignore Verification | ✅ PASS | Inspection | `NEW_VIDEO.json` is not ignored by `lingourmet_universal/.gitignore`. Root ignore interference will resolve on split. |
| **Fix-02** | Mock Teardown | ✅ PASS | Code Review | Added `tearDown` to mock handlers in 3 test files. |
| **Fix-03a** | SmartTextSegmenter Fix | ✅ PASS | `flutter test` | Fixed Thai atom segmentation logic (split adjacent atoms). |
| **Fix-03b** | Regression Smoke Tests | ✅ PASS | `flutter test` | Dictionary Overlay, Asset Integrity, Config Loader, Content Validation all PASS. |
| **Fix-04** | README Refactor | ✅ PASS | `flutter analyze` | `lingourmet_universal/README.md` is now self-contained. |

## 2. Integrity Checks

- [x] **Test Suite**: Critical tests are passing.
- [x] **Documentation**: README instructions are runnable.
- [x] **Ignore Rules**: No broad ignores in target directory.
- [x] **Repo State**: Clean working directory.

## 3. Split Execution Plan

**Command**:
```bash
git subtree split --prefix=lingourmet_universal -b split-frontend-v1
```

**Verification**:
1. Switch to branch `split-frontend-v1`.
2. Verify root is now the content of `lingourmet_universal/`.
3. Verify `README.md` is the refactored frontend README.
4. Verify `.gitignore` is the frontend clean gitignore.
5. Run `flutter analyze` to ensure self-contained correctness.

## 4. Rollback Plan

If split fails or verification fails:
1. `git checkout master`
2. `git branch -D split-frontend-v1`
3. Resolve any unexpected state.

## Decision

**GO / NO-GO**: **GO** 🟢
