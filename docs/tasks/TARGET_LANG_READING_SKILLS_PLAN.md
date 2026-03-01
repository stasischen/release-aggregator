# TARGET_LANG_READING_SKILLS_PLAN

## Goal

建立獨立於 survival 對話層的 Reading 架構，讓課程能系統化訓練閱讀理解與證據定位能力。

---

## Scope

1. Reading Flow
- `pre-read`: 背景啟動、關鍵詞預熱
- `while-read`: gist/detail/inference/discourse
- `post-read`: summary/stance/transfer

2. Reading Contract
- text profile
- question blueprint
- evidence mapping
- reading rubric

---

## MVP Principles

1. 每題必須可追溯證據（evidence-based）。
2. 題型不只 literal，至少覆蓋 inference。
3. schema-first：先可被 generator/checker 消費，再優化題目品質。

---

## Deliverables

1. Reading node contract spec
2. Reading schemas for generator input
3. Reading gate rules for TLG-006
4. KO A1/A2 pilot report（2 units）

---

## Definition of Done

1. `TARGET_LANG_READING_SKILLS_TASKS.json` 任務完成並標記狀態。
2. Reading schemas 可被 generator 直接使用。
3. Gate 能攔截無證據、題幹對位不一致等 blocker。
4. Pilot 產出可行的 freeze 建議與缺陷分類。
