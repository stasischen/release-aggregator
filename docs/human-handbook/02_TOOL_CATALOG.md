# Tool Catalog (Current)

Only tools verified in active scripts/runbooks are listed here.

## Aggregator Tools

| Tool | Location | Function |
|---|---|---|
| Release CLI wrapper | `scripts/release.sh` | Parses release args and invokes Python aggregator |
| Release aggregator | `scripts/release.py` | Copies artifacts, hashes files, writes/validates `global_manifest.json` |
| Viewer sync | `scripts/viewer/sync_core_i18n_viewer_data.py` | Syncs staged core/i18n data into viewer data files |
| Control tower launcher | `scripts/ops/start_lingo_control_tower.sh` | Starts zellij control-tower layout |

## Supporting System Tools

| Tool | Repo | Function |
|---|---|---|
| Schema validator | `core-schema/validators/validate.py` | Validates manifest and contracts |
| Build pipeline entrypoints | `content-pipeline` | Produces release artifacts under `dist/` |

## Tool Detail Pages

- `docs/human-handbook/tools/release_sh.md`
- `docs/human-handbook/tools/release_py.md`
- `docs/human-handbook/tools/viewer_sync.md`
- `docs/human-handbook/tools/control_tower_start.md`
