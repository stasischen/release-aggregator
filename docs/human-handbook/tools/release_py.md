# Tool: `scripts/release.py`

## Function
Aggregates artifacts from pipeline `dist` into staging and generates validated manifest.

## What It Does
1. Walks `--pipeline-dist` for `.json`, `.ogg`, `.mp3` files.
2. Copies files into `--output` with directory preservation.
3. Computes SHA256 hash for each file.
4. Writes package entries into `global_manifest.json`.
5. Validates manifest using `core-schema` validator and schema.

## Required Arguments
- `--pipeline-dist`
- `--output`
- `--core-schema`
- `--source-repo`
- `--source-commit`
