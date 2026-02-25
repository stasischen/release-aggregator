# B1 Candidate Review Handoff (2026-02-25)

## Context

目前正在進行 **B1 Dialogue Audit (B1-01~B1-25)** 的收尾與字典候選（Candidate）審查。
目標是確保 B1 的 Gold Standard 語法正確（無 Copula 污染）且符合新流程（Evidence Backfilled），並產出一個乾淨的 Staging Candidate 給後續全量 Build 使用。

## Accomplishments (Current Session)

1. **Repo Cleanup**: 已在 `content-ko` 提交 `b6e9eb08`，還原了先前誤觸發的 production atom 變更。
2. **Evidence Backfill**: 已在 `content-ko` 提交 `965b18d0`，補齊了 B1-01~B1-25 的 `review_preflight_ack.json` 與 `surgery_full_pass_attest.json`。
3. **QA Gate**: 驗證 `python scripts/ops/qa_gate.py --level B1` 已通過 (PASS)。
4. **Candidate Build**: 成功建立 B1-only candidate：`content/staging/dictionary_candidates/b1_review_20260225`。

## Current Findings & Blockers (Important)

在進行 `b1_review_20260225` 的候選審查時發現：

- **`일본하고` 依舊汙染**：在 `mapping.json` 中顯示為 `ko:n:일본+ko:v:하다+ko:e:고`。
- **Root Cause**: `fix_surgery.py` 第 130 行存在 typo：`atom = "ko:n:일본+ ko:p:하고"`（`+` 後面多了一個空格）。
- **Status**: 尚未修復此 typo，需由下一位接手。

## Remaining Tasks

1. **Fix Heuristic**: 修正 `content-ko` 根目錄下的 `fix_surgery.py` 第 130 行，移除 `ko:p:하고` 前的空格。
2. **Re-Apply B1-07**:
   - 執行 `python fix_surgery.py B1-07`。
   - 執行 `python scripts/review/orchestrator.py apply --lesson B1-07`。
3. **Rebuild Candidate**: 重新執行 `python scripts/ops/build_dictionary.py --gold-dir content/gold_standards/dialogue/B1 --stage-name b1_review_20260225_v2`。
4. **Verification**: 依照 `docs/SOPs/KO_DICT_CANDIDATE_REVIEW_CHECKLIST.md` 重新檢查 `mapping.json`。
5. **Report**: 輸出審查報告（PASS/FAIL），但**不要執行 promotion**。

## Artifacts Generated

- Stage: `E:\Githubs\lingo\content-ko\content\staging\dictionary_candidates\b1_review_20260225`
