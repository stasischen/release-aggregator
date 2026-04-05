# Knowledge Ingestion Plan v0

## Goal

定義如何將 `lingo-curriculum-source/reports` 中已整理的韓文教學內容，正規化為 `content-ko` 的正式 `learning_library/knowledge` 內容。

本文件聚焦：

- source classification
- source-of-truth strategy
- normalization rules
- canonical item / split / merge policy
- content-ko 落地策略
- pipeline impact

本輪不做：

- 大規模搬遷 report
- 完整自動轉換腳本
- frontend app 直接改動
- 把 planning 視為 migration 已完成

---

## Scope

本輪盤點的主要來源：

- `/Users/ywchen/Dev/lingo/lingo-curriculum-source/reports/youtube_beginner_grammar/clean_md`
- `/Users/ywchen/Dev/lingo/lingo-curriculum-source/reports/youtube_connective_endings/clean_md`
- `/Users/ywchen/Dev/lingo/lingo-curriculum-source/reports/youtube_connectors/clean_md`

本文件判斷是基於實際抽讀的代表性 source：

- `youtube_beginner_grammar/001_敬語結尾正式敘述 습니다ㅂ니다.md`
- `youtube_beginner_grammar/002_標準敘述一般禮貌體 아요어요해요.md`
- `youtube_beginner_grammar/003_非敬語 是 야이야.md`
- `youtube_beginner_grammar/004_主語助詞이가 이가.md`
- `youtube_connective_endings/105_...-아서---어서---해서-因為-一般原因.md`
- `youtube_connective_endings/072_...-(으)면-如果的話-一般條件.md`
- `youtube_connective_endings/096_...-지만-雖然但是.md`
- `youtube_connective_endings/108_...-거나-或者-或是-選擇.md`
- `youtube_connectors/001_...하필-偏偏.md`
- `youtube_connectors/002_...공교롭게도-不巧.md`
- `youtube_connectors/003_...의외로-出乎意料地.md`
- `youtube_connectors/004_...뜻밖에-意外地.md`

---

## Current Findings

### 1. Source Shape by Report Family

#### `youtube_beginner_grammar`

特徵：

- 多數是單一文法點或單一助詞/語尾
- 內容通常包含簡短說明、變化規則、例句
- 適合直接轉為 `knowledge_item`

判斷：

- 這批最接近 curated teaching drafts
- 多數可作為 first migration pack 的主要來源

#### `youtube_connective_endings`

特徵：

- 高度系列化，幾乎一篇一個接續語尾或句型
- 標題與例句清楚，但詳細限制、語用邊界不一定充分
- 適合進 `grammar > ending`，但需先做 normalize 與去重策略

判斷：

- 可作為高價值 migration input
- 不能直接視為最終 source of truth

#### `youtube_connectors`

特徵：

- 多數是獨立詞彙或固定連接語
- 結構簡單，主要由標題、語感描述、例句構成
- 較接近 `connector` 或部分 `expression`

判斷：

- 適合獨立為 `connector`
- 不應混進 `grammar`，除非實際涉及語尾或變化規則

---

## Source Role and Source-of-Truth Strategy

### System Roles

- `lingo-curriculum-source/reports`
  - 角色：`migration input` + `historical reference`
  - 用途：提供已整理的教學內容、原始影片脈絡、初步中文解說
  - 限制：不是正式 knowledge library 的長期編修主體

- `content-ko`
  - 角色：post-normalization source of truth
  - 用途：承載正式 `learning_library` 內容、可維護 canonical item、i18n overlay 與 links

- `release-aggregator`
  - 角色：planning / task / migration spec owner
  - 用途：承接 taxonomy、遷移規範、風險分流與 pipeline impact 定義

### Core Policy

`reports` 不應被定義成單純 raw notes，也不應被視為最終正式庫。

較準確的定位是：

- migration 時的主要輸入來源
- 正規化前的 curated drafts
- 遷移完成後仍保留為歷史依據與審計參考

正式勘誤、後續改寫、canonical ID 維護，應落在 `content-ko`，避免雙源同步。

### Intake Decision Rules

可直接進 `content-ko` knowledge overlay 的條件：

- 單一概念明確
- 標題可穩定抽出 canonical surface
- 例句品質足夠
- 解說沒有強依附影片語境

必須先 normalization / cleanup 的條件：

- 有多個語用功能混在同一篇
- 表面形式與中文標題不穩定
- 同概念在其他 report 也出現
- level 不明或例句風格不一致

不應直接進正式 knowledge library 的內容：

- 強依附影片演出或情緒包裝的描述
- 只有例句、缺乏穩定概念邊界的內容
- 高度多義但尚未拆清 usage 的高階語尾
- 本質上更接近 vocab / dictionary note 的單字說明

---

## Knowledge Taxonomy and Item Shape

### Primary Taxonomy

正式 taxonomy 仍採用：

- `grammar`
- `pattern`
- `connector`
- `expression`
- `usage`

但 ingestion 實作上必須區分「taxonomy」與「item shape」，避免把 `usage` 當成雜項主類。

### Shape Definitions

#### `grammar`

收錄：

- 助詞
- 語尾
- 活用規則
- 文法性 suffix / copula / honorific marker

判準：

- 涉及附著於詞幹、名詞、動詞或形容詞
- 有明確變化規則或接續條件

例：

- `~습니다/ㅂ니다`
- `~아요/어요/해요`
- `~야/이야`
- `~이/가`
- `-아서/어서/해서`
- `-(으)면`
- `-지만`

#### `pattern`

收錄：

- 多成分句型模板
- 可教成「框架」但不只是一個單一語尾
- 需要 slot 或句位說明的句型

判準：

- 重點在句型模板，不只是語尾本體
- 常以一個或多個 placeholder 教學

例：

- `N은/는 N이에요`
- `N이/가 어디예요?`
- 問候型自我介紹框架

#### `connector`

收錄：

- 獨立詞彙型連接詞
- 副詞性轉承語
- 固定連接片語

判準：

- 本身是獨立表面形式
- 不靠活用接在動詞詞幹後

例：

- `그리고`
- `그래서`
- `하지만`
- `하필`
- `공교롭게도`

#### `expression`

收錄：

- 固定說法
- 問候語
- 社交公式
- 慣用表達

判準：

- 教學價值來自整體固定表達，而非拆解規則

例：

- `안녕하세요`
- `처음 뵙겠습니다`
- `잘 부탁드립니다`

#### `usage`

定位：

- 不是預設的大宗 ingestion 類
- 主要作為其他 knowledge item 的附屬註解層、教學 block 或細部用法切分

只在以下情況才作為獨立 item：

- 該內容本身是穩定可引用的 usage convention
- 且不屬於特定 grammar / expression 的子說明

一般情況下：

- `usage` 應先落在 `usage_notes_zh_tw`
- 或 `teaching_blocks_zh_tw`

### Taxonomy Mapping Decisions

#### Endings

`ending` 統一歸類為 `grammar > ending`。

原因：

- 語尾本質上仍屬附著型文法標記
- 與詞幹接續、變化條件高度相關
- 若獨立成大類，會和 `pattern` / `connector` 邊界混亂

#### Connectors vs Grammar

規則：

- 若涉及動詞或形容詞的接續變化，進 `grammar`
- 若為獨立詞彙型連接詞，進 `connector`

例：

- `-지만` -> `grammar > ending`
- `하지만` -> `connector`

#### Greetings

問候語預設進 `expression > greeting`，而不是 `pattern`。

只有在內容主體是可替換 slot 的教學框架時，才進 `pattern`。

---

## Normalization Plan

### Unit of Conversion

原則不是「一份 report 必然對應一個 knowledge item」。

採以下規則：

- 一份 report 可對應一個 knowledge item
- 一份 report 也可能拆成多個 knowledge items
- 多份 report 也可能合併到同一個 canonical item

### Split Rules

一份 report 應拆成多個 item 的條件：

- 同一篇實際涵蓋兩個以上獨立概念
- 同一表面形式對應兩個以上核心語用功能，且 learner 需分開理解
- 報表同時在講「形式」與「固定表達」，而兩者可獨立復用

可先不拆、而改用 teaching blocks 的條件：

- 仍屬同一 canonical grammar item
- 只是說明不同語感、限制或常見搭配
- 拆開會造成過度碎片化

### Merge Rules

多份 report 應合併到同一 canonical item 的條件：

- 核心 surface 相同
- 教學主體相同
- 差異主要在例句、語氣或說明寫法

若多份 report 對同一概念解釋不同：

- 以 `content-ko` canonical item 作為整合點
- 優先保留最穩定、最可教學、最不依附影片脈絡的說明
- 不做 source-level versioned items
- 原始差異保留在 source refs 與 migration notes

### Canonical ID Strategy

禁止直接以 report 檔名產生正式 knowledge ID。

正式 ID 應以 normalized concept 命名，例如：

- `kg.grammar.copula.present_polite_ieyo`
- `kg.grammar.ending.reason_aseo_eoseo_haeseo`
- `kg.connector.sequence.geurigo`
- `kg.expression.greeting.annyeonghaseyo`

ID 組成建議：

- prefix: `kg`
- family: `grammar | pattern | connector | expression | usage`
- subcategory: `copula | ending | particle | honorific | greeting | contrast | cause | choice ...`
- slug: canonical concept slug

### Alias Policy

每個 canonical item 應允許保留：

- `surface`
- `surface_variants`
- `aliases_zh_tw`
- `source_refs`

即使 artifact v0 還未正式支援所有欄位，planning 上也應先保留概念，避免後續 merge 時失去來源對應。

### Field Mapping Rules

#### Required v0 Fields

- `id`
- `kind`
- `subcategory`
- `level`
- `tags`
- `surface`
- `title_zh_tw`
- `summary_zh_tw`
- `explanation_md_zh_tw`
- `usage_notes_zh_tw`
- `example_bank`

#### Optional v0.1+ Fields

- `surface_variants`
- `aliases_zh_tw`
- `teaching_blocks_zh_tw`
- `source_refs`
- `register`
- `constraints`

### Markdown-to-Knowledge Mapping

#### Title

來源：

- 第一層 `#` 標題

映射：

- `title_zh_tw`: 清理 emoji、系列編號後的人類可讀標題
- `surface`: 從標題中的韓文形式或箭頭後形式抽取 canonical surface

#### Description

來源：

- `## Description` 區塊主文

映射：

- `summary_zh_tw`: 1-2 句去包裝後的摘要
- `explanation_md_zh_tw`: 經整理後保留 markdown 的正文

處理原則：

- 去除純情緒性包裝句
- 保留規則、語境、限制、對照說明

#### Bullet Rules / Usage Notes

來源：

- 用法條列
- 接續條件
- 形式變化說明

映射：

- `usage_notes_zh_tw`

#### Example Sentences

來源：

- 成對的韓文句與中文翻譯

映射：

- `example_bank[].ko`
- `example_bank[].zh_tw`
- `example_bank[].source_ref`

### Structured vs Markdown Preservation

可保留 markdown 的欄位：

- `explanation_md_zh_tw`
- `teaching_blocks_zh_tw`

應結構化的欄位：

- `kind`
- `subcategory`
- `level`
- `tags`
- `surface`
- `usage_notes_zh_tw`
- `example_bank`

---

## First-Pack Gate

第一批只收：

- 低歧義
- 高 learner value
- 低 schema 壓力
- 低 merge 風險
- 容易掛進現有 app 與 links 模型

第一批暫不收：

- 高度多義語尾
- 語氣與語用需大量分層的高階表現
- 書面語、修辭語、感性語尾
- 需要更多 schema 才能表達 constraints 的項目

---

## content-ko Landing Strategy

### Directory Policy

延續既有 `learning_library/knowledge/...`，但避免一開始把 taxonomy 壓扁成單一層。

建議路徑：

```text
content-ko/content/
├── core/
│   └── learning_library/
│       └── knowledge/
│           ├── grammar/
│           │   ├── copula/
│           │   ├── ending/
│           │   ├── particle/
│           │   └── honorific/
│           ├── pattern/
│           │   ├── introduction/
│           │   ├── question/
│           │   └── sentence_frame/
│           ├── connector/
│           │   ├── sequence/
│           │   ├── contrast/
│           │   └── cause/
│           ├── expression/
│           │   ├── greeting/
│           │   └── social_formula/
│           └── usage/
└── i18n/
    └── zh_tw/
        └── learning_library/
            └── knowledge/
                ...
```

### Core / i18n Responsibility

- `core`
  - 存放 canonical structure
  - surface, kind, subcategory, level, tags, references

- `i18n/zh_tw`
  - 存放 title, summary, explanation, usage notes

### Expansion Policy

此結構應能支援未來新增：

- `grammar/ending`
- `grammar/particle`
- `grammar/honorific`
- `connector/*`
- `expression/*`

但 v0 不需要一次把全部 family 都填滿。

---

## Pipeline Impact

### Content Migration Only

以下可先視為 content migration 問題，不必動 pipeline schema：

- 新增 canonical knowledge items
- 新增對應 i18n 說明
- 建立 source-to-knowledge links
- 建立 sentence-to-knowledge links

### Likely Pipeline Additions

以下後續可能需要 schema / merge logic 增補：

- `source_refs` 支援
- `surface_variants` / alias merge
- `teaching_blocks_zh_tw` 支援
- duplicate detection / canonical merge hints

### Deferred Pipeline Work

本輪先不要動：

- 自動 ingestion script
- 大規模批次抽取
- source-level diff aware merge
- 複雜 graph query schema

---

## Risks

- 若未先定義 canonical ID 與 merge 規則，先搬內容會導致同概念重複入庫
- 若把 `usage` 當主要分類，知識庫會快速退化成雜項桶
- 若直接把 report 情緒包裝與影片語境搬進 knowledge，正式庫會不可維護
- 若一開始就大量收高階 connective endings，後續幾乎必須重構 schema

---

## Non-Goals

- 這份計畫不決定所有高階語尾的最終 taxonomy
- 這份計畫不要求立即自動化所有 report ingestion
- 這份計畫不把 reports 清空或淘汰

---

## Recommended Next Step

下一輪最適合做的是：

1. 先建立 `knowledge` canonical item spec 範本
2. 依本文件做一個小型 manual migration pack
3. 在實際遷移 8-15 個低風險 item 後，再決定是否值得寫 normalizer script

原因：

- 先用小批量驗證 split / merge / ID policy
- 比先寫 script 更能暴露 taxonomy 邊界問題
- 可避免在 schema 未穩前大量產生之後要回收的內容
