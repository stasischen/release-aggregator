# Task: Root Cause Analysis & Fix for Skipped Stable Tests

## Overview
- **Status**: PLANNED
- **Priority**: MEDIUM
- **Assignee**: AI Agent / QA
- **Description**: Re-enable and fix tests that were skipped or modified during the V5-A1 content migration and asset cleanup. Investigate why UI snapshots changed and re-generate Golden images.

## Background
During the "Stable Branch Cleanup" (2026-02-21), several tests were skipped (`skip: true`) to unblock the release pipeline. These failures were primarily caused by:
1. **Asset Deletion**: Non-KO assets (de, th) were removed from the stable branch, breaking tests that relied on them.
2. **V5 Standardization**: Changes in dictionary IDs and atoms caused UI renders to differ slightly from old Golden snapshots.

## Skipped/Modified Tests to Address
1. [ ] **Golden Tests Re-generation**:
   - `test/features/video/presentation/widgets/immersive_subtitle_overlay_golden_test.dart`
   - `test/features/dictionary/presentation/widgets/dictionary_content_golden_test.dart`
   - *Action*: Run `flutter test --update-goldens` on a standard environment (macOS) and verify the changes are purely superficial (styling/V5 IDs).
2. [ ] **Asset Integrity logic Restoration**:
   - `test/core/asset_integrity_test.dart`
   - *Action*: Ensure the test correctly handles environment-based checks (Stable vs. Experimental) so that adding new languages doesn't immediately break the build again.
3. [ ] **Video Metadata Synchronization**:
   - `assets/config/video_metadata.json` vs. `9_production` contents.
   - *Action*: Ensure automated build scripts keep this metadata in sync with the physical asset deletion.

## Root Cause Analysis (RCA) Checklist
- [ ] Determine if UI changes in Golden tests were due to V5 `DictionaryParser` normalization or genuine styling regressions.
- [ ] Verify if `ConfigLoader` lesson count estimation (previously 102) needs a dynamic threshold instead of hardcoded expectations.

## Success Criteria
- [ ] All tests in `lingo-frontend-web` pass without `skip: true`.
- [ ] Golden images are updated to match V5 standards.
- [ ] Clean test report across all core modules.
