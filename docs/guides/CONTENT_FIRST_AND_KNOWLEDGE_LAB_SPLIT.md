# Content-First And Knowledge-Lab Split

## Goal
明確定義 Lingo app 內兩種不同的學習模式：
- `Content-First Learning`
- `Knowledge-First Lab`

這兩者必須共用同一套資料圖譜，但不應混成同一個主體驗。

## Why Split
如果把兩種模式混在同一頁，常見問題會是：
- 畫面主體不清楚
- 使用者不知道現在是在學內容，還是在查知識
- 影片 / 對話 / 文章的沉浸式學習體驗被 reference UI 打斷
- 文法 / 句型 / 字彙的查詢體驗又不夠乾淨

因此要明確拆開：
- `內容學習模式`
- `知識查詢模式`

## Shared Data Graph
兩種模式應共用同一套底層：
- `source`
- `sentence`
- `topic`
- `knowledge_item`
- `vocab_item`
- `user_learning_state`

核心關係不變：
- `source -> sentence`
- `sentence -> knowledge_item`
- `sentence -> vocab_item`
- `sentence -> topic`
- `topic -> sentence`
- `topic -> source`
- `knowledge_item -> source`

## Mode A: Content-First Learning
### Definition
以內容為主體的學習模式。

### Suitable Content
- `video`
- `dialogue`
- `article`
- `story`
- `lesson`

### Primary User Intent
- 我要學這支影片
- 我要看這篇文章，同時理解句子
- 我要跟讀 / shadowing
- 我要知道這一句用了什麼文法或句型

### Main Screen Shape
1. Source header / media
2. Transcript or sentence timeline
3. Selected sentence detail panel
4. Supporting highlights

### Interaction Priority
1. 先進內容
2. 選句子
3. 看對應解說
4. 視需要再 drill down 到 topic / knowledge detail

### What Belongs Here
- source body
- media preview or player
- sentence list
- sentence-linked grammar/pattern/vocab/topic panel
- shadowing
- familiar / boost

### What Does Not Belong As Main Focus
- 全站知識點瀏覽
- 純文法書式導覽
- 大型 reference index

### Product Positioning
這應是目前 prototype 的主線。

## Mode B: Knowledge-First Lab
### Definition
以知識點本身為主體的查詢 / 複習模式。

### Primary User Intent
- 我要查某個句型怎麼用
- 我要看 A1 到 A2 的核心文法
- 我要查某個主題有哪些常用表達
- 我要從知識點反查有哪些內容來源用到它

### Main Screen Shape
1. Topic / grammar / pattern / vocab browser
2. Canonical explanation
3. Example bank
4. Related sources

### Interaction Priority
1. 先進知識點
2. 看解說與例句
3. 再反查內容來源

### What Belongs Here
- grammar catalog
- pattern catalog
- vocab reference
- topic browser
- reverse lookup to sources

### Product Positioning
這應是另一個獨立 feature。
它不是 `SourceDetailScreen` 的主體。

## Screen Responsibility Split
### `SourceDetailScreen`
責任：
- content-first 主畫面
- source media / body
- sentence-driven learning
- right-side explanation panel

### `TopicDetailScreen`
責任：
- 從內容 drill-down 的次級頁
- 也可被未來 knowledge lab 重用

### Future `KnowledgeLabScreen`
責任：
- knowledge-first 主入口
- grammar / pattern / vocab / topic browse

## Navigation Recommendation
### Current Priority
先強化：
- `Home -> SourceDetail`
- `SourceDetail -> TopicDetail`
- `SourceDetail -> Full Video Player`

### Future Separate Entry
之後再補：
- `Home -> Knowledge Lab`

## Integration With Existing Video Player
目前建議：
1. 先做 `content-first`
2. 先支援從 `SourceDetail` 跳去完整 `VideoPlayer`
3. 不要一開始就把完整播放器 deeply embed 進 learning library

原因：
- 現有 video player 已有自己的 subtitle / dictionary / fullscreen 邏輯
- 現階段直接嵌入會提高耦合
- 先做導流與分工較穩

## Implementation Guidance
### Short Term
- SourceDetail 改成內容主體
- responsive layout
- source media preview
- `觀看完整內容` 按鈕

### Mid Term
- sentence 到 player 的單向跳轉
- source / sentence / topic 高亮整合

### Long Term
- player 與 sentence timeline 雙向同步
- embedded player variant
- shared playback bridge

## Decision
目前 app 端應採：
- `Content-First Learning` 作為主學習模式
- `Knowledge-First Lab` 作為獨立 reference feature

不要把兩者混成同一個入口或同一個主畫面。
