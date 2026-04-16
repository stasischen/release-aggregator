# Architecture Idea Review (2026-04-07)

## Goal

整理一批新的產品/架構發想，評估：

- 想法是否可行
- 應該落在哪一層
- 先做什麼才不會把系統複雜度一次拉太高

本文件是方向評估，不等於已立項 implementation plan。

---

## Executive Summary

整體判斷：

1. `統一例句庫 + atom/knowledge 反查例句` 是可行而且值得做的方向。
2. `可替換詞句框` 也可行，而且 repo 其實已經有 `slot_substitution` 基礎，不需要從零開始。
3. `沉浸式學習說明 + 基礎發音/音變知識庫 + 按學習者語言推薦入門影片` 可行，但屬於 onboarding / knowledge enrichment，不是核心 runtime blocker。
4. `自建內容 -> TTS -> typing/shadowing` 可行，但要分階段。先做「可匯入內容 + TTS + 練習」，不要一開始就要求完整自建 segmentation/dictionary。
5. 真正高風險的不是 UI，而是 `canonical data model`。如果例句、知識點、slot、source 全部都能互相引用，必須先定義穩定 graph，否則後面會一直補洞。

建議優先順序：

1. 統一例句庫
2. slot substitution 的 canonical schema
3. content-first 的 typing/shadowing 掛載
4. 知識庫中的發音/音變與入門影片
5. 自建內容系統

---

## 1. 統一例句庫

### Idea

不要把例句綁死在單一知識項底下，例如：

- grammar A 有自己的 5 句
- grammar B 有自己的 5 句
- vocab C 有自己的 5 句

而是建立一個統一 `example sentence bank`，讓：

- 單字
- 文法
- 句型
- atom

都去共用同一批例句。

系統可根據 segmentation / atom link 去反查：

- 哪些例句含某個 vocab atom
- 哪些例句包含某個 grammar atom 或 grammar ref
- 哪些例句符合某個 pattern frame

### Feasibility

判斷：`可行，且長期應該這樣做`

原因：

- 符合目前 `Content-First` / `Knowledge-Lab` 共用 graph 的方向。
- 例句會變成可重用資產，而不是知識點內嵌文字。
- 後續更容易做「從 sentence 反查 knowledge」與「從 knowledge 反查 sentence」。

### Recommended Boundary

建議新增一層 canonical artifact：

- `example_sentence`
- `example_sentence_i18n`
- `example_sentence_links`

其中：

- `example_sentence` 存 canonical source text、segmentation、difficulty、register、audio refs
- `example_sentence_i18n` 存翻譯與教學說明
- `example_sentence_links` 存到 `dictionary_atom` / `knowledge_item` / `pattern` / `topic` 的 refs

### Why This Is Better Than Embedded Examples

如果例句直接塞在 grammar / vocab / pattern item 裡，會有幾個問題：

- 同一句會重複存在多處
- 後續勘誤難同步
- 一句話同時展示 vocab + grammar + pattern 時，資料所有權不清楚
- 很難統一做 TTS、排序、難度分級、品質分數

### Use of Early Sentence Bank

你提到「早期版本的例句庫拿來用」。

判斷：`可以當 bootstrap source，但不能直接當正式 truth`

建議做法：

1. 把早期例句庫當 migration input。
2. 跑 normalize，補 canonical ids、segmentation、language metadata、quality flags。
3. 不合格的句子只保留作 staging / candidate，不直接進 production bank。

### Main Risks

- 舊例句的 segmentation 品質不一致
- 翻譯風格不一致
- 同一句可能同時對應多個 grammar/pattern，若沒有主次標記會造成檢索噪音

### Recommendation

先做最小版：

- 先只支援 `sentence -> atom refs`
- 第二步再補 `sentence -> grammar/pattern/topic refs`
- 第三步才做排序策略，例如 `best examples`, `beginner-safe`, `high-frequency`

### Existing Mixed Knowledge Content

目前 knowledge 內容裡已經有一些「文法說明 + 例句」混合在同一 item 內。

如果現有量還不大，較好的做法是直接轉，不保留長期雙軌。

建議策略：

1. 直接盤點現有 knowledge item 內的例句。
2. 可獨立成立的句子全部抽進 `example sentence bank`。
3. 原 knowledge item 改成存 `example_sentence_refs`，不再把例句文本當正式主存放位置。
4. 只有非句子型教學說明、對照備註、usage commentary 留在 knowledge item。

判準：

- 可獨立理解、可重用、可被多 item 引用的句子 -> 抽進 bank
- 強依附當前文法解說語境的對照說明 -> 留在 item

如果內容量仍小，這件事應該一次完成，不要刻意保留過渡狀態。

### Concrete Example From Current Content

可直接用現有 `time` family mockup 示範。

來源參考：

- [ko_topic_family_time_mockup.json](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_topic_family_time_mockup.json)
- [LEARNING_LIBRARY_CONTENTKO_MIGRATION_NOTE.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_CONTENTKO_MIGRATION_NOTE.md)

目前資料裡像這樣：

```json
{
  "id": "kp.time.today_is_weekday",
  "kind": "pattern_frame",
  "surface": "오늘은 N요일이에요",
  "summary_zh_tw": "最直接的星期表達句型，適合做主題頁第一個高亮框架。",
  "topic_refs": ["topic.time.weekday"],
  "example_bank": [
    {
      "ko": "오늘은 토요일이에요.",
      "zh_tw": "今天是星期六。",
      "sentence_ref": "video:79Pwq7MTUPE:v_009"
    }
  ]
}
```

這個 case 的拆法應該是：

保留在 knowledge item 的內容：

- `surface`: `오늘은 N요일이에요`
- `summary_zh_tw`: 這是教學說明，不是句子資產
- `topic_refs`

抽進 example sentence bank 的內容：

- `오늘은 토요일이에요.`
- `今天是星期六。`
- `sentence_ref = video:79Pwq7MTUPE:v_009`

抽完後的 knowledge item 比較像：

```json
{
  "id": "kp.time.today_is_weekday",
  "kind": "pattern_frame",
  "surface": "오늘은 N요일이에요",
  "summary_zh_tw": "最直接的星期表達句型，適合做主題頁第一個高亮框架。",
  "topic_refs": ["topic.time.weekday"],
  "example_sentence_refs": ["ex.ko.time.today_is_saturday.v1"]
}
```

對應的 example sentence 可變成：

```json
{
  "id": "ex.ko.time.today_is_saturday.v1",
  "text_ko": "오늘은 토요일이에요.",
  "text_zh_tw": "今天是星期六。",
  "source_sentence_ref": "video:79Pwq7MTUPE:v_009",
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "topic_refs": ["topic.time.weekday"]
}
```

再看另一個例子：

```json
{
  "id": "kg.time.topic_particle_eunneun",
  "kind": "grammar_point",
  "surface": "은/는",
  "summary_zh_tw": "在星期、月份、今天/昨天這種時間主題中很常作為句首主題標記。",
  "topic_refs": [
    "topic.time.weekday",
    "topic.time.relative_day",
    "topic.time.month"
  ]
}
```

這種內容目前沒有內嵌例句，只有規則性說明。

所以：

- `summary_zh_tw` 應保留在 knowledge item
- 不需要為了抽例句而硬把這段說明改寫成句子
- 之後只要讓它連到共用例句，例如 `오늘은 토요일이에요.`, `이번 달은 5월이에요.` 即可

結論：

- `example_bank` 裡的句子：抽出去
- `summary_zh_tw` / `usage commentary`：留在 knowledge item
- 沒有句子的 grammar item：不需要硬製造假例句，只要後續補 link 到 sentence bank

---

## 2. 可替換詞句框架構

### Idea

針對高頻可遷移結構，建立可替換詞的句框，例如：

- `먹었어요 {item}`
- `샀어요 {item}`
- `오늘은 {date}`

並搭配常用詞庫與受控翻譯，確保：

- 替換後的目標語自然
- 翻譯也通順
- 不會出現語義不合理的組合

### Feasibility

判斷：`可行，而且現有系統已有基礎`

依據：

- repo 已有 `slot_substitution` / `pattern_transform`
- pattern index 也已有 `transform_types`
- mock data 中已經存在 `slot_surface`、`slot_values`、`builder` 類結構

這表示方向不是新發明，而是把目前分散的 pattern/preview 結構正式化。

### Recommended Boundary

不要把這層做成「自由文字替換」。

建議資料模型是：

- `pattern_frame`
- `slot_definition`
- `slot_bank`
- `slot_compatibility_rule`

最小需求：

- 每個 slot 有 semantic type，例如 `food`, `drink`, `date`, `place`, `person`
- 每個 frame 宣告接受哪些 slot type
- translation 不直接字串拼接，而是使用 phrase template 或 target-side rendering rule

### Example

```json
{
  "frame_id": "ko.buy.past.item",
  "base_surface": "{item_acc} 샀어요.",
  "slot_defs": [
    {
      "slot_id": "item",
      "allowed_types": ["food", "daily_good", "ticket"]
    }
  ],
  "render_hints": {
    "zh_tw": "買了{item_zh_tw}",
    "en": "bought {item_en}"
  }
}
```

### Main Risks

- 替換詞若只看 POS，不看 semantic class，會產生不自然句子
- 翻譯若直接機械拼接，中文會不順
- 文法上看似可換，語用上未必常見

### Recommendation

這層很適合 A1/A2 先做受控版本：

- 只做 noun slot
- 只做高頻 frame
- 只允許 curated slot bank

不要一開始就做開放式 generative recombination。

---

## 3. 沉浸式學習原理說明

### Idea

產品上明講：

- 初學不需要先學完整文法系統
- 可以先從基礎 `X` 百字與 `X` 十句型開始
- 真正困難的是找到循序漸進教材
- app 會替使用者整理好難度與順序

### Feasibility

判斷：`高度可行`

這主要是：

- onboarding 文案
- 課程定位
- curriculum explanation

技術阻力很低，重點在教學敘事是否一致。

### Recommended Boundary

這不應該做成底層 schema task。

比較適合落在：

- onboarding
- course intro
- product marketing copy
- help / FAQ / methodology page

### Recommendation

可先做一頁簡潔版說明，不必等整個 curriculum engine 完成。

---

## 4. 基礎發音/音變知識庫

### Idea

在知識庫提供：

- 基礎發音
- 音變規則
- 入門級解說

並根據學習者語言，掛對應語系的入門教學影片，例如：

- 用中文學韓文
- 用英文學韓文
- 用日文學韓文

### Feasibility

判斷：`可行，但應視為 knowledge-first enrichment`

repo 已有：

- `pronunciation` / `prosody` 的規劃
- YouTube grammar/connectors ingestion 基礎
- knowledge-first 架構分流

所以這條線和現有方向一致。

### Recommended Boundary

拆成兩層：

1. `canonical pronunciation knowledge items`
2. `external reference videos`

不要把外部 YouTube 影片本身當 source of truth。

應該是：

- app 內有 canonical knowledge item
- knowledge item 可附 `recommended_external_refs`

### Main Risks

- 外部影片品質不一
- 多語系教學風格差異很大
- 外部連結可失效

### Recommendation

先做 curated metadata，不做 deep integration：

- `support_locale`
- `provider`
- `url`
- `topic`
- `level`
- `quality_note`

這樣之後可替換來源，不綁死在單一 YouTube 素材。

---

## 5. 自建課程內容

### Idea

讓使用者或系統：

- 用 prompt 產出 app 可吃的文章格式
- 存起來
- 用 TTS 練習
- 自建 segmentation / dictionary
- 支援匯入匯出

### Feasibility

判斷：`部分可行，但需要明確切 phase`

#### Phase A

`可行`

- 產出受控文章格式
- 存成 app 可讀內容
- 用 TTS 播放
- 支援匯入匯出

這其實接近「custom source authoring」。

#### Phase B

`條件式可行`

- 句子級練習
- typing / shadowing
- basic lookup

前提是 custom content 至少要有：

- sentence split
- stable ids
- minimal locale fields

#### Phase C

`高複雜度`

- 自建 segmentation
- 自建 dictionary
- 自建 grammar links

這等於把一部分 `content-ko + dictionary + knowledge overlay` 的能力下放到 end-user authoring。

如果太早做，資料品質和維護成本都會失控。

### Recommended Scope Split

不要把「自建內容」視為單一功能。

應拆成：

1. `custom source import/export`
2. `custom TTS practice`
3. `custom sentence practice`
4. `custom lexical annotations`
5. `custom segmentation/dictionary authoring`

前 3 項可先做。
後 2 項應視為 power-user / creator mode。

### Recommendation

MVP 建議只做：

- 匯入 structured text/article
- 自動 sentence split
- TTS
- typing/shadowing
- optional manual keyword list

先不要做完整 user-owned dictionary truth。

---

## 6. 打字 / Shadowing 練習

### Idea

使用者可以選：

- app 內既有 source
- 自建內容
- 自建重點整理

點句子後做：

- 打字
- 跟讀 / shadowing
- 練發音

### Feasibility

判斷：`可行，而且應該掛在 content-first`

這和既有方向一致：

- `SourceDetail` / player 先是主體
- sentence selection 是核心互動
- shadowing 是句子層的次級行為

### Recommended Boundary

把這層掛在 `sentence selection` 之下，而不是獨立設計另一套內容系統。

建議句子操作：

- `listen`
- `repeat`
- `shadow`
- `type`
- `view linked knowledge`

### Main Risks

- 如果和知識查詢模式混在一起，主畫面會過載
- 如果每種內容格式都自己實作 typing/shadowing，前端會分裂

### Recommendation

先定義一個共通 `sentence practice action contract`，讓：

- dialogue
- video transcript
- article sentences
- custom article

都能共用同一套 sentence action。

---

## 7. Cross-Cutting Data Model Recommendation

如果上述方向要成立，底層建議穩定以下幾種 entity：

- `source`
- `sentence`
- `example_sentence`
- `dictionary_atom`
- `knowledge_item`
- `pattern_frame`
- `slot_bank`
- `topic`
- `external_reference`

核心 link：

- `source -> sentence`
- `sentence -> dictionary_atom`
- `sentence -> knowledge_item`
- `example_sentence -> dictionary_atom`
- `example_sentence -> knowledge_item`
- `pattern_frame -> slot_bank`
- `knowledge_item -> example_sentence`
- `topic -> knowledge_item`
- `knowledge_item -> external_reference`

重點原則：

1. `例句` 不應只是 knowledge item 內嵌欄位。
2. `slot bank` 不應只是 UI helper，而應是可重用資料資產。
3. `external references` 只能是補充層，不能取代 canonical knowledge。
4. `custom content` 應先是 source 層，不要一開始就升格成 knowledge truth。

---

## 8. Suggested Execution Order

### Wave 1

- 建立 `example sentence bank` 最小 schema
- 建立 `example sentence -> atom` links
- 把舊例句庫當 migration input

### Wave 2

- 正式化 `pattern_frame + slot_bank`
- 先支援 noun-slot substitution
- 建立 translation render hints

### Wave 3

- 把 typing / shadowing 掛到 content-first sentence actions
- 讓 source / video / article / custom text 共用

### Wave 4

- 建立 pronunciation / sound change knowledge items
- 補 `external_reference` curated metadata

### Wave 5

- 做 custom content import/export
- 再看是否要往 power-user segmentation / custom dictionary 擴張

---

## 9. Final Recommendation

最值得立項的不是「一次做很多新功能」，而是先把兩個中介層做對：

1. `example sentence bank`
2. `pattern_frame + slot_bank`

這兩層一旦穩定，後面的知識庫例句、替換詞練習、typing、shadowing、自建內容都比較容易接上。

相反地，如果現在直接做：

- 自建 segmentation
- 自建 dictionary
- 多語系外部影片推薦
- 各種練習模式同時上

會先把系統複雜度炸開，但 canonical graph 還沒定型。

所以結論是：

- 方向整體可行
- 但要先做 `shared reusable assets`
- 再做 user-facing feature surfaces

---

## Related Existing Docs

- [CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md)
- [TARGET_LANG_AUDIO_SKILLS_PLAN.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TARGET_LANG_AUDIO_SKILLS_PLAN.md)
- [KNOWLEDGE_INGESTION_PLAN_V0.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/KNOWLEDGE_INGESTION_PLAN_V0.md)
- [PEDOPT_002_TRANSFORM_PRACTICE_SPEC.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/PEDOPT_002_TRANSFORM_PRACTICE_SPEC.md)
