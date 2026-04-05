# Learning Library Schema Freeze v0

## Goal
根據目前 `lingo-frontend-web` prototype 已驗證過的學習流程（video/dialogue/article learning detail），正式凍結第一期資料合約 (v0)。

此 schema 將作為 `content-ko` learning overlay 的輸入規範，以及 `content-pipeline` 的輸出標準。

---

## 1. `source` (學習入口)

代表一個完整的學習素材，如一段影片、一篇對話或一篇文章。

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼，格式：`src.ko.{type}.{slug}` | 已驗證 |
| `type` | enum | `video`, `dialogue`, `article`, `story`, `lesson`, `podcast` | 已驗證 |
| `mediaId` | string | **Optional**: 用於播放器的媒體 ID (YouTube ID 或音檔 ID) | 已驗證 |
| `title` | string | 本地化標題 | 已驗證 |
| `level` | string | 難易度 (e.g. `A1`, `A2`, `B1`) | 已驗證 |
| `metadata` | object | 根據 type 不同而異 (如 video 有 `thumbnail_url`, `duration`) | 已驗證 |
| `sentence_refs` | string[] | 包含的句子 ID 清單 | 已驗證 |
| `topic_refs` | string[] | 關聯的主題 ID 清單 | 已驗證 |
| `knowledge_refs` | string[] | **Reserved**: 本 source 的主要教學核心知識點 | Reserved |

---

## 2. `sentence` (教學單元)

最小句子載體，承載翻譯、時間軸與與知識點的連結。

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼 (e.g. `sent.{source_id}.{index}`) | 已驗證 |
| `source_id` | string | 所屬 source ID | 已驗證 |
| `surface_ko` | string | 韓文原文 | 已驗證 |
| `translation_zh_tw` | string | 中文翻譯 | 已驗證 |
| `start_ms` | number | **Optional**: 影片對應開始毫秒 | 已驗證 |
| `end_ms` | number | **Optional**: 影片對應結束毫秒 | 已驗證 |
| `knowledge_refs` | string[] | 連結到 `knowledge_item` 的 ID 清單 | 已驗證 |
| `topic_refs` | string[] | 連結到 `topic` 的 ID 清單 | 已驗證 |
| `vocab_refs` | string[] | 連結到 `vocab_set_item` 的 ID 清單 | 已驗證 |

---

## 3. `knowledge_item` (教學知識點)

可重用的語法、句型、連接詞或用法解說。

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼 (e.g. `kg.beginner.present.copula`) | 已驗證 |
| `kind` | enum | `grammar`, `pattern`, `connector`, `expression`, `usage` | **Update v0** |
| `subcategory` | string | 細分類 (e.g. `copula`, `ending`, `greeting`, `sequence`) | **Update v0** |
| `level` | string | 難易度 | 已驗證 |
| `tags` | string[] | 自由標籤 (e.g. `polite`, `daily_life`) | **Update v0** |
| `surface` | string | 語法標記或句型框架 (e.g. `~이에요/예요`) | 已驗證 |
| `title_zh_tw` | string | 本地化名稱 | 已驗證 |
| `summary_zh_tw` | string | 簡介 (1-2 句話) | 已驗證 |
| `explanation_zh_tw` | string | 詳細解說 (Markdown) | 已驗證 |
| `usage_notes_zh_tw` | string[] | 使用注意事項/變化規則清單 | 已驗證 |
| `example_bank` | array | 例句池 (含 ko, zh_tw, source_ref) | 已驗證 |

---

## 4. `topic` (學習主題)

聚合相同主題下的單字、句型與內容來源。

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼 (e.g. `topic.time.weekday`) | 已驗證 |
| `title_zh_tw` | string | 本地化主題名稱 | 已驗證 |
| `category` | string | 主題家族 ID (e.g. `time`, `number`) | 已驗證 |
| `level` | string | 難易度 | 已驗證 |
| `summary_zh_tw` | string | 主題摘要 | 已驗證 |
| `parent_id` | string | **Optional**: 父層主題或家族 ID | 已驗證 |
| `knowledge_refs` | string[] | 該主題下的核心句型/語法 ID | 已驗證 |
| `vocab_refs` | string[] | 該主題下的核心詞彙 ID 清單 | 已驗證 |
| `sentence_refs` | string[] | 代表性例句 ID | 已驗證 |
| `source_refs` | string[] | 推薦內容來源 ID | 已驗證 |

---

## 5. `vocab_set_item` (教學詞彙集合)

**注意：這不是字典真相 (Dictionary Atom)，而是教學挑選層。**

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | 唯一識別碼 (e.g. `kv.time.weekday.monday`) | 已驗證 |
| `surface` | string | 韓文單字 (e.g. `월요일`) | 已驗證 |
| `title_zh_tw` | string | 中文翻譯 | 已驗證 |
| `topic_refs` | string[] | 關聯的主題 ID | 已驗證 |
| `dictionary_atom_ref` | string | **Reserved**: 連結到正式字典 Atom 的 ID | Reserved |

---

## 6. `links` (關聯索引)

正式化後，關係將從 `source` 或 `sentence` 內嵌改為獨立層描述（可由 pipeline 生成）。

| 欄位 | 類型 | 說明 | 驗證狀況 |
| --- | --- | --- | --- |
| `id` | string | Link 唯一碼 | 已驗證 |
| `source_id` | string | 起點 ID | 已驗證 |
| `target_id` | string | 終點 ID | 已驗證 |
| `relationType` | enum | `teaches`, `uses`, `example_of`, `related_to` | **Update v0** |

---

## 關鍵決策與限制

1. **核心原則**: `dictionary atoms` 和 `vocab_sets` 永遠維持兩層。`vocab_set` 只存教學用的表面資料或 index，不承載詞源真相。
2. **Taxonomy 擴充**: `knowledge_item` 引入 `kind` / `subcategory` 二級分類，目前 prototype 已驗證 `grammar`, `pattern`, `connector` 三大類。
3. **Reserved Fields**: 預留了 `relationType` 以便未來支援更細緻的圖譜查詢，但 Phase 1 仍以單純的 `refs` linking 為主。
4. **i18n 分離**: 所有標題與解說欄位 (suffix `_zh_tw`) 在 `content-ko` source 層將被拆分到 `i18n/` 目錄，但 build 後的 artifact 應包含合併後的結果。
