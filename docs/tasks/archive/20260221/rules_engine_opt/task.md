# 任務清單：Rules Engine 深度優化與 Banmal (平語) 支援擴充

## Phase 1: 優先權與邊界測試框架建立

- [ ] 撰寫 `test_rules_engine.py` 測試腳本
  - [ ] 涵蓋 A1 級別核心詞彙（`하다`, `있다`, 敬語變化等）
  - [ ] 涵蓋不規則變化（`ㅂ/ㅆ/ㄹ` 收音等）
  - [ ] 建立防止優先權碰撞的迴歸測試機制（確保新規則不會破壞現有解析）

## Phase 2: 上下文感知的 `요` 攔截器實作

- [ ] 修改 `engine/rules_engine.py` 的 Match 與 Reconstruction 迴圈
  - [ ] 實作動態檢查邏輯：判斷前一個 Atom 的 POS
  - [ ] 若前一 POS 為 `ko:e`，則強制將 `요` Parse 為 `ko:e:요`
  - [ ] 若前一 POS 為體詞 (`n`, `pron`, `prop`, `adv`)，則強制將 `요` Parse 為 `ko:p:요`
- [ ] 透過 `test_rules_engine.py` 驗證 `요` 碰撞問題是否解決

## Phase 3: 平語 (Banmal) 基礎規則擴充

- [ ] 創建 `engine/rules/31_verb_endings_banmal.json`
  - [ ] 加入基礎動形詞平語尾：`-어/아`, `-했어`, `-자`, `-니`, `-냐` 等
  - [ ] 設定 `dictionary_required: true` 防護網
- [ ] 創建 `engine/rules/41_copula_banmal.json`
  - [ ] 加入名詞平語繫詞：`-(이)야`, `-(이)었어/였어`
- [ ] 透過測試腳本驗證平語詞彙（如 `먹어`, `진짜야`, `했어`）是否能正確解構

## Phase 4: A1 Overrides 瘦身 (De-Overridization)

- [ ] 掃描 `content/overrides/A1-*.jsonl`
- [ ] 刪除高頻且引擎已能正確解析的重複項目
  - [ ] 移除 `ko:adj:있다+ko:e:어요` (50x)
  - [ ] 移除 `ko:pron:저+ko:p:는` (23x)
  - [ ] 移除 `ko:v:하다+ko:e:어요` (14x)
  - [ ] 移除 `ko:adj:있다+ko:e:었+ko:e:어요` (11x)
  - [ ] 移除 `ko:v:하다+ko:e:었+ko:e:어요` (8x)
  - [ ] 移除 `ko:adj:좋다+ko:e:네+ko:e:요` (7x)
  - [ ] 移除 `ko:pron:언제+ko:cop:이다+ko:e:에요` (7x)
- [ ] 針對特殊複合詞（如 `씨는요` 8x, `좋아해요` 8x），評估是否應加入 `mapping_phrase.json` 或 `mapping_verbs.json`
  
## Phase 5: 最終驗證與自動化腳本優化

- [ ] 修改 `scripts/dev/generate_overrides_from_gold.py`
  - [ ] 加入「Try-Engine-First」模擬機制（若引擎可解出完全相同的 Atom，便跳過寫入 Jsonl 減少冗餘）
- [ ] 執行 `scripts/ops/run_mapping_pipeline.py` 及 QA 閘門，確保 V5 A1 內容的相容性為 100%
