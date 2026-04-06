# LLCM-005g — Learning Library Core/I18n Pack Emission Spec

## Goal

把 Learning Library pipeline 的正式輸出從「單一 localized bundle」改為：

- `target-language core packs`
- `support-language i18n packs`

本文件只定義 pipeline emission contract，不處理 frontend composition 細節。

## Build Axes

pipeline 需明確區分兩個維度：

- `target`
  - 學習語 / canonical content language
  - 例：`ko`
- `support`
  - 教學語 / learner-facing i18n language
  - 例：`zh_tw`, `en`

## Output Directory Layout

建議輸出目錄：

```text
assets/artifacts/learning_library/{target}/
  core/
    sources_index.json
    sentences.json
    knowledge.json
    topics.json
    vocab_sets.json
    links.json
  i18n/
    {support}/
      sources.json
      sentences.json
      knowledge.json
      topics.json
      vocab_sets.json
```

等價完整檔名可視為：

- `learning_library_{target}_core_sources_index.json`
- `learning_library_{target}_core_sentences.json`
- `learning_library_{target}_core_knowledge.json`
- `learning_library_{target}_core_topics.json`
- `learning_library_{target}_core_vocab_sets.json`
- `learning_library_{target}_core_links.json`
- `learning_library_{target}_i18n_{support}_sources.json`
- `learning_library_{target}_i18n_{support}_sentences.json`
- `learning_library_{target}_i18n_{support}_knowledge.json`
- `learning_library_{target}_i18n_{support}_topics.json`
- `learning_library_{target}_i18n_{support}_vocab_sets.json`

規則：

- repo 內建議採資料夾分層路徑
- 文件與討論中可用完整檔名表達
- `links` 目前只出現在 core

## Required Packs

### Core Packs

必須輸出：

1. `core/sources_index.json`
2. `core/sentences.json`
3. `core/knowledge.json`
4. `core/topics.json`
5. `core/vocab_sets.json`
6. `core/links.json`

### I18n Packs

每個 support language 必須輸出：

1. `i18n/{support}/sources.json`
2. `i18n/{support}/sentences.json`
3. `i18n/{support}/knowledge.json`
4. `i18n/{support}/topics.json`
5. `i18n/{support}/vocab_sets.json`

## Field Ownership Matrix

### 1. Sources Index

`core/sources_index.json`

- `id`
- `type`
- `media_id`
- `level`
- `thumbnail_url`
- `duration`
- `topic_refs`
- `knowledge_refs`
- `sentence_refs`

`i18n/{support}/sources.json`

- `id`
- `title`
- `summary`
- optional learner-facing badges / labels

### 2. Sentences

`core/sentences.json`

- `source_id`
- `sentences[].id`
- `sentences[].surface`
- `sentences[].start_ms`
- `sentences[].end_ms`
- `sentences[].knowledge_refs`
- `sentences[].topic_refs`
- `sentences[].vocab_refs`

`i18n/{support}/sentences.json`

- `source_id`
- `sentences[].id`
- `sentences[].translation`
- optional sentence gloss / teaching notes

### 3. Knowledge

`core/knowledge.json`

- `id`
- `kind`
- `subcategory`
- `level`
- `tags`
- `surface`
- canonical example source refs

`i18n/{support}/knowledge.json`

- `id`
- `title`
- `summary`
- `explanation`
- `usage_notes`
- localized example gloss

### 4. Topics

`core/topics.json`

- `id`
- `category`
- `level`
- `parent_id`
- `knowledge_refs`
- `vocab_refs`
- `sentence_refs`
- `source_refs`

`i18n/{support}/topics.json`

- `id`
- `title`
- `summary`

### 5. Vocab Sets

`core/vocab_sets.json`

- `id`
- `surface`
- `topic_refs`
- `source_refs`
- `sentence_refs`
- `dictionary_atom_ref`

`i18n/{support}/vocab_sets.json`

- `id`
- `title`
- optional gloss / pronunciation note

### 6. Links

`core/links.json`

- `id`
- `origin_id`
- `target_id`
- `relation_type`

`links` 不建立 i18n pack。

## Naming Rules

### IDs

- 所有 core 與 i18n pack 必須共用同一組 canonical ids
- i18n pack 不得產生新的 content ids

### Support-Language Pack Naming

- support language 代碼直接使用 locale id
- 例：`zh_tw`, `en`, `ja`

### Forward Compatibility

若未來要 source/topic shard，命名應建立在此基底上：

- `core/sources/{source_id}.json`
- `i18n/{support}/sources/{source_id}.json`

但 `LLCM-005g` 先不要求實作 shard。

## Build CLI Contract

建議命令：

```bash
npm run build:learning-library -- --target=ko --support=zh_tw --out=./dist
```

必要參數：

- `--target`
- `--support`
- `--out`

可選參數：

- `--validate-only`
- `--include-types=video,dialogue,article`

## Validation Rules

### Hard Fail

1. core pack 缺必要檔案
2. i18n pack 缺必要檔案
3. i18n pack 中有 id 不存在於對應 core pack
4. core refs 指向不存在的 core entity
5. 同一 entity 在 core / i18n 間欄位越界

### Allowed In Staging

以下可以存在，但要明確報告：

- `staging_only`
- `readiness_flag != ready`
- `segmentation_status != clean`
- article 尚未全覆蓋

## Staging Recovery Scope

主線第一階段先要求：

- `dialogue`
- `video`

所以 `LLCM-005g` 的第一版 emission 驗收只需保證：

- `ko core + zh_tw i18n`
- `dialogue/video` pack 可穩定輸出
- article 可保留 partial / deferred 狀態

## Acceptance Criteria

`LLCM-005g` 完成時，至少要滿足：

1. pipeline 輸出命名與路徑規則固定
2. core / i18n field ownership 有明確邊界
3. frontend 可依此 contract 實作 composition intake
4. 不再以 localized finalized blob 作為新增主輸出
5. staging recovery 可直接使用 `core + zh_tw i18n` 進行驗證

## Follow-Up

下一手直接依賴這份 emission spec：

- `LLCM-005h`
- `LLCM-006a`
- `LLCM-006b`

