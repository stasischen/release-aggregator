# Audit Report: [Language] Phase 3 (Mapping)

**Date**: [YYYY-MM-DD]
**Status**: 🔴 PENDING / 🟢 COMPLETE

> [!IMPORTANT]
> Before starting this audit, you MUST read the Golden Sample for Phase 3:
> [Golden Sample: Korean Phase 3](file:///e:/Githubs/Lingourmet_universal/.agent/workflows/golden_samples/audit_report_ko_p3.md)

## 📊 Summary

- **Total Unique Chunks**: PENDING
- **Collisions Detected**: PENDING
- **Collisions Resolved**: 0
- **Manual Locks (Manual tags)**: 0

## 📝 Collision Resolution Log (Homonyms)

| Surface | Assigned Atom ID | Context/Reason             | Status |
| :------ | :--------------- | :------------------------- | :----: |
| [Text]  | [ID]             | [Linguistic Justification] |   🟢   |

## 🔍 Coverage & Consistency Check

- [ ] **Number-Unit Split**: Verified that all numbers are split from units (e.g. 3월 -> 3 + 월).
- [ ] **Counter Tagging**: Verified that all measure words (量詞) are tagged as `pos: M`.
- [ ] **Phrase Hardening**: Verified that compound phrases (e.g. 아이스 아메리카노) are split into dictionary atoms.
- [ ] **Manual Locks**: Verified that sensitive resolutions are locked with `tags: manual`.
- [ ] **Zero UNK**: Confirmed no `ko_UNK` ghost atoms remain.
