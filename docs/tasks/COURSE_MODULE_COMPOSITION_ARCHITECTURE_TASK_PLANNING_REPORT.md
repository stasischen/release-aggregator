# COURSE_MODULE_COMPOSITION: Architecture & Task Planning Report

本報告針對 `CMOD-001~010` 的架構設計與任務規劃進行總結，嚴格對齊 `COURSE_MODULE_COMPOSITION_PLAN.md` 術語與既存契約邊界。

## 1. 任務執行順序建議

建議採「職責邊界 -> 擴充提案 -> 契約同步 -> 工具整合 -> 驗證 -> 下代建議」的路徑：

1. 第一階段：架構約束 (`CMOD-001` + `CMOD-002`) - 確立三層模型職責。
2. 第二階段：擴充提案 (`CMOD-003`, `CMOD-004`, `CMOD-005`) - 在三層架構約束下，定義具體元數據。
3. 第三階段：命名與語意對齊 (`CMOD-006`) - 統一 `repair_practice` 等欄位。
4. 第四階段：模板與工具鏈整合 (`CMOD-007` + `CMOD-008`) - 將提案轉化為生產力工具。
5. 第五階段：Pilot 單元驗證 (`CMOD-009`) - 基於 `A1-U05` 實測。
6. 第六階段：演進建議 (`CMOD-010`) - 針對下一個契約邊界提出建議。

## 2. 任務清單

| ID | Task Goal (一句話目標) | Deliverable (交付物) | Dependencies |
| :--- | :--- | :--- | :--- |
| `CMOD-001` | 定義 Content/Interaction/Review 三層職責，將 `dialogue` / `video` 定位為 input carriers。 | `CMOD_001_THREE_LAYER_MODEL_SPEC.md` | - |
| `CMOD-002` | 映射既存 node taxonomy 到三層模型角色，區分教學 payload 與支援表面。 | `CMOD_002_NODE_MAPPING_MATRIX.md` | `CMOD-001` |
| `CMOD-003` | 提出 `interaction_modes` contract note，支援單一節點的多路徑回答模式。 | `interaction_modes` contract note | `CMOD-001`, `CMOD-002` |
| `CMOD-004` | 提出 `review_policy` contract note（CMOD 層級），定義與 UI 解耦的複習元數據。 | `review_policy` contract note | `CMOD-001`, `CMOD-002` |
| `CMOD-005` | 提出 `completion_rules` contract note，建立適用於引導產出節點的判定標準。 | `completion_rules` contract note | `CMOD-001`, `CMOD-002`, `CMOD-003` |
| `CMOD-006` | 執行跨文檔語意校準，統一 `repair_practice`, `trigger_type`, `repair_goal` 的命名與對應邊界。 | alignment patch list | `CMOD-005`, `PEDOPT-009` |
| `CMOD-007` | 更新 `UNITFAC-005` 模板，引導作者在現有框架下填寫三層擴充欄位。 | updated `UNITFAC_005` templates | `CMOD-006` |
| `CMOD-008` | 在 `mockup_check.py` 中實現 warning-first 規則，偵測缺失的三層模組元數據。 | `mockup_check.py` updates | `CMOD-007` |
| `CMOD-009` | 套用提案元數據至 `A1-U05` Pilot，驗證既存渲染器的向下相容性。 | `A1-U05` fixture apply | `CMOD-008` |
| `CMOD-010` | 針對下一代契約邊界提出 include/defer freeze recommendation。 | `CMOD_010_FREEZE_RECOMMENDATION.md` | `CMOD-009` |

## 3. 目前不能做的部分

1. Hard Schema Lock (v0.1): 三層擴充欄位在 CMOD 線上維持為 proposal level，不強制寫死於已 frozen 的 `UNITFAC-001 v0.1` 核心結構。
2. Implementation: 所有提案僅限於契約定義，不包含 item bank 的排程實作或前端渲染程式碼。
3. Advanced Segmentation: `segmentation_anchor_links` 屬後續規劃，延後至 `CMOD-011+` 執行，本階段不處理細粒度錨點連結。

## 4. 與現有 Docs 衝突/需對齊的地方

1. UNITFAC-001 v0.1 邊界定位: 既存文件已凍結 v0.1，`CMOD-010` 只應定位為針對「下一個契約邊界」之建議。
2. review_policy 語意分層: 區分 CMOD 的複習策略提案與 `TLG-025` item bank 已有的排程欄位，前者為提案階層，後者為既存實作欄位。
3. `source_refs` 硬約束: CMOD 線明確禁止將 `source_refs` 用於 UI 跳轉，必須維持為單向知識溯源。
4. Metadata 命名統一: 修正與對齊 `repair_practice`, `trigger_type`, `repair_goal` 在契約、模板與檢查器間的落差。
5. `grammar_note.sections`: 於 `UNITFAC-005` 註記其為過渡期形狀，以維持與既存渲染器的相容性。

