# Wave 2 / Batch 002 Manifest: Beginner Grammar

This batch targets 15 high-frequency, low-risk items from `youtube_beginner_grammar/clean_md`.

## 1. Candidate Inventory

| ID | Source | Target Slug | Subcategory | Status | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | 009/023 | `dative` | `particle` | **READY** | Essential A1 particle. High frequency. |
| **02** | 025 | `source_from` | `particle` | **READY** | Complement to dative. Low risk. |
| **03** | 019 | `musun` | `determiner` | **READY** | Basic question word (What kind of). |
| **04** | 021 | `purpose_path` | `ending` | **READY** | "Go/Come in order to". Clear structure. |
| **05** | 028 | `progressive` | `tense` | **READY** | "-고 있다". Core tense missing from Wave 1. |
| **06** | 032 | `adj` | `modifier` | **READY** | "ㄴ/은" modifier. Essential structure. |
| **07** | 033 | `verb_present` | `modifier` | **READY** | "는" modifier. Essential structure. |
| **08** | 042 | `negative` | `request` | **READY** | "-지 마세요". Basic request form. |
| **09** | 062 | `polite` | `request` | **READY** | "-(으)세요". Basic request form. |
| **10** | 051 | `allow` | `permission` | **READY** | "-아/어도 되道". High frequency. |
| **11** | 052 | `prohibit` | `permission` | **READY** | "-(으)면 안 되다". Companion to allow. |
| **12** | 054 | `want` | `desire` | **READY** | "-고 싶다". Essential A1 expression. |
| **13** | 068 | `wish` | `desire` | **READY** | "-았/었으면 좋겠다". High value. |
| **14** | 063 | `benefactive` | `ending` | **READY** | "-아/어 주다". Help/Auxiliary verb. |
| **15** | 058 | `suggestion` | `ending` | **READY** | "-(으)ㄹ까요?". High frequency suggestion. |

## 2. Skipped Items (Rationale)

- **001/002/003**: Already in `content-ko` (Wave 1).
- **004/005/006/007/008**: Already in `content-ko` (Wave 1).
- **013/014/015/016**: Already in `content-ko` (Wave 1).
- **027/031**: Already in `content-ko` (Wave 1).
- **045/046**: Already in `content-ko` (Wave 1).
- **072-080**: Connectors/Connective endings; deferred to Wave 3 for deeper semantic check.
- **114 (아/어지다)**: State transition; deferred to Wave 5.
- **115 (아/어하다)**: Emotional state; deferred to Wave 5.

## 3. Implementation Plan

For each item:
1.  Read `youtube_beginner_grammar/clean_md/*.md`.
2.  Extract Title (Chinese), Summary, Explanation, and Example Bank (KO/ZH).
3.  Clean up: Remove video-specific text ("請按讚", "金老師"), clear OCR/mixed-script corruption.
4.  Standardize: Use `explanation_md_zh_tw` for usage rules.
5.  Generate `id`: `kg.grammar.{subcategory}.{slug}`.
6.  Write to `content-ko/content/core/learning_library/knowledge/grammar/{subcategory}/...`.
7.  Write to `content-ko/content/i18n/zh_tw/learning_library/knowledge/grammar/{subcategory}/...`.

## 4. Verification

- Run `verify_reports.py`.
- Run `audit_mixed_script.py`.
