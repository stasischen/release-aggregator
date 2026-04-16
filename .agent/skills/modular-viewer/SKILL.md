---
name: modular-viewer
description: Use when you need to preview curriculum content, grammar points, or example sentences in the Modular UI Viewer. Use this to verify that the generated JSON artifacts are correctly rendered and that audio/TTS/alignment are working as expected.
---

# Modular UI Viewer

The Modular UI Viewer (Lingo Modular Mockup) is a local browser-based runtime that simulates the Lingourmet mobile app experience. It is the primary tool for content developers and agents to verify "Real Content" builds.

Primary location:
- `/Users/ywchen/Dev/lingo/release-aggregator/tools/modular-viewer/index.html`

## Capabilities

- **Curriculum Preview**: Load and navigate lesson sequences (Dialogue, Video, Vocab, Practice).
- **Knowledge Lab Preview**: Browse and read grammar explanations, patterns, and example sentences.
- **Data Verification**: Verify i18n resolution, atom alignment, and asset linking.
- **Audio Testing**: Test TTS engine selection and audio engine stability.

## Standard Procedures

### 1. Synchronization
Before viewing changes made in `content-ko`, you must synchronize the runtime data:

```bash
# In release-aggregator
python3 scripts/generate_library_manifest.py
```

Or from `content-ko` (see `content-ko/VIEWER.md`):
```bash
python3 scripts/ops/export_learning_library_runtime.py \
  --locale zh_tw \
  --out-root ../release-aggregator/tools/modular-viewer/data/runtime/
```

### 2. Loading Content
The viewer can load two types of content:

1.  **Lesson Units**: Defined in `tools/modular-viewer/data/fixtures.json`.
2.  **Knowledge Lab**: Automatically scanned from `tools/modular-viewer/data/library_manifest.json` and its runtime companions.

### 3. Debugging
- If content doesn't load: Check the browser console for fetch errors (usually JSON file missing or malformed).
- If audio fails: Click the "🔊 語音修復" (Audio Repair) button in the top right to prime the speech engine.
- If translations are missing: Ensure the build artifacts include the targeted locale (default: `zh_tw`).

## Related Documentation

- `release-aggregator/docs/tasks/mockups/modular/UNIFIED_LESSON_RUNTIME_CONTRACT.md` (Legacy documentation for data shapes)
- `content-ko/VIEWER.md` (Sync instructions)
