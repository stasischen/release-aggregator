# PRG-001: Release Manifest Schema Specification

## Overview

This document defines the formal schema for the **Release Manifest** (`prd.release_manifest.json`), which acts as the authoritative allowlist for production releases. The Production Assembler MUST only bundle lessons and units explicitly listed in this manifest.

## Top-Level Structure

The manifest is a single JSON object containing versioning and an array of release entries.

```json
{
  "version": "1.0.0",
  "updated_at": "2026-04-06T12:00:00Z",
  "entries": [
    { ... entry object ... }
  ]
}
```

## Field Definitions (Entry Object)

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `unit_id` | String | Yes | The teaching unit ID (e.g., `a1_unit_01_intro_identity`). |
| `lesson_id` | String | Yes | The specific lesson ID (e.g., `ko_l1_dialogue_a1_01`). |
| `release_status` | Enum | Yes | Current status (see Enums below). |
| `content_type` | Enum | Yes | Lesson type (see Enums below). |
| `course_type` | Enum | Yes | Instructional role (see Enums below). |
| `source_refs` | Array[String] | Yes | List of raw source IDs associated with this lesson. |
| `contract_version` | String | Yes | Version of the content contract naming rule (see below). |
| `viewer_verified` | Boolean | Yes | Whether the lesson has been verified in the viewer. |
| `qa_gate_passed` | Boolean | Yes | Whether manual/auto QA has approved this entry. |
| `staging_only` | Boolean | Yes | If `true`, this entry MUST NOT enter any production bundle. |
| `notes` | String | No | Internal notes for the release decision. |

## Enumerated Values

### `release_status`
- `draft`: Work in progress, not visible in staging catalog by default or marked as experimental.
- `staging_only`: Verified for staging candidates but restricted from production releases.
- `production`: Approved for final production release.

### `content_type`
- `dialogue`: Interactive dialogue lessons.
- `video`: Video-based comprehension lessons.
- `article`: Reading/article lessons.
- `grammar-heavy`: Grammar-focused drilling or explanation lessons.

### `course_type`
- `lesson`: Standard core curriculum lesson.
- `bonus`: Optional/supplemental video or interactive content.
- `supplemental`: Remedial or extra-practice content.

## Naming Rules (`contract_version`)

To avoid confusion with the `core+i18n vNext` working draft or segmentation versions:
- Prefix: `cm-` (Content Manifest)
- Pattern: `cm-v{major}.{minor}.{patch}`
- Example: `cm-v1.0.0`
- Meaning: This indicates the lesson was approved under Content Manifest Contract version 1.0.0.

## JSON Example

```json
{
  "version": "1.0.0",
  "updated_at": "2026-04-06T12:00:00Z",
  "entries": [
    {
      "unit_id": "a1_unit_01_intro_identity",
      "lesson_id": "ko_l1_dialogue_a1_01",
      "release_status": "production",
      "content_type": "dialogue",
      "course_type": "lesson",
      "source_refs": ["src.ko.dialogue.a1_01"],
      "contract_version": "cm-v1.0.1",
      "viewer_verified": true,
      "qa_gate_passed": true,
      "staging_only": false
    }
  ]
}
```

## Governance Rules

1. **Gate over Source**: Adding a raw source file to the `content-ko` repo does NOT automatically trigger production release. The entry MUST be manually or programmatically added to this manifest.
2. **Production Filter**: The Production Assembler MUST ignore any entry where `staging_only` is `true` or `release_status` is not `production`.
3. **Validation**: Any JSON validator used by the pipeline MUST reject any manifest that uses undefined `release_status` or mismatched `source_refs`.
