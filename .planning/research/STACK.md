# Research: Stack

## Current Stack
- Docs-first control tower with Markdown and JSON contracts.
- Operational scripts in Bash + Python.
- External validator and schema dependency from `core-schema`.

## Recommended Direction
- Keep Python for aggregation and validation orchestration.
- Add lightweight test harness (pytest or shell fixtures) for release script behavior.
- Add docs link checker to reduce protocol drift.

## Why
- Maintains low complexity while increasing confidence.
- Fits current team workflows and existing script skillset.
