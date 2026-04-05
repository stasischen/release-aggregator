# Learning Library Pipeline Draft v0

## Goal

設計 `content-pipeline` 如何將 `content-ko` 的分散內容轉化為 App 可用的整合 artifact。

---

## 1. Flow Overview

```text
[Input: content-ko]
    ├── core/                (Source Truth & Overlay Structure)
    └── i18n/zh_tw/          (Localized Teaching Content)
           |
           v
[Pipeline: Normalization]
    ├── Merge core & i18n
    ├── Indexing & Graph Linking
    └── Validation (Referential Integrity)
           |
           v
[Output: App Artifacts]
    └── learning_library_*.json
```

---

## 2. Input/Output Mapping

### A. Merged Models (Structure + Translation)

| Target Artifact | Source Core Paths | Source I18n Paths |
| --- | --- | --- |
| `knowledge.json` | `core/learning_library/knowledge/` | `i18n/zh_tw/learning_library/knowledge/` |
| `topics.json` | `core/learning_library/topics/` | `i18n/zh_tw/learning_library/topics/` |
| `vocab_sets.json` | `core/learning_library/vocab_sets/` | `i18n/zh_tw/learning_library/vocab_sets/` |

### B. Generated Indexes

| Target Artifact | Build Logic |
| --- | --- |
| `sources_index.json` | 掃描 `core/video/*.json` 與 `core/dialogue/*.json` 提取 metadata。 |
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

1. **Dangling Refs**: `links` 指向不存在的 `kg_id` 或 `source_id`。
2. **Missing I18n**: 建檔於 `core` 但在 `i18n` 目錄找不到對應的翻譯檔。
3. **Invalid Kind**: `knowledge_item` 使用了不符合 schema 的 `kind`。

---

## 4. Pipeline Steps (Detail)

### Step 1: Scan & Load

- 遍歷 `content-ko` 指定目錄，載入所有 JSON 檔案。
- 使用 `core-schema` 驗證原始檔案格式。

### Step 2: Knowledge Merging

- 以 `core` 為 base，深度合併 `i18n` 內的欄位 (如 `title_zh_tw` -> `title`)。
- 處理 `example_bank` 的合併。

### Step 3: Source Indexing

- 從影片檔提取 `id`, `type`, `mediaId`, `title`, `level`。
- 從影片/對話檔內嵌的 `topic_refs` 收集資訊。

### Step 4: Link Aggregation

- 收集外部 `links/*.json`。
- (Optional) 自動從 `sentence.knowledge_refs` 提取關係並轉化為反查索引。

### Step 5: Emit

- 產出 `v0` 規範的 4+1 個 JSON 檔案。
- 建議輸出位置：`lingo-frontend-web/assets/content/learning_library/zh_tw/` (由 release-aggregator 協調)。

---

## 5. Next Phase Implementation Focus

- 實作 `content-pipeline` 中的 `learning-library` 處理器類別。
- 撰寫 `validateRefs` 工具函式。
- 整合至既存的 build script。
