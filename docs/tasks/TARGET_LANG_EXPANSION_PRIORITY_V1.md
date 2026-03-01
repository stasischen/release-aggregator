# TARGET_LANG_EXPANSION_PRIORITY_V1

## Goal

文件化「可先擴張哪些語言」的決策基準與分梯隊策略。  
本文件僅作規劃依據，不代表立即實作承諾。

---

## Decision Criteria

語言優先順序以以下四項綜合評估：

1. **Learner Demand**: 學習者規模與市場需求。
2. **LLM Reliability**: 在教學任務（對話、閱讀、解釋、修正）的穩定度。
3. **Resource Availability**: 可用語料、字典、TTS/ASR、生態成熟度。
4. **Operational Fit**: 與現有 `TLG-005/006`、`lang_generation_profile` 對接成本。

---

## Priority Tiers

## Tier 1 (Recommended First Wave)

1. `en` (English)
2. `es` (Spanish)
3. `fr` (French)
4. `de` (German)
5. `ja` (Japanese)
6. `ko` (Korean)
7. `zh` (Mandarin Chinese)
8. `pt` (Portuguese)
9. `it` (Italian)

定位：
- 高需求 + 高資源 + 對 LLM 教學任務通常最穩定。
- 最適合先驗證「多語系共架構」的可複用性。

## Tier 2 (Conditional Expansion)

1. `hi` (Hindi)
2. `th` (Thai)
3. `id` (Indonesian)
4. `vi` (Vietnamese)
5. `tr` (Turkish)

定位：
- 潛力與區域需求強，但需更嚴格語系 profile 與 gate 校正。
- 建議在 Tier 1 跑通後再逐語言上線。

## Tier 3 (Long-tail / Research-led)

- 其他低資源或資料不均語言（依實際需求追加）。

定位：
- 優先做 profile 與評測資料建設，再進入量產。

---

## Architecture Fit (Current System)

現有架構可直接支援多語擴張，關鍵在 profile 與 gate：

1. `TLG-005`：依 `target_lang + content_genre + register_target` 生成內容。
2. `TLG-006`：依語系 gate 擋下語言不符/語域不符/文體不符。
3. `lang_generation_profile_v1`：每語言定義 register、genre style、prompt policy、gate policy。

---

## Per-Language Onboarding Checklist

每新增一個語言，至少完成：

1. 新增 `docs/tasks/lang_profiles/{lang}_generation_profile_v1.json`
2. 補齊該語言 pattern library（A1/A2 起步）
3. 補齊 repair strategy registry
4. 跑 `TLG-005` sample generation（含 dialogue + reading）
5. 跑 `TLG-006` gate（含 lang/style blockers）
6. 完成 2 units pilot + issue report

---

## Rollout Policy (Draft)

1. 先上 `Tier 1` 中 2-3 語言，驗證跨語系穩定性。
2. 通過後批次擴張 Tier 1 餘下語言。
3. Tier 2 逐語言試點，不一次開太多。
4. 任何語言若 gate fail rate 過高，降級為 research track。

---

## Notes

1. `th` 在此文件是正式候選語言之一，但不是唯一優先目標。
2. 本文件是策略基線；最終實作語言清單可由 PM/市場策略調整。
