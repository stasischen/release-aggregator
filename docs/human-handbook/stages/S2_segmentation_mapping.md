# S2: Segmentation + Mapping (`content-ko`)
# S2：分詞與映射（`content-ko`）

## Goal / 目標
Produce reviewed segmentation/POS gold, then generate dictionary/mapping artifacts safely via staged candidates before promotion.
先完成已審核的分詞/POS 金標，再以 staged candidate 安全產生 dictionary/mapping 產物，最後才 promotion。

## Prerequisites / 前置條件
- S1 completed
- 已完成 S1
- Updated canonical source in `../content-ko`
- `../content-ko` canonical source 已更新
- Human reviewer has read required KO review docs (enforced by preflight ack)
- 人工審查者已閱讀 KO review 必讀文件（由 preflight ack 強制）

## Inputs / 輸入
- S1 canonical source artifacts
- S1 的 canonical source
- Existing dictionary/mapping resources
- 既有 dictionary/mapping 資源
- Existing gold standards and review run files (`data/reviews/runs/**`)
- 既有金標與 review run 檔案（`data/reviews/runs/**`）

## S2 Full Flow (Current) / S2 完整流程（現行）

### A. Review Preflight (Required) / Review 前置簽核（必須）

Purpose:
- Prevent agents/humans from skipping core segmentation standards before surgery/review.
- 防止 agent/人工在未讀核心規範時直接進行 surgery/review。

Required docs (hash-locked in ack):
- `content-ko/docs/SOPs/KO_DATA_STANDARDIZATION_PROTOCOL.md`
- `content-ko/docs/tech/KO_SEGMENTATION_RULES.md`
- `content-ko/docs/prompts/KO_REVIEW_EXPERT_GUIDANCE.md`

```bash
cd ../content-ko
python3 scripts/review/00_review_preflight.py list
python3 scripts/review/00_review_preflight.py ack \
  --lesson B2-05 \
  --reviewer <human_or_agent_id> \
  --confirm-phrase I_READ_REQUIRED_KO_REVIEW_DOCS
```

Notes:
- `scripts/review/orchestrator.py draft/apply` will fail if preflight ack is missing or stale.
- If any required doc changes, the old ack becomes invalid and must be re-acked.
- `scripts/review/orchestrator.py draft/apply` 若 preflight ack 缺失或過期會直接失敗。
- 任一必讀文件變更後，舊 ack 會失效，需重新 ack。

## How To Ask An Agent (Natural Language) / 如何用自然語言要求 Agent 執行 S2 審查

Use natural language, but include these fields clearly:
- lesson scope (which lesson(s))
- stop stage (run until where)
- review mode (must keep manual surgery **full-pass**)
- whether production promotion is allowed

建議用自然語言，但請清楚包含這些欄位：
- 課程範圍（哪些課）
- 停止階段（做到哪一步）
- 審查模式（必須保留 manual surgery **full-pass**）
- 是否允許 promotion 到 production

### Scope Expressions (Recommended) / 範圍表達（建議）

- Single lesson / 單課：`B2-05`
- Multiple lessons / 多課：`B2-05, B2-06, B2-08`
- Range (same level) / 區間（同級）：`B2-05 到 B2-08` / `B2-05~B2-08`
- Whole level / 整級：`B2 全部`
- Mixed list / 混合清單：`A2-01, A2-03, B1-02`

### Stop Stage Keywords (Recommended) / 停止階段關鍵字（建議）

- `只做 preflight + draft`
- `做到 surgery full-pass + apply`
- `做到 qa gate`
- `做到 dictionary candidate（不要 promotion）`
- `做到 promotion`

### Important Constraints To State / 建議明講的限制

- `surgery 要 full-pass，不是只看 residual`
- `先 engine-first remediation/lint，再人工 surgery`
- `未經我確認不要 promotion`
- `qa gate 沒過不要往下`

### Example Requests (Good) / 良好範例

1. `請跑 B2-05 的審查流程，做到 qa gate。surgery 要 full-pass，先 remediation/lint，再人工 review。不要 promotion。`
2. `幫我跑 B2-05 到 B2-08 的 review pipeline，逐課 preflight，surgery 全量審查，做到 dictionary candidate stage 即可。`
3. `請處理 A2-01、A2-03、B1-02，先做 draft + remediation/lint，人工 full-pass surgery 後 apply，再回報哪些課卡在 qa gate。`
4. `把 B2 全部課程跑到 qa gate；如果發現新規律切錯，先回流引擎/override，不要只在 surgery 重複手改。`

### Example Requests (Ambiguous; Avoid) / 容易誤解的說法（避免）

- `幫我看一下 B2`
- `把 review 跑完`
- `把有問題的修一修`

These are ambiguous because they do not specify scope, stop stage, or whether promotion is allowed.
這些說法會造成歧義，因為沒有指定範圍、停止階段、以及是否允許 promotion。

### B. Draft + Surgery Workspace / 初版草稿與 Surgery 工作檔

Purpose:
- Build draft gold and the `surgery_<LESSON>.json` work file for manual review.
- 產生 draft gold 與人工審查用 `surgery_<LESSON>.json`。

```bash
cd ../content-ko
python3 scripts/review/orchestrator.py draft --lesson B2-05
```

What is “surgery”?
- `surgery_<LESSON>.json` is the manual review work file (mid-stage), not final output.
- Surgery is **full-pass manual review** of the lesson rows, not a residual-only patch list.
- High-risk/residual rows should be reviewed first for efficiency, then reviewer must complete a full sweep of all rows.
- Human/agent edits the surgery file, then uses `apply` to merge back into gold.
- `surgery_<LESSON>.json` 是人工審查工作檔（中段），不是最終產物。
- Surgery 是該課程的**全量人工審查**，不是只修 residual 的 patch 清單。
- 可先看 high-risk/residual 提升效率，但之後必須完成全量逐列掃描。
- 在該檔完成審查後，再用 `apply` 回寫金標。

### C. Auto-remediation + Lint (Engine-first) / 自動修補與 Lint（引擎優先）

Purpose:
- Remove recurring engine-fixable segmentation/POS errors before manual review scales.
- Separate true errors from dictionary gaps.
- 先清掉可由引擎修復的規律錯誤，再讓人工聚焦；同時分離真錯誤與字典缺口。

```bash
cd ../content-ko
python3 scripts/ops/remediate_gold.py --level B2 --glob 'B2-*.jsonl'
python3 scripts/ops/lint_gold.py --level B2 --glob 'B2-*.jsonl'
```

If applying engine-fixable changes:

```bash
python3 scripts/ops/remediate_gold.py --level B2 --glob 'B2-*.jsonl' --apply
```

### D. Manual Surgery Review / 人工 Surgery 審查

Purpose:
- Fix residual segmentation/POS issues and ambiguous rows manually.
- Complete a full-pass review to catch newly discovered mistakes outside lint/heuristic coverage.
- 人工修正 residual 的切分/POS 與歧義項目，並以全量掃描補到 lint/heuristic 未覆蓋的新錯誤。

Typical work file:
- `../content-ko/data/reviews/runs/<LESSON>/surgery_<LESSON>.json`

### Manual Surgery Full-Pass Definition / Surgery 全量審查定義（必讀）

Full-pass means all of the following are true:
- Reviewer opens the lesson surgery file and reviews **every row** at least once (not only rows surfaced by scripts/lint).
- Reviewer may use risk ordering (fallback/lint-hit/low-confidence first), but must finish a complete row-by-row sweep afterward.
- Script outputs/reports may be used as **triage aids only**; they do **not** count as a full-pass by themselves.
- When a new recurring error pattern is discovered during the full sweep, reviewer records it and routes it back:
  - engine-fixable pattern -> tokenizer/rules remediation first, then rerun remediation/lint
  - non-engine lexical exception -> override/manual handling

Full-pass does **not** mean:
- Running a script that scans all rows and assuming the lesson is reviewed
- Reviewing only residual/lint-hit rows and skipping the rest
- 只跑腳本掃過全量資料就當作完成人工審查
- 只看 residual/lint 命中項目而未完成其餘列的逐列掃描

Practical review order (recommended):
1. High-risk rows first (fallback / lint-hit / low-confidence / conflict)
2. Full sweep of remaining rows
3. Record new patterns discovered during sweep
4. Re-run remediation/lint if engine/rule changes were made

Then apply:

```bash
cd ../content-ko
python3 scripts/review/orchestrator.py apply --lesson B2-05
```

After manual full-pass is complete, write the full-pass attestation (required for QA gate pass by default):

```bash
cd ../content-ko
python3 scripts/review/surgery_full_pass_attest.py write \
  --lesson B2-05 \
  --reviewer <human_or_agent_id> \
  --confirm-phrase I_COMPLETED_FULL_PASS_MANUAL_SURGERY
```

### E. QA Gate (Unified Gate Check) / QA Gate（統一通行證）

Purpose:
- Enforce preflight ack, surgery full-pass attestation, remediation/lint report freshness, and blocker rules before dictionary steps.
- 在進入字典步驟前，強制檢查 preflight ack、surgery 全量簽核、報告新鮮度與 blocker 規則。

```bash
cd ../content-ko
python3 scripts/ops/qa_gate.py \
  --lesson B2-05 \
  --level B2 \
  --glob 'B2-*.jsonl'
```

### F. Dictionary Candidate Build (Staging-first) / 字典候選產物建置（先進 staging）

Purpose:
- Prevent first-pass dictionary/mapping output from polluting production assets.
- 避免第一版 dictionary/mapping 直接污染正式資產。

```bash
cd ../content-ko
python3 scripts/ops/build_dictionary.py --stage-name b2_candidate_01
```

Output (staged candidate):
- `../content-ko/content/staging/dictionary_candidates/b2_candidate_01/content/core/dictionary/**`
- `../content-ko/content/staging/dictionary_candidates/b2_candidate_01/content/i18n/zh_tw/dictionary/**`
- `../content-ko/content/staging/dictionary_candidates/b2_candidate_01/content/i18n/zh_tw/mapping.json`
- `../content-ko/content/staging/dictionary_candidates/b2_candidate_01/build_manifest.json`

### G. Candidate Review + Promotion / 候選產物審查與升版

Purpose:
- Human verifies staged dictionary/mapping candidate, then explicitly promotes.
- 人工確認 staged dictionary/mapping 候選產物後，再明確 promotion。

Requirements before promotion:
- QA gate passed
- Candidate review passed
- Approval marker exists: `REVIEW_APPROVED` (in stage root)
- QA gate 通過
- 候選產物審查通過
- stage 根目錄存在核准標記 `REVIEW_APPROVED`

```bash
cd ../content-ko
python3 scripts/ops/promote_dictionary_candidate.py \
  --stage-dir content/staging/dictionary_candidates/b2_candidate_01 \
  --yes
```

## Outputs / 輸出
- Reviewed gold standards (`../content-ko/content/gold_standards/**`)
- QA reports (`../content-ko/reports/*_gold_remediation_report.*`, `*_gold_lint_report.*`, `*_qa_gate_report.*`)
- Staged dictionary candidate (`../content-ko/content/staging/dictionary_candidates/<stage>/**`)
- Promoted production dictionary/mapping (after explicit promotion):
  - `../content-ko/content/core/dictionary/**`
  - `../content-ko/content/i18n/zh_tw/dictionary/**`
  - `../content-ko/content/i18n/zh_tw/mapping.json`

## Exit Gate / 驗收門檻
1. Preflight ack exists and matches current required-doc hashes.
1. preflight ack 存在且與目前必讀文件雜湊一致。
2. Gold remediation/lint reports are fresh and reviewed.
2. gold remediation/lint 報告為最新且已檢查。
3. Manual surgery full-pass is completed (human-reviewed, not script-only).
3. Manual surgery 全量審查已完成（人工逐列，不可僅靠腳本）。
4. QA gate passes (no blocker findings beyond threshold).
4. QA gate 通過（blocker 未超過門檻）。
5. Dictionary output is reviewed in staged candidate before promotion.
5. dictionary 輸出先於 staged candidate 完成審查後才 promotion。
6. Promoted artifacts are usable by S3 build.
6. promotion 後產物可被 S3 建置使用。

## Troubleshooting / 排錯
1. `orchestrator draft/apply` fails on preflight:
1. `orchestrator draft/apply` 因 preflight 失敗：
   - Run `scripts/review/00_review_preflight.py list`
   - Re-read required docs and run `ack`
   - 執行 `list`，重新閱讀必讀文件後再 `ack`
2. QA gate fails:
2. QA gate 失敗：
   - Regenerate remediation/lint reports
   - Fix blocker findings (or explicitly adjust threshold with documented reason)
   - 重跑 remediation/lint 報告，修正 blocker（或記錄原因後調整門檻）
3. Promotion refused:
3. promotion 被拒：
   - Confirm stage path is correct
   - Ensure `REVIEW_APPROVED` marker exists in stage root
   - 確認 stage 路徑正確，並建立 `REVIEW_APPROVED` 標記
