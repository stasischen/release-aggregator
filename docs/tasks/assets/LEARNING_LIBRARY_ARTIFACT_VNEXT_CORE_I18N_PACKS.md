# Learning Library Artifact vNext — Target Core + Support I18n Packs

## Decision

Learning Library 主線 artifact 不再以「單一 support language 合成後的大包」作為長期方向。

改為：

- `target-language core pack`
- `support-language i18n pack`
- frontend intake 在 runtime / repository 層組裝

這個決策的原因是：

1. 目前內容量仍小，且課程正在重構，現在升級 contract 成本最低。
2. 未來目標是多語學多語，不能讓同一份 target-language 內容隨 support language 重複打整包。
3. lazy load、語言切換、跨 support language 複用都要求 `core` 與 `i18n` 分離。

## Packaging Model

以學韓文為例：

- `learning_library_ko_core_sources_index.json`
- `learning_library_ko_core_sentences.json`
- `learning_library_ko_core_knowledge.json`
- `learning_library_ko_core_topics.json`
- `learning_library_ko_core_vocab_sets.json`
- `learning_library_ko_core_links.json`

搭配：

- `learning_library_ko_i18n_zh_tw_sources.json`
- `learning_library_ko_i18n_zh_tw_sentences.json`
- `learning_library_ko_i18n_zh_tw_knowledge.json`
- `learning_library_ko_i18n_zh_tw_topics.json`
- `learning_library_ko_i18n_zh_tw_vocab_sets.json`

以及未來：

- `learning_library_ko_i18n_en_*.json`
- `learning_library_ko_i18n_ja_*.json`

`links` 先視為 canonical graph data，歸於 core。

## Core vs I18n Boundary

### Core Owns

以下欄位屬於 target-language canonical content：

- `id`
- `type`
- `media_id`
- `level`
- `thumbnail_url`
- `duration`
- `topic_refs`
- `knowledge_refs`
- `vocab_refs`
- `sentence_refs`
- `surface_ko` / target-language sentence surface
- `start_ms`
- `end_ms`
- `kind`
- `subcategory`
- `tags`
- `surface`
- `parent_id`
- canonical graph / link structure

### I18n Owns

以下欄位屬於 support-language teaching layer：

- `title`
- `summary`
- `explanation`
- `translation`
- `usage_notes`
- example gloss / translation
- learner-facing taxonomy labels

原則：

- target-language form / structure / graph 不放進 i18n pack
- learner-facing說明 / 翻譯 / 教學文字 不放進 core pack

## Frontend Composition Contract

frontend 不再直接吃單語言 finalized blob。

改為：

```text
target core pack
  + selected support-language i18n pack
  -> learning library composition adapter
  -> UI/domain snapshot
```

frontend repository 的責任：

1. 先載入 target core
2. 再載入指定 support language i18n
3. 組裝成目前畫面需要的 domain model
4. i18n 缺漏時 fail soft，但不可偷偷切回別的 support language

## Lazy-Load Readiness

這個分包模型比目前單包模式更適合 lazy load，因為之後可以進一步演進為：

- 先載 `sources_index core + selected i18n`
- 點進 detail 時再載 `sentences/knowledge/topics`
- 僅切換 support language i18n，不重載 core

本次先凍結「core / i18n 分包 contract」；
是否同步做更細的 source/topic shard，可留待下一階段。

## Migration Policy

這次決策雖然會調整主線 artifact contract，但屬於有意識的早期架構升級，不視為違反原先「不要改主線 artifact contract」原則。

明確理由：

- 現在資料量仍小
- frontend intake 尚未正式全面切換
- unit refactor 尚未大量建立在舊 contract 上
- 若現在不改，之後 `zh_tw/en/...` 與 lazy load 會造成雙重返工

## Effect On Mainline

主線順序不變：

1. staging recovery
2. frontend intake
3. unit-by-unit refactor

但 Layer 1 / Layer 2 的 artifact 基線改成：

- staging recovery 以 `core + zh_tw i18n` 為驗證單位
- frontend intake 以 `core + selected i18n` 為正式承接方式

## Immediate Follow-Up

需要同步更新：

1. `LEARNING_LIBRARY_ARTIFACT_SPEC_V0.md`
2. `LEARNING_LIBRARY_PIPELINE_DRAFT_V0.md`
3. `LEARNING_LIBRARY_CONTENTKO_MIGRATION_PLAN.md`
4. `LEARNING_LIBRARY_CONTENTKO_MIGRATION_TASKS.json`
5. `TASK_INDEX.md`

## Non-Goals

本次不一起做：

- B1+ segmentation 修復
- knowledge lab enrichment
- CONTENT_V5_MIGRATION_L0
- source/topic shard 細分策略

