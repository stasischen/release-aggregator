# Implementation Plan - KO-MAP-04: Dictionary & POS Fixes

本任務負責將 `KO-GEMINI-05` 的人工複核結果落實到辭典檔案中，並清理因規則引擎增強而產生的冗餘 Mapping。

## User Review Required

> [!IMPORTANT]
> 本任務涉及對 `content/source/ko/i18n/base/` 目錄下多個 `mapping_*.json` 檔案的直接修改（搬移 Lemma）。
> 任何 POS 搬移都會觸發 `scripts/ops/stage2_executor.py` 的重新計算。

## Decomposition Checklist (YAML)

```yaml
decomposition_check:
  request_scope: "落實 POS 複核結果，搬移 -되다 動詞，並清理冗餘 ko:phrase mappings。"
  phase_id: 04A
  target_repo: "content-ko"
  touched_paths: 
    - "content/source/ko/i18n/base/mapping_nouns.json"
    - "content/source/ko/i18n/base/mapping_verbs.json"
    - "content/source/ko/i18n/base/mapping_adjectives.json"
    - "content/source/ko/i18n/base/mapping_adverbs.json"
  dependency_prev_phase: "KO-GEMINI-05"
  boundary_statement: "One phase one repo. No cross-repo edits in this phase."
```

## Proposed Changes

### [Component] content-ko Dictionary Base

#### [MODIFY] [mapping_nouns.json](file:///e:/Githubs/lingo/content-ko/content/source/ko/i18n/base/mapping_nouns.json)

- 標記 `가까이`, `각각` 為 `DUAL` (暫定在 metadata 或透過 dual-mapping 處理，依 `KO-DICT-03` 合約)。

#### [MODIFY] [mapping_verbs.json](file:///e:/Githubs/lingo/content-ko/content/source/ko/i18n/base/mapping_verbs.json)

- [NEW] 移入來自 `mapping_adjectives` 的 `-되다` 動詞。
- [NEW] 移入來自 `mapping_adjectives` 的誤植動詞 (如 `나다`, `고민하다`)。

#### [MODIFY] [mapping_adjectives.json](file:///e:/Githubs/lingo/content-ko/content/source/ko/i18n/base/mapping_adjectives.json)

- [DELETE] 移除已確認為動詞的 Lemma。

#### [MODIFY] [mapping_adverbs.json](file:///e:/Githubs/lingo/content-ko/content/source/ko/i18n/base/mapping_adverbs.json)

- [DELETE] 移除誤植的名詞 (如 `가게`, `무게`)。

## Phase Breakdown

### Phase 04A: Systematic POS Migration

- 根據 `KO-GEMINI-05` 的 Backlog，執行檔案間的 Lemma 搬移。
- 特別處理 `-되다` 被動詞系列。

### Phase 04B: Redundant Mapping Cleanup

- 使用 `grep` 找出辭典中所有的 `ko:phrase` 與 `ko:word`。
- 檢查是否已可由當前 rules 解構。
- 移除確認冗餘的 entry（例如 `찾겠죠` -> `찾다` + `~겠죠`）。

### Phase 04C: Verification & Gates

- 執行 `scripts/ops/stage2_executor.py`。
- 確保 Coverage 不下降。
- 驗證 `unresolved_surface_count == 0`。

## Verification Plan

### Automated Tests

- `python3 scripts/ops/stage2_executor.py`
- 檢查 `runs/` 下生成的最新 QA report。
