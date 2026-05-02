# Owners and Responsibilities

This document defines who owns each repository scope and where handoffs happen.

## Repo Ownership

| Repo | Owner Role | Owns | Must Not Own |
| :--- | :--- | :--- | :--- |
| `core-schema` | Architects | Schemas, validator, compatibility policy | Content ingestion, frontend runtime, release deploy |
| `content-ko` | Content Team | Source content, ingestion, normalize, mapping, dictionary/grammar source | Artifact release logic, frontend behavior |
| `content-pipeline` | Infra / Data Engineering | Build and validation pipeline, CI gates, artifact generation | Source-of-truth content edits, release publishing |
| `release-aggregator` | Release Manager | Collect artifacts, provenance manifest, staged release preparation, control-tower docs | Content mutation, frontend code changes, production deploy |
| `lingo-frontend-web` | Frontend Team | Intake sync, runtime loading, app behavior, frontend tests | Content production/build pipeline logic |

## LLLO Responsibility Boundary

1. `lllo` is writer/source input.
2. `content-ko` is canonical publishable source.
3. No direct release from `lllo`.

## Handoff Points

1. `content-ko` -> `content-pipeline`:
   - handoff: normalized source + mapping/dictionary/grammar source
2. `content-pipeline` -> `release-aggregator`:
   - handoff: validated artifacts + schema version + build metadata
3. `release-aggregator` -> `lingo-frontend-web`:
   - handoff: staged release + global manifest + pinned version

## Promotion / Rollback Boundary

`release-aggregator` prepares validated staging artifacts and provenance manifests.
Production promotion and rollback require a separate executable workflow before they can be treated as automated responsibilities.

## Escalation Rule

If a task requires editing files across boundary domains, split into separate repo tasks and approve scope explicitly before execution.
