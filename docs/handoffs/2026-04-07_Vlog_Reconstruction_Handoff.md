# AI Handoff: Korean Vlog Subtitle Reconstruction

- **Date**: 2026-04-07
- **Topic**: Video Subtitle Enrichment & Quality Correction
- **Status**: [IN_PROGRESS]

## Context
We are processing 11 Korean vlogs in `content-ko` (v5_vlog series) to provide high-quality `zh_tw` (Traditional) and `zh_hans` (Simplified) subtitles. 

## Major Findings (CRITICAL)
Structural analysis revealed systematic **ID shifts** in most inherited Simplified Chinese assets (likely from previous ingestion steps).
- Example: In `NyCrQ-NZMbg`, "fry it" was mapped to "抹上", and "fish cake" was mapped to "你要在這裡吃嗎?".
- Summary: Simple transcoding is **CORRUPTED**. All 11 videos (except `ngOTUxM25gM`) must be **reconstructed** using Korean (`core`) and English (`en`) as ground truth.

## Accomplishments
- [x] Initial Audit of all 11 videos.
- [x] Full Reconstruction of `ngOTUxM25gM` (Self Intro) - **OK/Verified**.
- [x] Potential shifts detected in `NyCrQ-NZMbg` (~30 issues) and `eF65dUUDcEQ` (~10 issues).
- [x] Created `zh_hans` preservation structure.

## Pending Work
1.  **Fast Alignment Check**: Finalize the list of problematic files among the remaining 10 vlogs.
2.  **Deletion**: Remove the misaligned `zh_tw` and `zh_hans` files to start clean.
3.  **Deep Reconstruction**:
    - For each video ID:
        - Read `content/core/video/ko_v5_vlog_{ID}.json` (Korean).
        - Read `content/i18n/en/video/ko_v5_vlog_{ID}.json` (English).
        - Use Gemini to generate perfectly aligned `zh_tw` (Taiwan terms) and `zh_hans`.
4.  **Verification**: Run `validate_video_i18n.py audit` to ensure `match_ids: true`.

## Next Session Prompt
"我們正在處理 content-ko 的 11 支 vlog 字幕。請參考 `/Users/ywchen/Dev/lingo/release-aggregator/docs/handoffs/2026-04-07_Vlog_Reconstruction_Handoff.md`。重點是解決原始簡體中文資產的 **位移 (ID shift)** 問題。請針對剩餘 10 支有問題的影片，以韓英原始碼為基礎進行全量重建，確保 zh_tw 和 zh_hans 的映射完全正確。"
