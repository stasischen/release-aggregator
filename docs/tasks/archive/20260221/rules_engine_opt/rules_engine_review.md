# Rules Engine 語言學與架構合理性審核報告

> [!NOTE]
> 審核對象：`content-ko/engine/rules_engine.py` 及 `engine/rules/*.json`
> 審核標準：V5 原子化標準與韓語形態學
> 語言：繁體中文

## 1. 架構設計審核 (Architecture Evaluation)

目前的 Rules Engine 在設計上**非常優秀且符合韓文特性**：

- **智慧型發音變異處理 (Phonological Variation)：** 引擎內建了對 `ㅆ` (過去式) 和 `ㄹ/ㄴ` 等收音 (Batchim) 的特殊處理 (`ss_contraction`, `batchim_suffix`)。這能有效抓出隱藏的詞幹 (例如從 `했어요` 正確拆出 `하다` + `았` + `어요`，而不是瞎切)，語言學上極為合理。
- **字典約束 (Dictionary Required Guard)：** 在助詞 (如 `은/는/이/가`) 規則中啟用了 `dictionary_required: true`，這是一招好棋。它能防止過度解構 (Over-segmentation)，也就是說只有當前面的詞確實在字典中是個合理的名詞時，才會把助詞切出去，避免把單純名字結尾的字誤切。
- **動態 POS 校正：** `_normalize_predicate_atom_with_dictionary` 能根據字典證據自動把 `v` (動詞) 和 `adj` (形容詞) 校準，解決了韓文中動形同源的詞性飄忽問題。

## 2. 具體規則合理性 (Rule Rationality by V5 Standards)

我深入檢查了幾個最關鍵的 JSON 規則檔案：

### ✅ 動詞/形容詞規則 (`30_verb_endings.json`)

- 完全符合 V5 要求！例如：
  - `하세요` -> `하다`(詞幹) + `시`(敬語) + `어요`(語尾)
  - `겠네요` -> `겠`(推測) + `네요`(感嘆)
  - `웠어요` -> 針對 `ㅂ` 不規則變化 (如 `고마워요`) 正確還原為 `ᆸ다` + `었` + `어요`。這顯示規則在形態學上的還原 (Reconstruction) 是極度精確的。

### ✅ 繫詞規則 (`40_copula.json`)

- `이다` 的剝離完美執行！
  - 像 `예요/이에요` 或過去式的 `였어요/이었어요` 都被強制規範必須獨立出 `ko:cop:이다`。這徹底防止了把 `이다` 當作普通動詞或後綴的慘劇，對後續的語法樹建構非常有幫助。

### ⚠️ 助詞與語尾 (`60_particles.json`)

- 基礎助詞如 `에서`, `를`, `도` 的拆解沒有問題。
- **潛在盲點：** 引擎內對於 `요` 的判斷缺乏「上下文感知 (Context-awareness)」。在我們剛才的 A1 Overrides 報告中發現了 `ko:p:요` 被誤接在 `ko:e` (語尾) 後面的錯誤。因為目前的 Regex pattern 是以結尾做匹配，引擎很難單憑後綴知道前面的詞性是什麼。

## 3. 下一步優化建議 (Actionable Recommendations)

1. **實作上下文感知的 `요` 攔截器：**
   在 `rules_engine.py` 的建構結尾 (Reconstruction loop) 內加入針對 `요` 的動態判斷。如果前面被切出的原子是 `ko:e`，則它必須是 `ko:e:요`；如果前面是體詞 (`n`, `pron` 等)，則必須是 `ko:p:요`。這能根除 99% 的 `요` 詞性碰撞問題。

2. **優先權梳理與邊界測試 (Priority & Edge Cases)：**
   部分動詞規則的優先權很近 (例如 89, 90, 95)。隨著未來 B1/B2 語法引入，可能會發生「被提早匹配導致拆解不完全」的狀況。建議撰寫一個簡單的 `test_rules_engine.py`，輸入數百個極端變化型確認配對順序依然穩固。

3. **收割 Overrides 進入 Engine：**
   現在 Rules Engine 已經這麼強大了，我們之前在 A1 發現的「50次出現的 `있어요`」這類贅肉，可以直接依賴 Engine 處理，把 `.jsonl` 裡的 overrrides 完全刪除，達到系統極簡化。

---
**總結：** Rules Engine 的核心邏輯極其堅固，且對韓文語言學的特殊現象（不規則變化、敬語插入、縮寫）有深刻的理解與對應的架構設計。只要加上針對 `요` 的微調，它就是一個完美的解析器。
