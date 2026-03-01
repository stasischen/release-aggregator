# TLG Layer Integration Matrix v1

## Goal
提供 generator 可直接使用的課程組裝規則：先固定 Core，再依優先級掛載各技能 Layer。

## Integration Order
1. `core`
2. `listening`
3. `vocab_collocation`
4. `reading`
5. `pronunciation_prosody`
6. `writing`
7. `assessment`
8. `personalization`

## Mix Targets
- `A1-A2`: `core 70%`, `overlay 30%`
- `B1-C2`: `core 50%`, `overlay 50%`

## Node Mapping (Quick View)
- `L1/L2`: core + listening
- `L3`: core + reading
- `D1/G1`: core + vocab_collocation
- `G2`: core + grammar_progression
- `P3/P4`: core + grammar_progression + vocab_collocation
- `P5/P6`: core + pronunciation (P5/P6) + writing (P6)
- `R1`: assessment/personalization 主入口
- `X1/X2`: followup overlay 注入點（X1 偏聽說，X2 偏讀寫）

## Conflict Policy
- 先保留 `core` required elements。
- Overlay 衝突時：高優先級 layer 先保留。
- 超過節點 overlay budget 時：先丟低優先級 layer。

## Source of Truth
- JSON matrix: `docs/tasks/schemas/tlg_layer_overlay_matrix_v1.json`
- Reading architecture: `docs/tasks/TLG_013_READING_SKELETON_SPEC.md`
- Reading rubric: `docs/tasks/TLG_014_READING_RUBRIC_SPEC.md`
- Reading generator schema: `docs/tasks/schemas/tlg005_reading_generator_input_v1.schema.json`
