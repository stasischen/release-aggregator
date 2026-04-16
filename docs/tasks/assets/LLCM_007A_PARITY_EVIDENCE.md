# LLCM-007a — Parity Verification Evidence (Dialogue/Video)

## Status Summary
| Aspect | Status | Findings |
| :--- | :--- | :--- |
| **Course Map** | ✅ VERIFIED | Dialogue and Video units appear correctly in the modular viewer map. |
| **Dialogue Content** | ✅ VERIFIED | Turns and metadata for `A1-01` are correctly parsed and rendered. |
| **Dialogue I18n** | ✅ VERIFIED | `zh_tw` translations from `i18n` artifacts are successfully enriched. |
| **Video Content** | ✅ VERIFIED | Turns for `79Pwq7MTUPE` are visible in the unified timeline. |
| **Video Atoms** | ✅ VERIFIED | Word-level segmentation (atoms) is present and functional for Video. |

## Baseline Comparison (Seed vs Artifact)

### 1. Dialogue (A1-01)
- **Seed Baseline**: Standard dialogue turns with `role` and `text`.
- **Artifact Intake**: Verified that `payload.content` (Real Core) is correctly normalized by `LessonAdapter`.
- **Mismatch Check**: Observed that `id` mapping between `core` and `i18n` is 1:1 consistent.

### 2. Video (79Pwq7MTUPE)
- **Seed Baseline**: Complex turn-based video content with time ranges.
- **Artifact Intake**: V5 `nodes -> Start -> turns` structure is successfully flattened by the viewer.
- **Mismatch Check**: Atoms are correctly aligned with turn IDs (`v_001`, `v_002`, etc).

## Critical Infrastructure Adjustments
During verification, the following adjustments were made to the `modular-viewer` infrastructure:
1. **Symlink Repair**: Fixed `data/content-ko` to point to `../../../../content-ko/content`.
2. **Real Content Bridge**: Established symlinks for `i18n` and `atoms` in `tools/modular-viewer/data/real_content/`.
3. **App Hardening**: Updated `js/app_v2.js` to handle raw V5 core JSONs that lack full unit metadata by providing a default `can_do_i18n` stub.

## Visual Verification
Visual verification was confirmed using a local HTTP server to bypass CORS.
Screenshots showing successful rendering of Dialogue A1-01 and Video 79Pwq7MTUPE were captured and reviewed.

> [!IMPORTANT]
> **Dialogue Atoms Gap**: Observed that Dialogue `A1-01` currently lacks word-level segmentation (atoms) in the repo. This is an expected artifact gap and is handled gracefully by the viewer.
