# Learning Library Pipeline Draft v0

## Goal

設計 `content-pipeline` 如何將 `content-ko` 的分散內容轉會為 App 可用的整合 artifact。

---

## 1. Flow Overview

```text
[Input: content-ko]
    ├── core/                (Source Truth: Video/Dialogue/Article/Topic/Knowledge)
    └── i18n/zh_tw/          (Localized Teaching Content)
           |
           v
[Pipeline: Normalization]
    ├── Merge core & i18n
    ├── Indexing & Graph Linking
    ├── Sentence Extraction & Normalization
    └── Validation (Referential Integrity Check)
           |
           v
[Output: App Artifacts]
    └── learning_library_*.json (Index, Knowledge, Topics, Links, Vocab, Sentences)
```

---

## 2. Input/Output Mapping

### A. Merged Models (Structure + Translation)

| Target Artifact | Source Core Paths | Source I18n Paths |
| --- | --- | --- |
| `knowledge.json` | `core/learning_library/knowledge/` | `i18n/zh_tw/learning_library/knowledge/` |
| `topics.json` | `core/learning_library/topics/` | `i18n/zh_tw/learning_library/topics/` |
| `vocab_sets.json` | `core/learning_library/vocab_sets/` | `i18n/zh_tw/learning_library/vocab_sets/` |

### B. Payload Normalization

| Target Artifact | Build Logic |
| --- | --- |
| `sources_index.json` | 掃描 `core/video`, `core/dialogue`, `core/article` 提取 metadata。 |
| `sentences.json` | 從各類源檔案提取原文、翻譯、ref、時間軸，統整為 source_id 為鍵的索引庫。 |
| `links.json` | 聚合 `core/learning_library/links/*.json` 片段。 |

---

## 3. Build Contract (Command Proposal)

### Command

`npm run build:learning-library -- --lang=zh_tw --out=./dist`

### Parameters

- `--lang`: 目標語系 (預設 `zh_tw`)。
- `--out`: artifact 輸出目錄。
- `--validate-only`: 僅執行驗證不輸出檔案。

### Failure Conditions (Stop Build)

1. **Dangling Refs**: `links` 或 `sentences` 指向不存在的 `kg_id` 或 `source_id`。
2. **Missing I18n**: 建檔於 `core` 但在 `i18n` 目錄找不到對應的翻譯檔。
3. **Invalid Kind**: `knowledge_item` 使用了不符合 schema 的 `kind`。

---

## 4. Pipeline Steps (Detail)

### Step 1: Scan & Load

- 遍歷 `content-ko` 指定目錄，載入所有 JSON 檔案。
- 納入 `core/video`, `core/dialogue`, `core/article` 的正規掃描路徑。

### Step 2: Knowledge Merging

- 以 `core` 為 base，深度合併 `i18n` 內的欄位 (如 `title_zh_tw` -> `title`, `summary_zh_tw` -> `summary`)。

### Step 3: Source Indexing & Filtering

- 從影片、對話、文章檔提取 `id`, `type`, `mediaId`, `title`, `level`。
- 確保 `article` 類型能正確被索引。

### Step 4: Sentence Aggregation

- 遍歷所有 source 檔案，並將其 `sentences` 正規化為 App 內部 `Sentencev2` 模型。
- 這一步必須確保 `translation` 與 `refs` 已在 pipeline 內合併。

### Step 5: Link Aggregation

- 收集外部 `links/*.json`。
- 自動從 `sentence.knowledge_refs` 提取關係並轉化為反查索引。

### Step 6: Emit

- 產出 `v0` 規範的 6 個 JSON 檔案。
- 建議輸出位置：`lingo-frontend-web/assets/content/learning_library/zh_tw/`。

---

## 5. Next Phase Implementation Focus

- 實作 `content-pipeline` 中的 `learning-library` 處理器類別。
- 撰寫 `extractSentences` 與 `validateRefs` 工具函式。
- 整合至既存的 build script。
