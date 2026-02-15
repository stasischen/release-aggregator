# Audit Report: {Language} (Phase {N})

**Date**: {YYYY-MM-DD}
**Reviewer**: {Name}
**Evidence**: `scan_{lang}.log` (Attach Scan Logs!)

**Status Legend**:

- 🟢 **VERIFIED**: Passed Automated Scan AND Human Visual Semantic Check.
- ⚪ **PENDING**: Not yet checked.
- 🔴 **FAIL**: Needs Fix.

## 📊 Summary

- **Total Files Checked**: {N}
- **Issues Found**: {N}
- **Status**: ⚪ (Pending) / 🟢 (Pass)

## 🔍 Evidence-Based Validation

> **Note**: Replace `{Target N}` with the actual Big 5 language codes for this source language (e.g., `zh_TW`, `en`, `ja`, `es`, `id` for Korean).

| Target         | Command                                     | Result   |
| :------------- | :------------------------------------------ | :------- |
| **{Target 1}** | `tools.v5.audit_view ... {target_1} --scan` | {Result} |
| **{Target 2}** | `tools.v5.audit_view ... {target_2} --scan` | {Result} |
| **{Target 3}** | `tools.v5.audit_view ... {target_3} --scan` | {Result} |
| **{Target 4}** | `tools.v5.audit_view ... {target_4} --scan` | {Result} |
| **{Target 5}** | `tools.v5.audit_view ... {target_5} --scan` | {Result} |

## 📝 Audit Queue & Verification

| File Name    | {Target 1} | {Target 2} | {Target 3} | {Target 4} | {Target 5} | Visual Verification Notes |
| :----------- | :--------: | :--------: | :--------: | :--------: | :--------: | :------------------------ |
| `{file}.csv` |     ⚪     |     ⚪     |     ⚪     |     ⚪     |     ⚪     | Pending review.           |

## 🛠️ Action Items / Fix Log

- [ ] {Action Item}
