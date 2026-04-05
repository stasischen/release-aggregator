# Learning Library Artifact Spec v0

## Goal

定義 `content-pipeline` 輸出的正式 artifact 格式。這些文件是 `lingo-frontend-web` 消費的唯一標準，解決了從原始分散檔案到高效 App 查詢之間的落差。

---

## 1. `learning_library_sources_index.json`

### Sources Index 查詢需求

- 主頁 (Home) 的內容列表顯示。
- 根據 `type` (**video/dialogue/article**), `level`, `topics` 進行過濾與搜尋。
- 提供基本媒體資訊 (thumbnail, duration) 以便在列表顯示，不需讀取完整 source 內容。

### Sources Index 為何是 Artifact？

- **效能**: 原始來源分散在 `core/video`, `core/dialogue`, `core/article`，App 若在啟動時掃描數百個檔案會過慢。
- **整合**: 將各類 source 的 metadata 與 `i18n` 的標題合併。

### Sources Index Schema

```typescript
interface SourcesIndex {
  sources: {
    id: string;          // src.ko.{type}.{slug}
    type: 'video' | 'dialogue' | 'article' | 'story' | 'lesson' | 'podcast';
    mediaId?: string;    // YouTube ID 或音檔 ID
    title: string;       // Localized (zh_tw)
    level: string;       // A1, A2, B1...
    thumbnail_url?: string;
    duration?: number;   // seconds (主要針對 video/podcast)
    topic_refs: string[];
    knowledge_refs: string[];
  }[];
}
```

---

## 2. `learning_library_sentences.json` (Decided: Required)

### Sentences 查詢需求

- **學習核心內容**: 當進入 `SourceDetailScreen` 時，App 需要顯示對話或影片的每一行原文、翻譯與時間軸。
- **知識點掛載**: 每一句對應到的 `knowledge_refs` 與 `vocab_refs`。

### Sentences 為何是 Artifact？

- **避免 Raw File 依賴**: App 在 artifact 模式下不應直讀 `content-ko` 原始 source 檔（如 `core/video/*.json`），以免暴露原始結構變動風險。
- **正規化輸出**: 將影片、對話、文章三種不同 input 結構，統一轉化為 App 顯示層最易消費的 `Sentence` 陣列。

### Sentences Schema

```typescript
interface SentencesLibrary {
  index: {
    [source_id: string]: {
      sentences: {
        id: string;
        surface_ko: string;
        translation: string;
        start_ms?: number;
        end_ms?: number;
        knowledge_refs: string[];
        topic_refs: string[];
        vocab_refs: string[];
      }[];
    };
  };
}
```

---

## 3. `learning_library_knowledge.json`

### Knowledge 查詢需求

- **Knowledge Lab Home**: 顯示所有語法與句型清單。
- **Knowledge Detail**: 顯示特定知識點的正文與例句。
- **Source Context**: 在學習影片時，點擊連結彈出對應的知識點簡介。

### Knowledge 為何是 Artifact？

- **本地化合併**: 將 `content/core/learning_library/knowledge` (結構) 與 `content/i18n/zh_tw/learning_library/knowledge` (中文解說) 合併。

### Knowledge Schema

```typescript
interface KnowledgeLibrary {
  knowledge_items: {
    id: string;
    kind: 'grammar' | 'pattern' | 'connector' | 'expression' | 'usage';
    subcategory: string;
    level: string;
    tags: string[];
    surface: string;     // 韓文標記 (e.g. ~이에요/예요)
    title: string;       // Localized
    summary: string;     // 簡介
    explanation: string; // 詳細解說 (Markdown)
    usage_notes: string[];
    example_bank: {
      ko: string;
      zh_tw: string;
      source_ref?: string; // 關聯的 source ID
    }[];
  }[];
}
```

---

## 4. `learning_library_topics.json`

### Topics 查詢需求

- **Topic Browsing**: 顯示主題列表 (如：時間、顏色、地點)。
- **Topic Detail**: 顯示該主題下的推薦單字、句型與學習素材。

### Topics 為何是 Artifact？

- **階層展開**: 將 parent/child 關係展開，並整合 metadata。

### Topics Schema

```typescript
interface TopicsLibrary {
  topics: {
    id: string;
    title: string;
    category: string;    // Family ID
    level: string;
    summary: string;
    parent_id?: string;
    knowledge_refs: string[];
    vocab_refs: string[];
    sentence_refs: string[];
    source_refs: string[];
  }[];
}
```

---

## 5. `learning_library_links.json`

### Links 查詢需求

- **反查 (Reverse Lookup)**: 哪些影片有用到這個文法？ (Knowledge Detail 頁面顯示)。

### Links 為何是 Artifact？

- **集中管理**: Source Truth (影片本體) 不應頻繁改動，新發現的關聯存放在 links artifact 中。

### Links Schema

```typescript
interface LinksLibrary {
  links: {
    id: string;
    origin_id: string;   // 起點 (sentence_id 或 source_id)
    target_id: string;   // 終點 (通常是 knowledge_id, topic_id)
    relationType: 'teaches' | 'uses' | 'example_of' | 'related_to';
  }[];
}
```

---

## 6. `learning_library_vocab_sets.json` (Decided: Required)

### Vocab Sets 決策說明

**必須單獨存在**。

- **原因**: 它定位為「教學挑選層」。一個主題只需要教 20 個核心單字，而字典可能有 2000 個。
- **職責**: App 需要快速載入某主題的「字型、翻譯、發音」。

### Vocab Sets Schema

```typescript
interface VocabSetsLibrary {
  vocab_sets: {
    id: string;
    surface: string;
    title: string;       // Localized 教學翻譯
    topic_refs: string[];
    dictionary_atom_ref?: string; // 選填，連結到正式字典
  }[];
}
```

---

## 關鍵決策與落地方案

1. **Intake 隔離原則**: App 在啟動時載入上述 Artifact。**嚴禁在 artifact 模式下跨 Repo 讀取 `content-ko` 的原始私有檔案**。所有的顯示需求必須由 pipeline 打包進 artifact。
2. **多類型支援**: Pipeline 必須掃描 `core/video`, `core/dialogue`, `core/article` 三大目錄，並將其統一正規化為 `sources_index` 與 `sentences` payload。
3. **i18n 策略**: Pipeline 會根據 `TARGET_LANG` (如 `zh_tw`) 產出對應的一組檔案。
4. **Link 的威力**: 所有的 `refs` 應在 pipeline 階段進行引用完整性檢查 (Referential Integrity)。
