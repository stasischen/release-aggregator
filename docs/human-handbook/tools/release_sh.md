# Tool: `scripts/release.sh`

## Function
Shell wrapper for release aggregation command.

## What It Does
1. Accepts `--version` or `--output`.
2. Resolves defaults for `--pipeline-dist`, `--core-schema`, `--source-repo`, `--source-commit`.
3. Calls `scripts/release.py`.

## Example
```bash
./scripts/release.sh --version v1.2.3 --source-commit abc1234
```
