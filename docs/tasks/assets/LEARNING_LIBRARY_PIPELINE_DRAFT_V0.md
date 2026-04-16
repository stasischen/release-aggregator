# Learning Library Pipeline Draft v0

## Goal

設計 `content-pipeline` 如何將 `content-ko` 的分散內容轉為 App 可用的 `core + i18n packs`。

---

## 1. Flow Overview

```text
[Input: content-ko]
    ├── core/                (Source Truth: Video/Dialogue/Article/Topic/Knowledge)
    └── i18n/zh_tw/          (Localized Teaching Content)
           |
           v
[Pipeline: Normalization]
    ├── Emit target-language core pack
    ├── Emit support-language i18n pack
    ├── Indexing & Graph Linking
    ├── Sentence Extraction & Normalization
    └── Validation (Referential Integrity Check)
           |
           v
[Output: App Artifacts]
    ├── learning_library_{target}_core_*.json
    └── learning_library_{target}_i18n_{support}_*.json
```

---

## 2. Input/Output Mapping

### A. Split Models (Structure vs Teaching Layer)

| Target Artifact Pack | Source Core Paths | Source I18n Paths |
| --- | --- | --- |
| `*_core_knowledge.json` | `core/learning_library/knowledge/` | — |
| `*_i18n_{support}_knowledge.json` | — | `i18n/{support}/learning_library/knowledge/` |
| `*_core_topics.json` | `core/learning_library/topics/` | — |
| `*_i18n_{support}_topics.json` | — | `i18n/{support}/learning_library/topics/` |
| `*_core_vocab_sets.json` | `core/learning_library/vocab_sets/` | — |
| `*_i18n_{support}_vocab_sets.json` | — | `i18n/{support}/learning_library/vocab_sets/` |

### B. Payload Normalization

| Target Artifact | Build Logic |
| --- | --- |
| `*_core_sources_index.json` | 掃描 `core/video`, `core/dialogue`, `core/article` 提取 canonical metadata。 |
| `*_i18n_{support}_sources.json` | 從 source i18n/overlay 輸出 support-language title/summary 等 learner-facing 欄位。 |
| `*_core_sentences.json` | 從各類源檔案提取 target-language surface、ref、時間軸。 |
| `*_i18n_{support}_sentences.json` | 輸出 sentence translation / learner-facing gloss。 |
| `*_core_links.json` | 聚合 `core/learning_library/links/*.json` 片段。 |

---

## 3. Build Contract (Command Proposal)

### Command

`npm run build:learning-library -- --target=ko --support=zh_tw --out=./dist`

### Parameters

- `--target`: 學習語 / canonical content language。
- `--support`: 教學語 / learner-facing i18n language。
- `--out`: artifact 輸出目錄。
- `--validate-only`: 僅執行驗證不輸出檔案。

### Failure Conditions (Stop Build)

1. **Dangling Refs**: `links` 或 `sentences` 指向不存在的 knowledge_id, topic_id 或引用的 source_id。
2. **Missing I18n**: 需要支援的 i18n 項目在 `i18n/{support}` 目錄找不到對應檔案。
3. **Invalid Kind**: `knowledge_item` 使用了不符合 schema 的 `kind`。

---

## 4. Pipeline Steps (Detail)

### Step 1: Scan & Load

- 遍歷 `content-ko` 指定目錄，載入所有 JSON 檔案。
- 納入 `core/video`, `core/dialogue`, `core/article` 的正規掃描路徑。

### Step 2: Pack Emission Boundary

- `core` 只保留 canonical structure / graph / target-language surface。
- `i18n` 只輸出 learner-facing translation / explanation / labels。
- 不在 pipeline 階段合成單一 finalized blob 作為正式主輸出。

### Step 3: Source Indexing & Filtering

- 從影片、對話、文章檔提取 `id`, `type`, `mediaId`, `title`, `level`。
- 確保 `article` 類型能正確被索引。

### Step 4: Sentence Aggregation

- 遍歷所有 source 檔案，將 sentence 資料拆為：
  - core: target-language surface + refs + timing
  - i18n: translation / learner-facing gloss

### Step 5: Link Aggregation

- 收集外部 `links/*.json`。
- 自動從 `sentence.knowledge_refs` 提取關係並轉化為反查索引。

### Step 6: Emit

- 產出 `core + i18n` pack。
- 建議輸出位置：
  - `lingo-frontend-web/assets/artifacts/learning_library/{target}/core/`
  - `lingo-frontend-web/assets/artifacts/learning_library/{target}/i18n/{support}/`

---

## 5. Next Phase Implementation Focus

- 實作 `content-pipeline` 中的 `learning-library` pack builder。
- 撰寫 `extractSentences` 與 `validateRefs` 工具函式。
- 撰寫 frontend composition adapter，而非 finalized single-bundle intake。
