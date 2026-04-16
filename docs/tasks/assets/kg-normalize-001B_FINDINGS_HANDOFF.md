# kg-normalize-001B Findings & Handoff

本文件記錄了在執行第一批有界限正規化 (Bounded Normalization Batch) 時發現的結構問題與 Schema 演進衝突，交接給後續對應的 Agent 執行修正。

## 1. 發現與阻礙 (Findings & Blockers)

### 1-1. 例句 ID 配發衝突 (ID Allocation Collision)
由於目前其他 Agent 可能正在進行不同的 Ingestion Batch（產生新的 `ex.ko.s.XXXXXX` ID），本批次中若自行佔用 `000457` 到 `000466` 這些 ID 段，可能會引發資源競爭與索引衝突。
**交接建議**：後續恢復 `그래서` 與 `그리고` 例句時，必須透過中央機制（如 Python 解析現有庫中最大 ID 或交給 ingestion script 動態分配）來指派，避免 Hardcode。

### 1-2. V5 Schema 演進 (Schema Evolution Issue)
在重建例句時遭遇驗證腳本 (`validate_learning_library_schema.py`) 強制報錯，顯示 V5 Schema 已經有過更新。舊版備份 (20260414_235715) 以及許多 legacy 檔案中使用的部分欄位已經被棄用且強制阻擋：
- **[Core]** `surface_ko` -> 必改為 `ko`，遺留版欄位會被判為 forbidden。
- **[I18n]** `translation_zh_tw` -> 必改為 `translation`，遺留版欄位會被判為 forbidden。
**交接建議**：在所有救援例句與未來遷移中，必須對齊最新的 `ko` 及 `translation` 欄位名稱。

---

## 2. 待執行修復清單 (Pending Fixes)

請對應的 Agent 在安全環境下執行以下三個修正任務：

### 任務 A: Modifier Surface 去重複化
- **目標**：目前的 `kg.grammar.modifier.v_eun` 與 `kg.grammar.modifier.adj_noun` 的 `surface` 和 `title` 皆為 `"ㄴ/은 + 名詞"`。
- **作法**：
  - `v_eun` 改為 `"動詞 + ㄴ/은 + 名詞 (過去)"`
  - `adj_noun` 改為 `"形容詞 + ㄴ/은 + 名詞 (現在)"`

### 任務 B: A1 Adverbs 功能性標籤 (Tags) 補強
- **目標**：部分副詞的 tags 僅有 `["beginner", "v5_ingestion"]`，缺乏功能分類。
- **作法**：
  - 加 `time`：`akka`, `geumbang`, `najunge`, `ittaga`, `got`, `jamsi_hu`, `mak`, `eolleun`, `dangjang`
  - 加 `degree`：`yakgan`, `kkwae`
  - 確保所有副詞都有 `grammar` 與 `adverb` 標籤。

### 任務 C: Pilot Connector 救援與重建
- **目標**：從 `runs/backup/polluted_kg_lab/` 救援出 `그래서` (geuraeseo) 與 `그리고` (geurigo)。
- **作法**：
  - 將備份的 I18n KI 打平為 V5 格式 (移除 `_zh_tw` 後綴欄位)。
  - 重建遺失的 Core/I18n 例句，並賦予不衝突的 ID。
  - **切記**：例句必須遵守最新的 Core `ko` 與 I18n `translation` 欄位規範。
