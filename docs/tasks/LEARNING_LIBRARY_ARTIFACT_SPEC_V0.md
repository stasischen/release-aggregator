# Learning Library Artifact Spec v0

## Goal

定義 `content-pipeline` 輸出的正式 artifact 格式。這些文件是 `lingo-frontend-web` 消費的唯一標準，解決了從原始分散檔案到高效 App 查詢之間的落差。

---

## 1. `learning_library_sources_index.json`

### Sources Index 查詢需求

- 主頁 (Home) 的內容列表顯示。
- 根據 `type` (video/dialogue), `level`, `topics` 進行過濾與搜尋。
- 提供基本媒體資訊 (thumbnail, duration) 以便在列表顯示，不需讀取完整 source 內容。

### Sources Index 為何是 Artifact？

- **效能**: 原始來源分散在 `core/video` 與 `core/dialogue`，App 若在啟動時掃描數百個檔案會過慢。
- **整合**: 將 `core` 的 metadata 與 `i18n` 的標題合併。

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
    duration?: number;   // seconds
    topic_refs: string[];
    knowledge_refs: string[];
  }[];
}
```

### Sources Index Sample Shape

```json
{
  "sources": [
    {
      "id": "src.ko.video.79Pwq7MTUPE",
      "type": "video",
      "mediaId": "79Pwq7MTUPE",
      "title": "Vlog: 輕鬆聽韓文",
      "level": "A1",
      "thumbnail_url": "https://img.youtube.com/vi/79Pwq7MTUPE/0.jpg",
      "duration": 345,
      "topic_refs": ["topic.time.weekday"],
      "knowledge_refs": ["kg.beginner.present.copula"]
    }
  ]
}
```

---

## 2. `learning_library_knowledge.json`

### Knowledge 查詢需求

- **Knowledge Lab Home**: 顯示所有語法與句型清單。
- **Knowledge Detail**: 顯示特定知識點的正文與例句。
- **Source Context**: 在學習影片時，點擊連結彈出對應的知識點簡介。

### Knowledge 為何是 Artifact？

- **本地化合併**: 將 `content/core/learning_library/knowledge` (結構) 與 `content/i18n/zh_tw/learning_library/knowledge` (中文解說) 合併。
- **分類聚合**: 將所有 kind (grammar, pattern...) 聚合以便 App 一次載入。

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

### Knowledge Sample Shape

```json
{
  "knowledge_items": [
    {
      "id": "kg.beginner.present.copula",
      "kind": "grammar",
      "subcategory": "copula",
      "level": "A1",
      "tags": ["identity", "daily_life"],
      "surface": "~이에요/예요",
      "title": "是 (肯定句) ~이에요/예요",
      "summary": "用於名詞後，表示「是某物」或「是某人」。",
      "explanation": "### 形狀變化\n- 有收音: ~이에요\n- 無收音: ~예요",
      "usage_notes": ["這是非正式尊重的敬語結尾"],
      "example_bank": [
        { "ko": "학생이에요.", "zh_tw": "是學生。", "source_ref": "src.ko.dialogue.a1_01" }
      ]
    }
  ]
}
```

---

## 3. `learning_library_topics.json`

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

## 4. `learning_library_links.json`

### Links 查詢需求

- **反查 (Reverse Lookup)**: 哪些影片有用到這個文法？ (Knowledge Detail 頁面顯示)。
- **精準標記**: 在影片播放時，哪個 `sentence` 對應到哪個 `knowledge_item`。

### Links 為何是 Artifact？

- **集中管理**: Source Truth (影片本體) 不應頻繁改動，新發現的關聯存放在 links artifact 中。
- **圖譜轉化**: 將原始 `links/` 目錄的片段檔案，轉化為 App 可快速索引的字典。

### Links Schema

```typescript
interface LinksLibrary {
  links: {
    id: string;
    source_id: string;   // 起點 (通常是 sentence_id 或 source_id)
    target_id: string;   // 終點 (通常是 knowledge_id, topic_id)
    relationType: 'teaches' | 'uses' | 'example_of' | 'related_to';
  }[];
}
```

---

## 5. `learning_library_vocab_sets.json` (Decided: Required)

### Vocab Sets 決策說明

**必須單獨存在**。

- **原因**: 它定位為「教學挑選層」。一個主題只需要教 20 個核心單字，而字典可能有 2000 個。
- **職責**: App 需要快速載入某主題的「字型、翻譯、發音」，而不需要加載龐大的正式字典層。

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

1. **i18n 策略**: Pipeline 會根據 `TARGET_LANG` (如 `zh_tw`) 產出對應的一組檔案。App 根據使用者語系切換讀取的 artifact 路徑。
2. **不含 Source Body**: `learning_library_sources_index.json` 只含 metadata。真正的影片/對話內容 (sentences) 仍維持在獨立的原文檔案或大型單檔，本 artifact 僅作為導航入口。
3. **Link 的威力**: 所有的 `refs` 應在 pipeline 階段進行引用完整性檢查 (Referential Integrity)。
