# content-ko Overlay Migration Mapping


## Goal

定義 `content-ko` 內 `learning_library` overlay 的目錄結構，並列出第一批 (Phase 1) 正式遷移的內容對照表。

---


## 1. content-ko Overlay Layout Plan

根據 `Learning Source Multi-Layer Architecture` 協議，我們不破壞既存的 `core/dialogue|video` 結構，而是建立一個平行 overlay。


### 目錄結構

```text
content-ko/content/
├── core/
│   ├── dialogue/           # Source Truth: 對話原文、基礎 metadata
│   ├── video/              # Source Truth: 影片原文、時間軸
│   ├── grammar/            # Legacy Source: 原始教學素材
│   └── learning_library/   # [NEW] Learning Overlay
│       ├── knowledge/      # 知識點 (grammar, patterns, connectors, expressions, usage)
│       ├── topics/         # 學習主題 (time, number, color...)
│       ├── vocab_sets/     # 教學詞彙集合 (非字典真相)
│       └── links/          # 關係索引 (source-to-knowledge, sentence-to-topic...)
└── i18n/
    └── zh_tw/
        ├── dialogue/
        ├── video/
        ├── grammar/
        └── learning_library/ # [NEW] 教學層本地化
            ├── knowledge/    # 解說、標題、注意事項
            ├── topics/       # 主題名稱、摘要
            └── vocab_sets/   # 教學義項翻譯
```


### 職責說明

- **Source Truth**: 韓文原文與基礎媒體 ID，維持在 `core/video` 或 `core/dialogue`。
- **Learning Overlay**: 負責「教什麼」與「怎麼連」，不重複存放原文。
- **App Artifact**: 由 pipeline 執行，將上述多目錄合併成 app 最終使用的 `learning_library_*.json`。

---


## 2. First Migration Pack (Phase 1)

第一批遷移內容包含已在 prototype 驗證過的最小集合。


### A. Source Mapping (入口)

| Source ID | 來源 (Source of Truth) | 類別 |
| --- | --- | --- |
| `src.ko.video.79Pwq7MTUPE` | `content/core/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json` | video |
| `src.ko.dialogue.a1_01` | `content/core/dialogue/A1/A1-01.json` | dialogue |
| `src.ko.article.a1_01_intro` | — (App Prototype 新增，待正式化入 content-ko) | article |


### B. Knowledge & Topics (知識庫)

| Item ID | 類別 | 子類別 | 說明 |
| --- | --- | --- | --- |
| `kg.beginner.present.copula` | grammar | copula | `~이에요/예요` (A1-1 核心) |
| `kg.beginner.honorific.ssi` | grammar | honorific | `~씨` (人名接尾語) |
| `kg.beginner.ending.*` | grammar | ending | 預留分類位置 (如 `~아서/어서`) |
| `kp.daily.greeting.annyeong` | pattern | greeting | `안녕하세요` 家族 |
| `kp.daily.polite_question` | pattern | question | 敬語提問框架 |
| `topic.time.*` | topic | time | Time family (weekday, relative_day, clock_time) |


### C. Vocab Sets (教學詞表)

| Vocab ID | 表面字 | 教學標題 | 所屬主題 |
| --- | --- | --- | --- |
| `kv.time.weekday.saturday` | 토요일 | 星期六 | `topic.time.weekday` |
| `kv.time.relative_day.today` | 오늘 | 今天 | `topic.time.relative_day` |
| `kv.time.clock.nine_oclock` | 9시 | 九點 | `topic.time.clock_time` |

---


## 3. Migration Mapping Rules

1. **ID 一致性**: 遷移後的 ID 必須與 `LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md` 一致，且能直接對應 prototype seed 內的舊 ID。
2. **Path Mapping**:
    - 韓文本體落於 `content/core/learning_library/{kind}/{category}/{id}.json`
    - 中文本體落於 `content/i18n/zh_tw/learning_library/{kind}/{category}/{id}.json`
3. **Data Integrity**:
    - `sentence` 與 `source` 的連結由 `links/` 目錄負責，不要硬塞回 `core/video` 原始 JSON 裡，以保持 Source Truth 的純粹。

---


## 4. Next Step: 第二輪工作規劃 (Pipeline)

此 mapping 完成後，第二輪將實作：

- `content-pipeline` 的 `normalize-learning-library` 指令。
- 自動從 `core/*` 掃描，並根據 `learning_library/links` 生成最終關聯 artifact。
- 產出 `learning_library_sources_index.json` 供 App Home 使用。
