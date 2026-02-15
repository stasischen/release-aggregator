# Task Checklist

## 🔜 Next Steps

## ✅ Completed (2026-01-26)

- [x] **Video Dictionary E2E Test (v3-task-14)**
  - [x] Implemented robust mock infrastructure (`FakeDictionaryService`, `FakeVideoPlayback`).
  - [x] Fixed widget testing timeouts and race conditions.
  - [x] Verified full interaction flow: Subtitle Tap -> Dictionary Panel Open -> Content Display.

- [x] **Task Archival System**
  - [x] Implement `scripts/archive_tasks.py`
  - [x] Validated archival of DONE tasks
  - [x] Update `agent_sync_sop.md` with archival instructions

- [x] **GSD Context Optimization**
  - [x] Identify context bottleneck points
  - [x] Create `scripts/export_gsd_context.py` (Automation for Phase 1 -> Phase 2)
  - [x] Update `gsd.md` to strict "Clean Session" rules
  - [x] Verify the full flow (Plan -> Export -> Reset -> Execute)

- [x] **Distributed Workflow**
  - [x] Initialized Agent Manager concept and documentation.
  - [x] Fixed Identity alignment.

## ✅ Completed (2026-01-24)

- [x] **Provider Standardization (v3-task-6)**: Migrated `CafeSlang` and `SinoNumbers` to `AsyncNotifier` (Riverpod 2.x).
- [x] **Test Enforcement (v3-task-7)**: Implemented unit tests for `CafeSlang` and `SinoNumbers` with full logic coverage.
- [x] **Fix: UI AsyncValue Handling**: Updated Number Elevator and Sino Numbers Screen to correctly handle async state.
- [x] **VideoRepository Refactoring (v3-task-5)**: Extracted `SubtitleParserService` from VideoRepository, decoupling parsing logic. (Architect Approved).
- [x] **Workflow Upgrade (GMAO v1.4)**: Implemented Handoff Ticket mechanism and strict Session Logs.

## ✅ Completed (2026-01-24)

- [x] **Riverpod Refactoring & Build Stabilization**:
  - Resolved `InvalidTypeException` in `flashcard_view_model.dart` (Generator conflict).
  - Fixed `video_repository` code generation.
  - Standardized generic `Ref` usage across providers.
  - Cleaned up legacy files (`dream_weaver_backup.dart`) and unused imports.
  - Documented provider architecture decisions in `technical/ARCHITECTURE_DECISIONS.md`.

## ✅ Completed (2026-01-23)

- [x] **Thai Video V5 Pipeline Integration**:
  - Fixed segmentation using Max Match algorithm.
  - Deployed Thai dictionary with video-specific vocabulary.

## ✅ Completed (2026-01-22)

- [x] **Workflow Standardization & Code Quality**:
  - Consolidate idiom/chunk handling.
  - Refactored `DictionaryService`, `TtsService` documentation.
  - Archived legacy scripts and consolidated workflows.

<details>
<summary>📦 Archived Priorities</summary>

- [x] **Typing Games Architectural Reorganization (L5)** (2026-01-22)
- [x] **Standardize Mini-Games (L4)** (2026-01-22)
- [x] **Dictionary Logic Refactoring (L3)** (2026-01-22)
- [x] **Firebase Language Pack Integration (OTA)** (2026-01-22)
- [x] **German Content Validation** (2026-01-22)
- [x] **App Pack Pruning** (2026-01-22)
- [x] **Video Dictionary UI & Translation Refinements** (2026-01-21)
- [x] **German Dictionary Debugging & Audit** (2026-01-21)
- [x] **Refactoring Phase** (2026-01-21)
- [x] **Dream Weaver Prototype** (2026-01-21)
- [x] **Google Sign-In & Avatar** (2026-01-20)

</details>
