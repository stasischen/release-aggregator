# LLCM-007b — Mismatch Audit & Staging Acceptance Gate

This document records the observed mismatches between the `seed` (prototype) and `artifact` (migration) data sources for Dialogue and Video, and defines the criteria for acceptance into the Staging environment.

## 1. Mismatch List (Seed vs. Artifact)

### 1.1 Structural Mismatches
| Category | Seed Baseline | Artifact Mode | Impact |
| :--- | :--- | :--- | :--- |
| **Schema** | Flat `sentences` array in `seed_json.dart`. | V5 `core` JSON (nodes/turns) + `i18n` packs. | Minimal (handled by `LessonAdapter`). |
| **ID Continuity** | Hardcoded IDs like `d1_01`, `v_005`. | Canonical Turn IDs (e.g., `turn_01`, `v_005`). | Mixed. Alignment is good for Video, but Dialogue IDs may vary. |
| **I18n Binding** | Bundled `translationZhTw` field. | Compose `core` + `i18n` pack at runtime. | High consistency requirement for matching IDs. |

### 1.2 Enrichment Gaps (Deferred)
| Gap | Status | Description |
| :--- | :--- | :--- |
| **Dialogue Atoms** | 🚨 **KNOWN GAP** | `dialogue_atoms.json` is missing globally in `content-ko`. Word-level segmentation for Dialogue is currently unavailable in artifact mode. |
| **Segmentation Status** | ⚠️ PARTIAL | Video atoms exist for sample `79Pwq7MTUPE`, but not for all content. |

### 1.3 Volume & Scope Mismatches
| Category | Seed Baseline | Artifact Mode | Notes |
| :--- | :--- | :--- | :--- |
| **Turn Count** | Partial snippets (e.g., 23 sentences for Video). | **Full Core Resource** (e.g., 48+ turns). | Intentional. Artifact mode provides the complete resource. |
| **Metadata** | `themeTags` (String array). | V5 `unit` metadata with `zh_tw` titles. | Artifact provides richer metadata structure. |

---

## 2. Field Mapping Comparison (Seed vs. Artifact Mode)

| Field (Seed) | Artifact Linkage (via LessonAdapter) | Parity Status |
| :--- | :--- | :--- |
| `id` | `segment_id` (usually matching) | ✅ High |
| `surfaceKo` | `ko` (from Core `text` or `ko`) | ✅ High |
| `translationZhTw` | `translation` (from I18n `translations_i18n.zh_tw`) | ✅ High |
| `knowledgeRefs` | `anchor_refs` (from Core) | ⚠️ Partial (Schema varies) |
| `vocabRefs` | `atoms` (from separate Atoms JSON) | 🚨 Missing for Dialogue |
| `startMs` / `endMs` | `time.start` / `time.end` (Core) | ✅ High (Video Only) |

---

## 3. Staging Acceptance Gate (Executable Criteria)

| Criterion | Verification Method | Pass Condition |
| :--- | :--- | :--- |
| **Discovery** | Check Course Map in Modular Viewer. | Unit ID and Title are visible. |
| **Loading** | Click unit in Map. | Detail panel renders without Error Overlay. |
| **Content Flow** | Inspect Turns in Lesson View. | >0 turns visible with Korean text. |
| **I18n Sync** | Toggle/Check Translation Visibility. | `zh_tw` text is present and matches context. |
| **Fail-Soft** | Open Dialogue unit (A1-01). | View renders text turns despite missing atoms. |
| **Atom Fidelity** | Open Video unit (79Pwq7MTUPE). | Interactive chips appear on sentences. |

---

## 4. Decision Log
- **Dialogue Atoms**: Deferred. We accept the mismatch of "no word-level highlight" for Dialogue in Staging until the production extraction pipeline is ready.
- **Title Mapping**: Artifact mode will use the `title_i18n` from the pack, which may differ slightly from the prototype's manual string.
- **Volume**: We accept that artifacts return the full resource, even if the prototype only used a subset of sentences.

