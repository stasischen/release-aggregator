---
description: Build, Sync, and Validate Game Content / 建置、同步與驗證遊戲內容
---

# Build Content Workflow (內容建置流程)

> ⚠️ **重要**: 請使用完整的 V4 管線，不要單獨執行 build。
> ⚠️ **IMPORTANT**: Use the complete V4 pipeline, don't run build alone.

**完整流程請參考**: `/v4_content_pipeline`

## Quick Reference (快速參考)

```bash
# 完整管線 (推薦)
python -m tools.v4 pipeline {lang}

# 或者按步驟執行 (詳見 v4_content_pipeline.md):
# 1. atomize → 2. extract → 3. classify → 4. translate → 5. sync → 6. build
```

## ❌ 避免 (DO NOT)

```bash
# 不要直接執行這些指令！
python3 tools/v4/v4_build.py {lang}   # 已棄用
python3 tools/run_pipeline.py {lang}  # 已棄用
```

---
**Last Updated**: 2026-01-13

