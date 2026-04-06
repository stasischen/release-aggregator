# Learning Library content-ko Migration Plan

## Goal
把目前已在 app 內驗證過的 learning library mockup，逐步轉成正式內容資產：
- mockup 先在 app 內驗證 UX
- 再搬進 `content-ko`
- 再跑 pipeline
- 最後讓 app 改讀 artifact

## Scope
本計畫涵蓋：
- `Content-First Learning` 正式化
- `content-ko` learning overlay 目錄規劃
- pipeline artifact contract

本計畫不涵蓋：
- `Knowledge-First Lab` 全量 UI 實作
- dictionary atom 全量建設
- embedded player / deep sync

## Current State
目前已在 app prototype 內驗證：
- `video` source
- `dialogue` source
- `article` source

並已驗證共用：
- `SourceDetailScreen`
- sentence-driven detail panel
- topic / knowledge / vocab linking

目前問題不是 UI 不成立，而是資料仍停留在 app seed。

## Target State
正式資料流應變成：

```text
release-aggregator docs / mockups
  -> content-ko raw content + learning overlay
  -> pipeline normalization/build
  -> target-language core artifacts + support-language i18n artifacts
  -> lingo-frontend-web repositories
```

補充決策：

- Learning Library artifact 不再以單一 locale finalized blob 作為長期目標
- 改為 `target core + support i18n` 分包
- frontend intake 負責 composition

## Phase Plan
### Phase 1: Freeze Prototype Contracts
交付物：
- `source`
- `sentence`
- `knowledge_item`
- `topic`
- `vocab_set item`
- `links`

要求：
- 凍結 app prototype 已驗證欄位
- 明確區分：
  - source truth
  - learning overlay
  - build artifact
- 為 `knowledge_item` 補上可擴充 taxonomy：
  - `kind`
  - `subcategory`
  - `tags`

### Phase 2: Create `content-ko` Overlay Layout
交付物：
- `content/core/learning_library/...`
- `content/i18n/zh_tw/learning_library/...`

先建立：
- `knowledge`
- `topics`
- `vocab_sets`
- `links`

其中 `knowledge` 目錄規劃要預留未來擴充：
- `grammar/coupla|endings|particles|honorific`
- `patterns/greetings|self_intro|time`
- `connectors/sequence|cause|contrast`
- future `expressions`
- future `usage`

### Phase 3: Migrate First Verified Content Pack
先搬最小可用集合：
- `src.ko.video.79Pwq7MTUPE`
- `src.ko.dialogue.a1_01`
- `src.ko.article.a1_01_intro`
- A1-1 knowledge items
- time topic family

並確認第一批就能涵蓋至少兩種 grammar subcategory：
- `copula`
- `honorific`

作為未來 `ending`、`particle` 擴充的基礎驗證。

原則：
- 不一次搬整個 curriculum
- 只搬已在 app prototype 驗證過的部分

### Phase 4: Build Pipeline
目標：
從 `content-ko` 產出 app 可組裝使用的 artifact packs。

輸出：
- `learning_library_{target}_core_sources_index.json`
- `learning_library_{target}_core_sentences.json`
- `learning_library_{target}_core_knowledge.json`
- `learning_library_{target}_core_topics.json`
- `learning_library_{target}_core_links.json`
- `learning_library_{target}_core_vocab_sets.json`
- `learning_library_{target}_i18n_{support}_sources.json`
- `learning_library_{target}_i18n_{support}_sentences.json`
- `learning_library_{target}_i18n_{support}_knowledge.json`
- `learning_library_{target}_i18n_{support}_topics.json`
- `learning_library_{target}_i18n_{support}_vocab_sets.json`

### Phase 5: Frontend Intake
目標：
讓 `lingo-frontend-web` repository 能切到 `core + selected i18n` composition mode。

建議：
- 先保留 seed mode
- 再加入 core/i18n artifact mode
- 等驗證一致後移除 seed mode

## Repo Responsibility
### `release-aggregator`
負責：
- 架構文件
- mockup 定義
- task plan

### `content-ko`
負責：
- source truth
- learning overlay
- i18n 教學層

### `lingo-frontend-web`
負責：
- content-first app UX
- knowledge-first lab UX
- repository / state / screen integration

## Data Boundary Rules
1. source 本體不要長期留在 app seed
2. `dictionary atoms` 與 `vocab_sets` 分層
3. `learning_library_sources_index.json` 是 index，不是 source truth
4. frontend 正式輸入應為 `target core + support i18n`，而不是單語言 finalized blob

## First Migration Recommendation
先搬這些 item：
- `kg.beginner.present.copula`
- `kg.beginner.honorific.ssi`
- future-ready grammar taxonomy slots:
  - `ending`
  - `particle`
- `kp.daily.greeting.annyeong`
- `kp.daily.greeting.bangawoyo`
- `kp.daily.polite_question`
- `topic.time.weekday`
- `topic.time.relative_day`
- `topic.time.clock_time`

## Risks
- 若先搬資料、後定 schema，會返工
- 若把 `vocab_sets` 當成字典真相，之後會和 `dictionary/atoms` 衝突
- 若 app 直接讀 `content-ko` raw files，前端 parser 會過重

## Recommendation
先做：
1. schema freeze
2. content-ko overlay
3. first pack migration
4. freeze `target core + support i18n` artifact contract
5. pipeline artifact pack build
6. frontend composition intake

之後才做：
- `Knowledge-First Lab` 主入口
- dictionary 深整合
- article/story 更完整內容線
