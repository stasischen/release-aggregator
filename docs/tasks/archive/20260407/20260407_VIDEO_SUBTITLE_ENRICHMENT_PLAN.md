# Implementation Plan: Video Subtitle Quality & Enrichment (zh_tw)

Target: 11 newly ingested Korean Vlog videos in `content-ko`.

## User Review Required

> [!IMPORTANT]
> **Subtitles Reconstruction**: The video `ngOTUxM25gM` (Self-Introduction) is currently missing Chinese subtitles. I will use Gemini to generate these based on the Korean source and English reference. 
> 
> **Transcoding Strategy**: Since `opencc` is not available in the environment, I will use Gemini for the Simplified-to-Traditional conversion. This has the advantage of also being able to handle terminology mapping (e.g., "視頻" -> "影片") and removing disallowed parenthetical romanizations.

## Proposed Changes

### `content-ko`

#### [MODIFY] [reconstruct_zh_tw_logic](file:///Users/ywchen/Dev/lingo/content-pipeline/.agent/skills/youtube-content-ingestion/scripts/reconstruct_zh_tw.py)
*   I will either implement the LLM logic in this script or use a custom script in `content-ko/scripts/ops/` to handle the batch processing.
*   Goal: Generate `translations` object for missing/problematic videos.

#### [NEW] `content-ko/content/i18n/zh_hans/video/ko_v5_vlog_*.json` (11 files)
*   As per user request, Simplified Chinese versions will be preserved/created in a separate `zh_hans` directory for future use.

#### [NEW] `content-ko/content/i18n/zh_tw/video/ko_v5_vlog_ngOTUxM25gM_vlog_self_intro.json`
*   Reconstructed Chinese subtitles for the self-intro video (Traditional Taiwan Standard).

#### [MODIFY] `content-ko/content/i18n/zh_tw/video/ko_v5_vlog_*.json` (11 files)
*   Perform bulk Simplified -> Traditional conversion for the `zh_tw` (Traditional) versions.
*   Terminology normalization (video -> 影片, program/software -> 程式, digital/network -> 數位/網路).
*   Removing Disallowed Romanization (e.g., "韓語 (Hanguo)" -> "韓語").

## Open Questions

- **Specific Terminology**: Are there other specific terms besides "視頻/影片" and "程序/程式" that you want to ensure are converted correctly?
- **Tone of Voice**: For the self-intro video, should the Chinese translation be formal or informal? (The Korean source is likely informal if it's a vlog).

## Verification Plan

### Automated Tests
- Run `python3 scripts/ops/validate_video_i18n.py audit --target-lang zh_tw`.
- Assert `files_with_issues = 0` (or at least no issues for the 11 target videos).
- Verify `structurally_ok: true` in `manifest.json`.

### Manual Verification
- Generate markdown reports using `verify_video_i18n.py` for all 11 videos in `/tmp/`.
- Provide a summary of a few segments to the user for final approval of the translation tone.
