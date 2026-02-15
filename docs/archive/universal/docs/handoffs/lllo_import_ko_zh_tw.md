# Split-Content-02-LLLO: LLLO Import (ko -> zh_tw)

**Status**: ✅ DONE
**Commit**: (See final commit)
**Date**: 2026-02-14

## 1. Overview
Established the 1-to-1 source structure for `ko__zh_tw` pair and implemented the import mechanism.

## 2. Source Structure
```
content-ko/
├── content/
│   └── source/
│       └── ko__zh_tw/
│           ├── dialogue/  (Conversational content)
│           ├── article/   (Reading material)
│           ├── video/     (Video transcripts)
│           ├── teaching/  (Explanations)
│           └── grammar/   (Grammar points)
└── mappings/
    └── import_map_ko__zh_tw.json
```

## 3. Usage
```bash
# Import from LLLO repo
bash scripts/import_lllo.sh --pair ko__zh_tw --from /Users/ywchen/Dev/lllo
```

## 4. Verification
The script generates a valid JSON artifact in `content/source/ko__zh_tw/dialogue/`.
This file is ready for schema validation (next step: wire schema).

## 5. Next Steps
- Implement `Split-Content-03` to build these source files into production artifacts.
