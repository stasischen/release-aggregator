# CMOD-010 — Modular Curriculum Freeze Recommendation (UNITFAC-001 v0.1)

## Status
- **Status**: Draft / Recommendation
- **Task Ref**: `CMOD-010`
- **Target Standard**: `UNITFAC-001 v0.1`
- **Date**: 2026-04-17

## 1. Executive Summary

基於 `CMOD-001` 到 `CMOD-013` 的研發成果，本文件建議正式凍結 **UNITFAC-001 v0.1** 規格。此版本主要聚焦於「互動模式宣告」與「完成判準一致性」，旨在解決 V0 階段內容與互動過度耦合、難以擴充多種練習方式的問題。

## 2. Include List (應納入凍結範疇)

以下模組化契約已完成驗證，應作為 `v0.1` 以上單元的強制性標準。

### A. 強制性元數據 (Mandatory Metadata)
對於所有 `v0.1` 單元，凡具有交互行為之節點（即 `learning_role` 為 `controlled_output`、`immersion_output` 或任何具備非 `none` 之 `output_mode` 者），必須包含：
- **`interaction_modes`**: 宣告該內容支援的回答能力路徑（如 `["response_builder", "guided_typing"]`）。
- **`completion_rules`**: 明確定義節點完成的門檻（如 `min_attempts`, `required_modes`）。

對於純輸入型節點（Input Carriers），建議顯式宣告 `interaction_modes: ["none"]` 以求結構對齊，但 `v0.1` 階段暫不強制報錯。

### B. 互動契約 (Interaction Contract)
句子級別的互動行為應統一使用 `interaction_contract` 結構，並支援以下標準位置：
- **`dialogue`**: `turns` 或 `scenes[].turns` 中的每一行。
- **`article`**: `paragraphs[].sentences` 中的每一句。
- **`video_transcript`**: `lines` 中的每一行。
- **`none` (Node level)**: 頂層直接掛載（適用於單句練習卡）。

標準動作清單：`listen`, `repeat`, `shadow`, `type`。

### C. 角色與輸出權責 (Role-Output Decoupling)
- **`learning_role`**: 定義該節點在教學序列中的位置（Pedagogical Intent）。
- **`output_mode`**: 僅作為單元執行時的「預設分發器」（Dispatcher），其值必須存在於 `interaction_modes` 之中。

### D. 驗證強制化
`mockup_check.py` 已實施嚴格校驗：
- `v0.1` 單元缺失模組化元數據將報為 **ERROR**。
- `output_mode` 與 `interaction_modes` 的成員關係不一致將報為 **ERROR**。
- `interaction_contract` 缺失必要欄位（如 `audio_ref` 或 `target_surface`）將報為 **ERROR**。

## 3. Defer List (延後 / 暫緩範疇)

以下部分雖有初步定義，但尚未完全穩定或涉及複雜自動化，建議在 `v0.1` 中保持 **Optional** 或暫緩凍結：

- **`review_policy` 自動化細節**:
  - `intensity`, `spacing_semantics` 的具體數學模型與後台調度 logic。
  - `v0.1` 僅凍結元數據結構，不強制實施排程。
- **`teaching_blocks` 完整遷移**:
  - 目前保留 `grammar_note.sections` 作為過渡結構，不強制要求全面遷移至 `teaching_blocks`。
- **影片逐字稿 (`video_transcript`) 的進階實施**:
  - 雖然契約已定義，但大規模生產的工具鏈（Atomizer to Transcript）尚在優化中。
- **Anchor Linking (`segmentation_anchor_links`)**:
  - 複雜的字典下鑽路徑自動生成 logic 延後至 `v0.2`。

## 4. Migration Guide (V0 漸進式升級)

現有 V0 單元若需升級至 V1 契約，請遵循以下步驟：

1. **版本宣告**: 將 `version` 改為 `"unit_blueprint_v0.1"`。
2. **輸出節點加固**:
   - 將原本的 `output_mode` 加入 `interaction_modes` 陣列。
   - 補齊 `completion_rules`，建議預設值為：
     ```json
     "completion_rules": {
       "required_modes": ["<current_output_mode>"],
       "min_attempts": 1,
       "pass_policy": "manual_mark_after_required_modes"
     }
     ```
3. **句子動作升級**:
   - 若內容涉及 `dialogue`，將 `audio_ref` 移入 `interaction_contract.payload`。
   - 顯式標記 `actions`（預設建議為 `["listen", "repeat"]`）。
4. **驗證**:
   - 執行 `python scripts/mockup_check.py <file>`，確保無 **CMOD_** 前綴的錯誤。

## 5. Definition of Done for UNITFAC-001 v0.1

- [x] `core-schema` 更新並包含上述元數據定義。
- [x] `mockup_check.py` 正式開啟強制校驗（已完成）。
- [x] `A1-U05` Pilot 單元通過 100% 校驗並作為 Reference 存檔。
- [x] 所有撰寫模板 (`UNITFAC_005`) 更新完畢。
