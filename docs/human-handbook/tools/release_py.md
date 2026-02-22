# Tool: `scripts/release.py`
# 工具：`scripts/release.py`

## Function / 功能
Aggregate artifacts, hash files, generate and validate manifest.
聚合產物、計算雜湊、產生並驗證 manifest。

## What It Does / 做什麼
1. Walks `--pipeline-dist` for `.json`, `.ogg`, `.mp3`.
1. 掃描 `--pipeline-dist` 下的 `.json`/`.ogg`/`.mp3`。
2. Copies files to `--output` preserving structure.
2. 保留目錄結構複製到 `--output`。
3. Computes SHA256 and writes `global_manifest.json`.
3. 計算 SHA256 並寫入 `global_manifest.json`。
4. Validates manifest via `core-schema` validator.
4. 使用 `core-schema` validator 驗證 manifest。

## Required Args / 必填參數
- `--pipeline-dist`
- `--output`
- `--core-schema`
- `--source-repo`
- `--source-commit`
