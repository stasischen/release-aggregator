# TLG Generator Routing Matrix v1

## Purpose
定義「不同課程類型」在批次生成時，應該由哪一種 generator 負責，並規範 fallback/retry。

## Core Idea
- 不是單一模板生成所有內容。
- 每個 node suffix 有 primary generator。
- layer overlay 可以覆蓋 node 的 payload 要求。
- 所有輸出都必須經過 TLG-006 gate。
- 每次生成都必須載入 `target_lang` 對應的 `lang_generation_profile`（語系+文體控制）。

## Primary Mapping
- `L1/L2`: listening generator
- `L3`: reading generator
- `P4`: repair generator
- `P5`: speaking generator
- `P6`: writing generator（fallback speaking）
- `R1`: assessment generator（可混 reading/listening）

## Overlay Rules
- `reading` 只能掛 `L3/R1/X2`
- `listening` 只能掛 `L1/L2/R1/X1`
- `pronunciation_prosody` 只能掛 `P5/P6/X1`
- `repair` 只能掛 `P4`

## Batch Execution
1. 讀 manifest
2. 解析 `target_lang` 並載入 `lang_generation_profile`
3. 依 node suffix 路由到對應 generator
4. 套用 layer override + genre/register constraints
5. 跑 TLG-006 gate（含語系/文體檢查）
5. fail -> retry/fallback -> manual review

## Source of Truth
- JSON: `docs/tasks/schemas/tlg_generator_routing_matrix_v1.json`
- Lang profile schema: `docs/tasks/schemas/lang_generation_profile_v1.schema.json`
- Lang profiles:
  - `docs/tasks/lang_profiles/ko_generation_profile_v1.json`
  - `docs/tasks/lang_profiles/th_generation_profile_v1.json`
