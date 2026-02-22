# Artifact Map

## Main Paths

| Phase | Path Pattern | Owner |
|---|---|---|
| Build output | `../content-pipeline/dist/**` | `content-pipeline` |
| Staging output | `staging/<version>/**` | `release-aggregator` |
| Manifest | `staging/<version>/global_manifest.json` | `release-aggregator` |
| Frontend intake | (frontend repo asset paths) | `lingo-frontend-web` |

## Manifest Package Entry

`global_manifest.json` package entries include:
- `id`
- `version`
- `path`
- `hash` (`sha256:*`)
- `provenance` (`source_repo`, `source_commit`, `pipeline_version`, `schema_version`, `built_at`)
