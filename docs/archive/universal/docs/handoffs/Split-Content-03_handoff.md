# Split-Content-03: Content Pipeline

**Status**: ✅ DONE
**Commit**: (See final commit)
**Date**: 2026-02-14

## 1. Overview
Created `content-pipeline` to transform source content into production artifacts.
Currently supports `ko__zh_tw` pair.

## 2. Validation & Build Flow
1. **Input**: `content-ko/content/source/ko__zh_tw`
2. **Validation**: Check against `core-schema` (dialogue schema).
3. **Build**: Copy to `dist/ko/zh_tw/dialogue/{id}.json`.

## 3. Usage
```bash
# Verify pipeline (CI)
./ci/smoke_test.sh

# Run manually
python3 pipelines/build_ko_zh_tw.py \
    --input ../content-ko \
    --output dist \
    --core-schema ../core-schema
```

## 4. Deliverables
- `pipelines/build_ko_zh_tw.py`
- `ci/smoke_test.sh`
- `requirements.txt`

## 5. Next Steps
- `Split-Content-04` (Release Aggregator) to package these artifacts into a global release.
