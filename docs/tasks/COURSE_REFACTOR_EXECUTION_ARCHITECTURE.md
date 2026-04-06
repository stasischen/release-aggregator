# Course Refactor Execution Architecture

## Goal

本文件定義目前課程重構的實際執行順序，避免同時在內容回收、前端承接、課程重構、legacy 修復四個層面交叉施工。

目前的工作目標不是一次把所有課程重寫完，而是先建立一條可回收、可承接、可重構、可驗證的主線。

## Core Decision

執行順序固定為：

```text
1. 先把既有 dialogue / video 拉回 staging
2. 再把新版課程結構接到 viewer / frontend intake
3. 再按課型逐 unit 重構
4. 最後才回頭處理 legacy L0 V4 -> V5 遷移
```

原因：

- B1 以上 chunk segmentation 仍有殘餘問題，現階段不適合把全部內容直接推進 production。
- 如果前端還沒有穩定承接新版 unit contract，任何課程重構都會變成一次性的 fixture 工作。
- 如果在重構課程的同時大規模修 legacy schema / mapping，返工成本會快速上升。

## Execution Layers

### Layer 1: Staging Recovery

目的：
- 先恢復現有內容可見、可盤點、可抽樣驗證。
- 不要求 production-ready，只要求可被 intake。

內容：
- `dialogue`
- `video`
- 之後可擴展到 `article`

規則：
- 一律標記 `staging_only`
- 一律帶 `readiness_flag`
- 一律帶 `segmentation_status`
- 不直接進 production bundle

對應 task：
- `LEARNING_LIBRARY_CONTENTKO_MIGRATION`
- `GOLDEN_STANDARD_RECONCILIATION`
- `STABLE_TEST_RCA`

### Layer 2: Frontend Contract Integration

目的：
- 讓 viewer / frontend 先能穩定吃新版課程結構。
- 將 source-build artifact 與 hand-authored preview fixture 分離。

規則：
- viewer 以 source-build artifact 為正式輸入
- renderer 不直接依賴 preview-only fields
- i18n fallback 只允許存在於 adapter 層
- Learning Library / frontend intake 若仍在早期且尚未全面承接，可先升級為 `target core + support i18n` 分包 contract；此類升級視為降低後續返工的主線架構修正，不視為任意變更 artifact contract

對應 task：
- `MODULAR_VIEWER_REFACTOR`
- `LEARNING_LIBRARY_CONTENTKO_MIGRATION` (`LLCM-006~008`)

### Layer 3: Unit-by-Unit Course Refactor

目的：
- 以新版 unit contract 為基礎，按課型逐單元重構。
- 不一次改整個 level，而是先跑 pilot，再做同類型擴張。

課型：
- `dialogue / travel / daily-life`
- `video`
- `grammar-heavy`
- `article / reading`

建議順序：
1. `dialogue / travel / daily-life`
2. `video`
3. `grammar-heavy`
4. `article / reading`

課型重點：

`dialogue / travel / daily-life`
- 主軸：聽說
- 結構：input -> comprehension -> transform -> repair -> guided speaking

`video`
- 主軸：聽力、重播、shadowing、情境理解
- 優先做 staging playback + subtitle/sentence alignment

`grammar-heavy`
- 主軸：讀寫
- 結構：input -> pattern/rule -> rewrite -> contrast -> review

`article / reading`
- 主軸：閱讀理解、證據定位、推論、摘要

對應 task：
- `TARGET_LANG_COURSE_FACTORY`
- `COURSE_MODULE_COMPOSITION`

### Layer 4: Skill-Layer Expansion

目的：
- 在 unit factory 穩定後，為各課型補上更深的技能層。

對應 task：
- `TARGET_LANG_AUDIO_SKILLS`
- `TARGET_LANG_READING_SKILLS`
- `TARGET_LANG_WRITING_SKILLS`
- `TARGET_LANG_VOCAB_COLLOCATION`
- `TARGET_LANG_GRAMMAR_PROGRESSION`
- `TARGET_LANG_ASSESSMENT_LAYER`
- `TARGET_LANG_PERSONALIZATION_LAYER`

原則：
- 這些不作為起手式
- 必須晚於 Layer 2 / Layer 3

### Layer 5: Legacy Backfill

目的：
- 把舊的 L0 V4 課程安全遷回現有 V5 生態。

對應 task：
- `CONTENT_V5_MIGRATION_L0`

原則：
- 這條先獨立保留
- 不與 Layer 1~3 並行搶資源
- 等 source-build / viewer / unit contract 穩定後再推

## Task Mapping Summary

```text
Layer 1 內容回收
  -> LEARNING_LIBRARY_CONTENTKO_MIGRATION
  -> PRODUCTION_RELEASE_GATING
  -> GOLDEN_STANDARD_RECONCILIATION
  -> STABLE_TEST_RCA

Layer 2 前端承接
  -> MODULAR_VIEWER_REFACTOR
  -> LEARNING_LIBRARY_CONTENTKO_MIGRATION (frontend intake)

Layer 3 單元重構
  -> TARGET_LANG_COURSE_FACTORY
  -> COURSE_MODULE_COMPOSITION

Layer 4 技能深化
  -> TARGET_LANG_AUDIO_SKILLS
  -> TARGET_LANG_READING_SKILLS
  -> TARGET_LANG_WRITING_SKILLS
  -> TARGET_LANG_VOCAB_COLLOCATION
  -> TARGET_LANG_GRAMMAR_PROGRESSION
  -> TARGET_LANG_ASSESSMENT_LAYER
  -> TARGET_LANG_PERSONALIZATION_LAYER

Layer 5 legacy 補回
  -> CONTENT_V5_MIGRATION_L0
```

## Immediate Execution Recommendation

當前實際優先順序：

1. 完成 `LEARNING_LIBRARY_CONTENTKO_MIGRATION` 的 staging / frontend intake 收尾
2. 啟動 `MODULAR_VIEWER_REFACTOR`
3. 啟動 `TARGET_LANG_COURSE_FACTORY` 的 pilot unit 路徑
4. 視 pilot 結果再開 `COURSE_MODULE_COMPOSITION`
5. 最後再回到 `CONTENT_V5_MIGRATION_L0`

## Out of Scope

本文件不處理：

- 單一語言的 morphology / mapping 細節修復
- B1+ segmentation 的規則設計本身
- production release checklist 細節
- 單一前端頁面的樣式調整
