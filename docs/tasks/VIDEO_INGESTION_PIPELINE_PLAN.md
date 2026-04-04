# Implementation Plan: Video Ingestion Pipeline (VIDEO_INGESTION_PIPELINE)

## Goal
Establish an automated pipeline to fetch, process, and distribute YouTube video content (subtitles + metadata) into the Lingourmet platform with proper language separation (Source vs I18N).

## Architecture (3-Tier Separation)

### 1. Source Layer (Original)
- **Repository**: `content-ko`
- **Path**: `content/source/ko/video/{videoId}.json`
- **Owner**: Korean content curators.
- **Content**: Original Korean text with timestamps (`start`, `end`, `text`). No translations here.

### 2. Localization Layer (I18N)
- **Repository**: `content-ko`
- **Paths**: 
  - `content/i18n/zh_tw/video/{videoId}.json`
  - `content/i18n/en/video/{videoId}.json`
- **Content**: Key-value pairs mapping IDs (from source) to localized strings.

### 3. Production Layer (Melted)
- **Tool**: `content-pipeline`
- **Final Output Path (App-side)**: `lingo-frontend-web/assets/content/production/packages/{lang}/video/{videoId}.json`
- **Format**: Unified `SubtitleLine` objects compatible with Flutter app.

---

## Tooling Design (Skill: `youtube-content-ingestion`)

### Component 1: `fetch_yt.py`
- Uses `youtube-transcript-api` to fetch available transcripts.
- Detects the list of supported languages.
- Splits content into specific JSON files based on the directory structure above.

### Component 2: `video_metadata_generator.py`
- Automatically scrapes YouTube video metadata (Title, Duration, Channel, Thumbnail).
- Generates a snippet compatible with `lingo-frontend-web/assets/config/video_metadata.json`.

---

## Execution Roadmap

- [ ] **Phase 1: Tooling Setup (content-pipeline)**
  - Initialize the skill directory.
  - Set up Python dependencies.
  - Implement basic subtitle extraction.
  
- [ ] **Phase 2: Storage Setup (content-ko)**
  - Create directory structure for `source/ko/video` and `i18n/*/video`.
  - Ingest initial data for `dpzJkC7hptY` (Jaerim's Vlog).

- [ ] **Phase 3: Integration (lingo-frontend-web)**
  - Add the video entry to `video_metadata.json`.
  - Verify playback in the App using the "Video Learning" screen.

## Risks & Mitigation
- **Captions Availability**: Some videos don't have manual captions.
  - *Mitigation*: Fallback to auto-generated captions (mark them as `generated`).
- **Timestamp Drift**: Edits in source might break I18n alignment.
  - *Mitigation*: Use IDs for mapping, not timestamps, as much as possible.
