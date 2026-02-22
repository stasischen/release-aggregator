# Tool: `scripts/release.sh`
# 工具：`scripts/release.sh`

## Function / 功能
Shell wrapper for release aggregation.
發版聚合 shell 包裝器。

## What It Does / 做什麼
1. Accepts `--version` or `--output`.
1. 接收 `--version` 或 `--output`。
2. Resolves defaults for dist/schema/source fields.
2. 補齊 dist/schema/source 預設值。
3. Invokes `scripts/release.py`.
3. 呼叫 `scripts/release.py`。

## Example / 範例
```bash
./scripts/release.sh --version v1.2.3 --source-commit abc1234
```
