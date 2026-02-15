---
description: Content Integrity Check / 內容完整性檢查
---

# Content Integrity Check Workflow

This workflow is designed to prevent data loss where CSV files contain fewer lines than their source Yarn files. This is critical to ensure no dialogue is missing in the game.

## 🔍 The Tool

`tools/v4/qa/check_content_status.py` compares:

- **Expected Lines**: Extracted from `#line:ID` tags in Yarn files (`0_yarn`).
- **Actual Lines**: Extracted from `line_id` column in V5 Full View CSVs (`5_full_view`).

## 🛠️ How to Run

(Currently using legacy checker, it will be updated to V5 native soon)

```bash
python tools/v4/qa/check_content_status.py {lang}
```

## 🚨 Troubleshooting "Missing Lines"

If the tool reports `❌ Missing X lines!`:

### Option A: Synchronize Databases (V5 Recommended)

Safe and preserves existing data.

```bash
python -m tools.v5.core.update_db {lang}
python -m tools.v5.core.merger {lang}
```

### Option B: Manual Fix

1. Open the source Yarn file to find the missing `#line:ID` blocks.
2. Manually add the missing rows to the respective specialized DB in `1_translation/` and `2_atoms/`.
3. Re-run `merger` to update the Full View.

### Option C: Legacy/Reference Files

If the missing lines are from a "REFERENCE BLOCK" or "MIRROR" in Yarn that shouldn't be in the game, verify if the Yarn parser is counting them incorrectly. The current tool counts ALL unique `#line:` IDs.

## ✅ When to Run

- **Before major edits**: To ensure you are working on a complete file.
- **After bulk generation**: To verify the generator didn't drop lines.
- **Pre-commit**: validation step.
