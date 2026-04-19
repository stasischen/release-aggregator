# PRG Artifact Map Overview

## Purpose

This document explains the main files used in the Production Release Gating (PRG) flow and what each one does.

The key idea is:

- `release manifest` decides what may be released
- `staging candidates` provide buildable source material
- `production artifacts` are generated outputs
- `mockup viewer` files are for UI/runtime testing, not release decisions

## Main Artifacts

| Artifact | Typical Path | What It Does | Source of Truth |
| :--- | :--- | :--- | :--- |
| Release Manifest | `staging/production_release_gating/prd.release_manifest.json` or `staging/prg_pilot/pilot_allowlist.json` | The allowlist of lessons/units that may enter production. This is the release decision layer. | Yes |
| Staging Candidate Inventory | `content-pipeline/staging/**` or prototype staging outputs in `staging/prototype_output/**` | The pool of buildable candidate lessons gathered from source content. It is for verification and assembly, not release approval. | No |
| Production `manifest.json` | `lingo-frontend-web/assets/content/production/manifest.json` | The generated asset manifest consumed by the app or frontend package. It lists what is shipped. | No, derived output |
| Production `lesson_catalog.json` | `lingo-frontend-web/assets/content/production/lesson_catalog.json` | The generated lesson metadata catalog. It holds instructional structure, unit mapping, and display metadata. | No, derived output |
| Production bundles | `lingo-frontend-web/assets/content/production/packages/ko/**` | The actual lesson JSON and related assets that are shipped to production. | No, derived output |
| Viewer mockup data | `tools/modular-viewer/**`, `docs/tasks/mockups/**` | Local mock / demo data used for UI and runtime validation. It helps test viewer behavior but does not decide release eligibility. | No |

## What Each One Does

### What Counts As A "Course" Or "Lesson"

In this PRG flow, the word "course" is informal shorthand for the **lesson/unit blueprint**.

More precisely:

- `unit_id` identifies the broader instructional unit
- `lesson_id` identifies the concrete lesson entry inside that unit
- the lesson/unit blueprint defines what the teaching package looks like as a whole
- `dialogue`, `video`, `article`, and `grammar-heavy` are content types that can appear inside that blueprint

So:

- A `dialogue` file is not automatically "the course"
- A `video` file is not automatically "the course"
- An `article` file is not automatically "the course"
- The course is the **instructional package** that groups and orders those materials

### Practical Mental Model

Think of it this way:

- `blueprint` = the design for the lesson/unit
- `content_type` = the kind of material inside that design
- `release manifest` = the allowlist saying which blueprints may ship
- `production artifacts` = the packaged output generated from the allowed blueprints

Example:

- a `bonus_video` unit may contain one or more video lessons
- a dialogue-based unit may contain multiple dialogue lines plus supporting metadata
- an article-based unit may contain article text plus linked review or vocabulary data

The important point is that the release gate happens at the **lesson/unit blueprint** level, not at the individual raw source file level.

### 1. Release Manifest

The release manifest is the only file that says "this lesson/unit is allowed to ship."

Typical fields:

- `unit_id`
- `lesson_id`
- `release_status`
- `content_type`
- `course_type`
- `source_refs`
- `contract_version`
- `viewer_verified`
- `qa_gate_passed`
- `staging_only`

This file answers:

- What may go to production?
- Is this lesson only for staging?
- Has QA or viewer verification passed?

Reference:

- [PRG_001_RELEASE_MANIFEST_SCHEMA.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/PRG_001_RELEASE_MANIFEST_SCHEMA.md)

### 2. Staging Candidate Inventory

This is the staging-side pool of content that can be built, validated, or reviewed.

It may include:

- dialogue
- video
- article
- other content types that are not yet ready for production

This file set answers:

- Can the content be built?
- Is the content available on disk?
- Does the content match the expected schema or staging contract?

Reference:

- [PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md)

### 3. Production `manifest.json`

This is a generated output, not the decision source.

It is the asset manifest that the production app or frontend bundle reads at runtime.

This file answers:

- What asset files are shipped?
- Which lesson JSON paths exist in the production package?

It should be derived from the release manifest, not hand-edited.

Reference:

- [PRG_003_MANIFEST_MIGRATION_PATH.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/PRG_003_MANIFEST_MIGRATION_PATH.md)

### 4. Production `lesson_catalog.json`

This is also a generated output.

It contains the instructional metadata for shipped lessons and units, such as:

- unit ordering
- lesson ordering
- titles
- tags
- display metadata

This file answers:

- How should the shipped lessons be organized?
- What metadata should the frontend display?

Reference:

- [PRG_003_MANIFEST_MIGRATION_PATH.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/PRG_003_MANIFEST_MIGRATION_PATH.md)

### 5. Production Bundles

These are the actual packaged lesson artifacts and related assets.

They are the files that the app ultimately consumes after assembly.

This layer answers:

- What exact lesson JSON is shipped?
- What exact asset bundle is bundled with it?

Reference:

- [PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md)

### 6. Viewer Mockup Data

These files are for development, QA, and UI simulation.

Examples:

- `tools/modular-viewer/data/**`
- `docs/tasks/mockups/**`

They are useful for:

- checking viewer rendering
- testing UI logic
- reproducing runtime states

They are not used to decide what can ship to production.

Reference:

- [UNIFIED_LESSON_VIEW_ARCHITECTURE.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/assets/UNIFIED_LESSON_VIEW_ARCHITECTURE.md)

## Flow Summary

```text
source truth
  -> staging candidate inventory
  -> release manifest
  -> production assembler
  -> production manifest / lesson catalog / bundles
```

The viewer mockup files sit beside this flow as test fixtures, not as release inputs.

## Practical Rule

If a file answers "can we release this lesson?", it belongs to the release manifest layer.

If a file answers "what content exists in staging?", it belongs to the staging candidate layer.

If a file answers "what is shipped to the app?", it belongs to production artifacts.

If a file answers "what should the UI look like during testing?", it belongs to mockup or viewer data.
