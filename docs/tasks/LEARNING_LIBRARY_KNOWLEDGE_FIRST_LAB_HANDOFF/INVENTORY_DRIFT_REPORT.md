# Learning Library Knowledge-First Lab Inventory & Drift Report

## Objective
Confirm current state of Learning Library artifacts in `lingo-frontend-web` vs `content-ko` sources, and identify drifts from `LLCM-005G` emission and `LLCM-005H` intake specs.

## Findings

### P0: Critical Data & Contract Gaps
- **Vocab Sets & Links missing**: `vocab_sets_index.json` and `links.json` are emitted as empty files (`{ "vocab_sets": [] }`). This blocks the vocabulary feature and relational navigation in Knowledge Lab.
- **Manifest Drift**: `library_manifest.json` omits `vocab_sets` for both core and i18n. It also includes `dictionary_core.json` which is not in the `LLCM-005G` spec scope.
- **Fallback Loading**: `artifact_learning_library_data_source.dart` contains hardcoded fallbacks to `vocab_sets_index` because of the manifest omission, indicating a known but unresolved contract drift.

### P1: ID & Schema Alignment
- **ID Prefix Mismatch**: `topics.json` uses prefixed IDs (e.g., `src.ko.video.79Pwq7MTUPE`) whereas `sources_index.json` uses bare IDs (`79Pwq7MTUPE`). This breaks the resolution logic in the frontend.
- **Source Coverage**: Artifacts only contain 3 sources (2 videos, 1 dialogue), while `content-ko` contains hundreds. This suggests the emission filter is overly restrictive or readiness flags are missing.
- **Provenance vs Refs**: Knowledge items use a legacy `provenance` structure instead of the `example_source_refs` required by the spec.

### P2: Artifact Hygiene
- **Redundant Index Files**: Artifacts include multiple `*_index.json` files (knowledge, sentences, topics, vocab_sets) that are not part of the spec and seem redundant given the main files already contain the flat data.

---

## Inventory Table

| Category | Content-KO (Source) | Frontend (Artifact) | Artifact Location |
| :--- | :---: | :---: | :--- |
| **Sources** | ~1000+ | 3 | `core/sources_index.json` |
| **Sentences** | 2220 (files) | 2818 | `core/sentences.json` |
| **Knowledge** | 224 | 217 | `core/knowledge.json` |
| **Topics** | 4 | 4 | `core/topics.json` |
| **Vocab Sets** | 3 | 0 (empty) | `core/vocab_sets_index.json` |
| **Links** | 5 | 0 (empty) | `core/links.json` |

---

## Contract Drift Table

| Expected (LLCM-005G) | Actual (Frontend) | Status |
| :--- | :--- | :--- |
| `core/sources_index.json` | `core/sources_index.json` | ✅ OK |
| `core/sentences.json` | `core/sentences.json` | ✅ OK |
| `core/knowledge.json` | `core/knowledge.json` | ✅ OK |
| `core/topics.json` | `core/topics.json` | ✅ OK |
| `core/vocab_sets.json` | `core/vocab_sets_index.json` | ❌ **NAME DRIFT** |
| `core/links.json` | `core/links.json` | ✅ OK (Empty) |
| - | `core/dictionary_core.json` | ⚠️ **EXTRA** |
| - | `core/knowledge_index.json` | ⚠️ **EXTRA** |

---

## UI Readiness Table

| Screen/Route | Current Behavior | Gap |
| :--- | :--- | :--- |
| `Knowledge Lab Home` | Index-first (Topics/Items) | Functional, but low density (few sources) |
| `Topic Detail` | Knowledge item list | Broken source/vocab links (ID mismatch) |
| `Knowledge Detail` | Explanation reader | Missing canonical example sections |
| `Sentence Bank` | Sentence list/search | No cross-links to Knowledge/Topics |
| `Vocab Sets (N/A)` | Missing | No UI implementation or data path |

---

## Recommended Next Tasks

### Option A: Fix `vocab_sets` Manifest/Loader Contract (Highest Priority)
- Update `content-pipeline` to emit `vocab_sets.json` (rename from `vocab_sets_index`).
- Add `vocab_sets` to `library_manifest.json`.
- Remove fallback logic in `artifact_learning_library_data_source.dart`.
- Ensure all 3 existing `vocab_sets` source files are correctly packed.

### Option B: Knowledge Lab Index-First UI (Design-First)
- Fix the ID mismatch in `topics.json` to allow topic -> source navigation.
- Implement the Vocab Sets index UI in Knowledge Lab.
- Add "Related Concepts" section to Knowledge Detail using `links.json` once data is populated.

---

## Non-Goals & Files Not Modified
- Did not change any content schemas.
- Did not modify `content-pipeline` or `content-ko` source files.
- Did not touch production navigation for modular lesson runtime.
