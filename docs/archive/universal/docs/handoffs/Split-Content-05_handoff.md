# Split-Content-05: Frontend Integration

**Status**: ✅ DONE
**Commit**: (See final commit)
**Date**: 2026-02-14

## 1. Overview
Integrated `lingo-frontend-web` with `release-aggregator` output.
Established intake workflow for `ko__zh_tw` dialogue content.

## 2. Changes
- **Updated `pubspec.yaml`**: Added `assets/content/production/packages/ko/dialogue/`.
- **New Script**: `scripts/sync_content.sh` copies from `release-aggregator/staging`.
- **Docs**: Updated `docs/operations/content_artifact_intake.md` with mapping table.
- **Tests**: Updated `test/core/asset_integrity_test.dart` to verify `dialogue` assets.

## 3. Path Mapping
| Source | Target |
|---|---|
| `ko/zh_tw/dialogue/*` | `packages/ko/dialogue/*` |

## 4. Verification
```bash
# Sync content
./scripts/sync_content.sh

# Run tests
flutter test test/core/asset_integrity_test.dart
flutter test test/repositories/event_repository_integration_test.dart
```

## 5. Next Steps
- `Split-Content-06` (Freeze Monorepo): Archive legacy content in monorepo and update docs.
