# Knowledge Lab And content-ko Architecture

## Goal
定義 `Knowledge-First Lab` 的長期內容架構，並說清楚它和現有 `Content-First Learning` prototype 的關係。

此文件回答三個問題：
- `Knowledge-First Lab` 應該怎麼和 `SourceDetailScreen` 分工
- learning library 正式內容應該放在哪個 repo
- app 應該吃什麼 artifact，而不是直接吃 prototype seed

## Product Split
### `Content-First Learning`
主入口是 `source`。

適合：
- `video`
- `dialogue`
- `article`
- `story`

主要互動：
- 先進內容
- 點句子
- 看句子對應的 grammar / pattern / topic / vocab

### `Knowledge-First Lab`
主入口是 `knowledge / topic / vocab`。

適合：
- 文法書
- 句型書
- 主題字卡
- 字典查詢
- 反查有哪些內容用到某知識點

主要互動：
- 先進知識點
- 看解說與例句
- 再反查對應 source / sentence

## Shared Graph
兩種模式共用同一套底層 graph：
- `source`
- `sentence`
- `knowledge_item`
- `topic`
- `vocab_item`
- `user_learning_state`

但不共用同一個主畫面。

## Source Of Truth
### Existing `content-ko` Structure
目前 `content-ko` 已有可作為正式 source of truth 的內容層：
- `content/core/dialogue`
- `content/core/video`
- `content/core/grammar`
- `content/i18n/zh_tw/dialogue`
- `content/i18n/zh_tw/video`
- `content/i18n/zh_tw/grammar`

另外已有字典層預留位置：
- `content/core/dictionary/atoms`

### Decision
長期不應把 source 本體保留在 app 端的大 seed 檔。

正式內容應放回 `content-ko`：
- source 本體沿用既有 `core/*` 與 `i18n/*`
- learning overlay 另外建立在 `content-ko`
- app 只吃 normalize/build 後的 artifact

## Extensible Knowledge Taxonomy
正式化時，不建議把 `knowledge_item.kind` 永遠綁死在 prototype 的三種：
- `grammarPoint`
- `patternFrame`
- `connectorItem`

長期建議改為兩層分類：

### `kind`
大類，供主導覽與主要 UI 分組使用：
- `grammar`
- `pattern`
- `connector`
- `expression`
- `usage`

### `subcategory`
細類，供擴充與搜尋使用。

範例：
- `grammar`
  - `copula`
  - `ending`
  - `particle`
  - `tense_aspect`
  - `honorific`
  - `negation`
- `pattern`
  - `greeting`
  - `self_intro`
  - `question`
  - `preference`
  - `time_expression`
- `connector`
  - `sequence`
  - `cause`
  - `contrast`
  - `addition`

### `tags`
額外加上自由標籤，支援跨類搜尋與聚合。

例如：
- `a1`
- `daily_life`
- `politeness`
- `school`
- `weekday`

### Why This Matters
這樣之後加入新的教學分類時，不需要重做 schema。

例如：
- `語尾` -> `kind = grammar`, `subcategory = ending`
- `敬語` -> `kind = grammar`, `subcategory = honorific`
- `問候語` -> `kind = pattern`, `subcategory = greeting`

## Recommended `content-ko` Overlay Layout
建議新增一個正式的 learning overlay 目錄：

```text
content-ko/content/core/learning_library/
  knowledge/
    grammar/
      copula/
      endings/
      particles/
      honorific/
    patterns/
      greetings/
      self_intro/
      time/
    connectors/
      sequence/
      cause/
      contrast/
    expressions/
    usage/
  topics/
  vocab_sets/
  links/
```

對應中文教學層：

```text
content-ko/content/i18n/zh_tw/learning_library/
  knowledge/
    grammar/
      copula/
      endings/
      particles/
      honorific/
    patterns/
      greetings/
      self_intro/
      time/
    connectors/
      sequence/
      cause/
      contrast/
    expressions/
    usage/
  topics/
  vocab_sets/
```

## Why Not Reuse `core/grammar` Directly
`core/grammar` 現在比較像原始教學素材或課程語法資料。

`learning_library/knowledge` 則是 app 可直接使用的 normalize layer。

兩者角色不同：
- `core/grammar`: source material
- `learning_library/knowledge`: app-facing knowledge contract

因此不建議直接把 app 需要的欄位硬塞回 `core/grammar`。

## Vocab Layer Decision
### Keep Dictionary Truth Separate
因為 `content-ko` 已經有：
- `content/core/dictionary/atoms`

所以不要再建立第二套 `learning_library_vocab.json` 當字典真相。

### Split Into Two Layers
1. `dictionary atoms`
- 真正詞典資料
- lemma / surface / sense / POS / dictionary examples

2. `vocab_sets`
- 某個 source 或某個 topic 要教哪些詞
- 是教學挑選層，不是字典真相

### Practical Rule
短期：
- learning library 先維持 `vocab_item` 給 app 顯示
- 內容正式化時，把它落到 `vocab_sets`

中期：
- 若有對應 dictionary atom，`vocab_set item` 只存 `dictionary_atom_ref`
- 若還沒有 atom，暫時保留 `surface` fallback

## Recommended Artifacts
原本 prototype 的五檔輸出，正式化後建議調整為以下結構：

### Required
1. `learning_library_knowledge.json`
- all knowledge items across:
  - grammar
  - pattern
  - connector
  - future expression / usage
- must retain:
  - `kind`
  - `subcategory`
  - `tags`

2. `learning_library_topics.json`
- topic families
- topics
- topic metadata

3. `learning_library_links.json`
- source -> topic refs
- sentence -> knowledge refs
- sentence -> topic refs
- sentence -> vocab refs
- reverse lookup indexes if needed

4. `learning_library_sources_index.json`
- app 端需要的 source metadata index
- 應視為 build artifact / index
- 不應是 source of truth

### Optional
5. `learning_library_vocab_sets.json`
- topic / source 的教學詞集合
- optional `dictionary_atom_ref`

### Not Recommended
- `learning_library_vocab.json`

這個命名太容易和正式 dictionary layer 混淆。

## Knowledge Lab Screen Model
### `KnowledgeLabHome`
- Grammar
- Patterns
- Topics
- Vocabulary

### `KnowledgeDetail`
- canonical explanation
- forms / rules
- examples
- related sources

### `TopicDetail`
- topic summary
- core patterns
- core vocab set
- related sentences
- related sources

### `VocabDetail`
- surface
- gloss
- related topics
- related sources
- dictionary atom deep link

## Build Pipeline Recommendation
### Inputs
- `content/core/dialogue`
- `content/core/video`
- `content/core/grammar`
- `content/i18n/zh_tw/dialogue`
- `content/i18n/zh_tw/video`
- `content/i18n/zh_tw/grammar`
- `content/core/learning_library/*`
- `content/i18n/zh_tw/learning_library/*`
- future `content/core/dictionary/atoms`

### Outputs
- `learning_library_sources_index.json`
- `learning_library_knowledge.json`
- `learning_library_topics.json`
- `learning_library_links.json`
- optional `learning_library_vocab_sets.json`

## Suggested Knowledge Item Contract
正式 schema 至少應保留：

```json
{
  "id": "kg.beginner.present.copula",
  "kind": "grammar",
  "subcategory": "copula",
  "level": "A1",
  "tags": ["status", "self_intro", "daily_life"],
  "surface": "~이에요/예요",
  "title_zh_tw": "是 ~이에요/예요"
}
```

語尾的例子：

```json
{
  "id": "kg.beginner.ending.aseo_eoseo",
  "kind": "grammar",
  "subcategory": "ending",
  "level": "A1",
  "tags": ["sequence", "reason"],
  "surface": "~아서/어서",
  "title_zh_tw": "先後/原因連接 ~아서/어서"
}
```

## Reserved Taxonomy For Future Expansion
為了避免未來加入新分類時重做 schema，建議現在就先預留以下 taxonomy。

### Knowledge `kind` / `subcategory`
#### `grammar`
- `copula`
- `ending`
- `particle`
- `tense_aspect`
- `honorific`
- `negation`
- `modifier`
- `question_form`
- `speech_level`

#### `pattern`
- `greeting`
- `self_intro`
- `question`
- `preference`
- `time_expression`
- `location`
- `shopping`
- `school`
- `daily_routine`

#### `connector`
- `sequence`
- `cause`
- `contrast`
- `addition`
- `condition`
- `conclusion`

#### `expression`
- `formulaic`
- `reaction`
- `classroom_phrase`
- `social_phrase`

#### `usage`
- `register`
- `politeness`
- `pronunciation_note`
- `spelling_note`
- `common_mistake`
- `culture_note`

### Topic Families
除了目前已驗證的 `time`，建議預留：
- `identity`
- `people`
- `school`
- `daily_life`
- `food`
- `place`
- `shopping`
- `transport`
- `weather`
- `emotion`
- `family`
- `work`
- `health`

### Source Types
目前 prototype 已驗證：
- `video`
- `dialogue`
- `article`

建議 schema 先容納：
- `story`
- `lesson`
- `podcast`
- `conversation`
- `note`
- `social_post`

### Vocab Set Kinds
建議預留：
- `source_core_vocab`
- `topic_core_vocab`
- `review_vocab`
- `confusable_vocab`
- `honorific_vocab`
- `survival_vocab`

### Learning Unit Types
目前主體仍以 `sentence` 為主，但 schema 設計建議預留未來可擴為：
- `sentence`
- `utterance`
- `paragraph`
- `quote`
- `caption`

### User Learning State Dimensions
除了目前 prototype 已用的：
- `hidden`
- `boosted`
- `shadowing_progress`

建議預留：
- `bookmarked`
- `reviewed`
- `needs_practice`
- `mastered`
- `confused`
- `pronunciation_focus`

### Link Relation Types
目前 prototype 多數關係還是單純 refs，但正式化時建議 `links` schema 預留：
- `teaches`
- `uses`
- `mentions`
- `example_of`
- `related_to`
- `contrasts_with`

這樣未來 `Knowledge-First Lab` 才能支援更細緻的反查與篩選，而不必重做資料層。

## Recommended Execution Order
1. 凍結目前 app prototype 已驗證過的 schema
2. 在 `content-ko` 建立 `learning_library` overlay 目錄
3. 先搬已驗證過的最小內容：
- video mock 對應的 links
- A1-01 dialogue links
- A1-01 article mock links
- A1-1 knowledge items
- time topic family
4. 建立 normalize pipeline
5. 讓 app repository 從 artifact 讀資料
6. 再開始設計正式 `Knowledge-First Lab`

## Scope Boundary
這個階段不要做：
- app 端長期維護大 seed 檔
- app 直接讀 `content-ko` 原始分散檔
- 在 app 端手寫大量知識正文
- 把 dictionary atoms 與 learning vocab set 混成一層

## Decision Summary
- `Knowledge-First Lab` 是獨立 feature
- 正式內容回到 `content-ko`
- `content-ko` 既有 source 目錄繼續作為 source truth
- 新增 `learning_library` overlay 放知識、主題、links、vocab sets
- app 只吃 build 後 artifact
