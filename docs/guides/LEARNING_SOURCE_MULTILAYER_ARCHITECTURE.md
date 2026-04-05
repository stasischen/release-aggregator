# Learning Source Multi-Layer Architecture

## Goal
定義 app 端的多層學習架構，讓不同內容型態都能共享同一套學習模型，而不是把架構綁死在 `video`。

此架構的核心原則：
- `source` 是學習入口，但不限定是影片
- `sentence` 是最小可教學的內容載體
- `topic`、`knowledge`、`vocab` 都是可重用資產
- 使用者學習狀態獨立於內容本體

補充原則：
- 資料層維持 `source-first`
- 體驗層可同時支援 `content-first` 與 `knowledge-first`
- `content-first` 與 `knowledge-first` 共用同一套 graph，不共用同一個主畫面

## Layer Model
1. `source`
- 學習入口
- 可對應：
  - `video`
  - `dialogue`
  - `article`
  - `story`
  - `lesson`
  - `podcast`

2. `sentence`
- 最小句子單位
- 可承載：
  - 原文
  - 翻譯
  - 時間軸
  - source 關聯
  - topic / knowledge / vocab 關聯

3. `topic`
- 學習主題
- 例如：
  - `星期幾`
  - `月份`
  - `相對日期`
  - `顏色`
  - `數字`

4. `knowledge_item`
- 可重用的教學知識點
- 子類型：
  - `grammar_point`
  - `pattern_frame`
  - `connector_item`

5. `vocab_item`
- 可重用單字或固定詞組
- 可先做 sentence-level 掛載
- 之後再和 dictionary / atom layer 深整合

6. `user_learning_state`
- 使用者狀態
- 例如：
  - `hidden_item_ids`
  - `boosted_item_ids`
  - `known_vocab_ids`
  - `shadowing_progress`

## Responsibility Boundaries
### `source`
負責：
- 內容入口
- metadata
- sentence collection
- source type

不負責：
- 存完整文法解說
- 存完整句型庫
- 存完整 topic 定義

### `sentence`
負責：
- 顯示原句
- 顯示翻譯
- 連到知識點
- 連到主題

不負責：
- 自己成為文法本體
- 自己承擔整個主題解說

### `topic`
負責：
- 聚合同一學習主題下的 vocab / knowledge / sentence / source
- 提供主題入口與瀏覽方式

### `knowledge_item`
負責：
- 可重用解說本體
- 教學摘要
- 例句池
- 對比與關聯知識

### `vocab_item`
負責：
- 單字顯示與教學 gloss
- 對應主題與例句
- 之後可與字典層合流

### `user_learning_state`
負責：
- 熟悉隱藏
- 加強高亮
- shadowing 進度
- topic 偏好

## Canonical Relationships
1. `source -> sentence`
- 一個 source 包含多個 sentence

2. `sentence -> knowledge_item`
- 一句可連多個知識點

3. `sentence -> vocab_item`
- 一句可連多個核心詞彙

4. `sentence -> topic`
- 一句可屬於多個學習主題

5. `topic -> source`
- 主題可反查哪些 source 使用它

6. `knowledge_item -> source`
- 知識點可反查在哪些內容中出現

## Why `source` Instead Of `video`
如果入口被定義成 `video`，則：
- 現有 dialogue 難以共用架構
- 未來 article / story / podcast 需要另做平行模型
- topic 與知識庫會被誤綁在影片產品上

如果入口被定義成 `source`，則：
- `video` 只是其中一種 source type
- 現有 dialogue 可直接接入
- 未來 article 也能沿用同一套 topic / knowledge / sentence 結構

## Recommended Core Schemas
### `source`
```json
{
  "id": "src.ko.video.79Pwq7MTUPE",
  "source_type": "video",
  "title": "Learn Korean with Easy Listening",
  "level": "A1-A2",
  "sentence_refs": ["sent.001", "sent.002"],
  "topic_refs": ["topic.time.weekday"]
}
```

### `sentence`
```json
{
  "id": "sent.79Pwq7MTUPE.v_009",
  "source_id": "src.ko.video.79Pwq7MTUPE",
  "surface_ko": "오늘은 토요일이에요.",
  "translation_zh_tw": "今天是星期六。",
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "vocab_refs": ["kv.time.relative_day.today", "kv.time.weekday.saturday"],
  "topic_refs": ["topic.time.weekday"]
}
```

### `topic`
```json
{
  "id": "topic.time.weekday",
  "title_zh_tw": "星期幾",
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "vocab_refs": ["kv.time.weekday.monday", "kv.time.weekday.tuesday"],
  "sentence_refs": ["sent.79Pwq7MTUPE.v_009"],
  "source_refs": ["src.ko.video.79Pwq7MTUPE"]
}
```

### `knowledge_item`
```json
{
  "id": "kp.time.today_is_weekday",
  "kind": "pattern_frame",
  "title_zh_tw": "今天是星期幾",
  "surface": "오늘은 N요일이에요",
  "topic_refs": ["topic.time.weekday"]
}
```

## Topic Family Recommendation
先支援可明確聚合的 family：
- `time`
  - `weekday`
  - `month`
  - `relative_day`
  - `clock_time`
- `number`
- `color`

這些 family 比較適合做 topic-first 入口，因為它們天然具有：
- 可列核心詞表
- 可列核心句型
- 可列相關 source

## UI Implication
### Product Modes
此架構支援兩種不同的產品模式：

1. `Content-First Learning`
- 以內容為主
- 使用者先進入影片 / dialogue / article / story
- 主要操作是選句、看片、跟讀、查看對應解說

2. `Knowledge-First Lab`
- 以知識點為主
- 使用者先進入文法 / 句型 / 字彙 / 主題
- 主要操作是查詢、比對、反查相關內容來源

這兩種模式都應共用：
- `source`
- `sentence`
- `topic`
- `knowledge_item`
- `vocab_item`
- `user_learning_state`

但不應共用同一個主入口與主畫面。

### Source Detail
- Header
- Source media / source body
- Sentence timeline
- Knowledge panel
- Shadowing

Source Detail 應優先採 `content-first`：
- source 是主體
- sentence 是主要互動層
- knowledge / topic / vocab 是 contextual layer
- 不應讓知識庫卡片主導整個畫面

### Topic Detail
- Hero summary
- Core patterns
- Core vocab grid
- Related sentences
- Related sources

### Knowledge Detail
- Canonical explanation
- Example bank
- Related topics
- Related sources

## Phased Rollout
1. `source + sentence + knowledge link`
- 先跑得動 sentence-level app mockup

2. `topic layer`
- 支援從內容 drill-down 到主題
- 保留未來 topic-first browse 能力

3. `vocab layer`
- 先 sentence-linked vocab

4. `dictionary deep integration`
- 等有穩定 tokenized dialogue/article examples 再接 atom layer

## Experience Recommendation
目前 prototype 應優先收斂成 `Content-First Learning`：
- 影片 / 文章 / 對話是主體
- 點句子後顯示文法 / 句型 / 字彙 / 主題解說
- topic detail 與 knowledge detail 是次級 drill-down

`Knowledge-First Lab` 應作為另一個獨立 feature：
- 類似句型書 / 文法書 / 字典 / topic reference
- 適合查詢、複習、反查內容來源
- 不應與 source detail 混成同一個主畫面

## Current Mockups
- Source-based seed mockup: [docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.json](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.json)
- Source-based visual mockup: [docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.html](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_video_learning_mockup_79Pwq7MTUPE.html)
- Topic family mockup: [docs/tasks/mockups/ko_topic_family_time_mockup.json](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_topic_family_time_mockup.json)
- Product mode split: [docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/guides/CONTENT_FIRST_AND_KNOWLEDGE_LAB_SPLIT.md)
