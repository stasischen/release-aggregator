# MDict 韓中字典內容清洗與導入計畫 (MDict Dictionary Ingest Plan)

## 任務目標
處理 `content-ko/content/staging/nikl_naver_rebuild/naver_zh_tw.jsonl` 中的 6580 筆未清洗 Naver/MDict 字典資料。
建立穩定的清洗 Skill，確保定義文字 (`definition_text_zh_tw` 與 `explanation`) 被正規化，並符合 `content_v2` dictionary inventory schema 的格式（例如區分 senses，去除 HTML tag / 冗餘符號，轉換簡體至繁體）。

## 執行策略：Pilot-First
為了避免大批次出錯，將採用「先建立 Skill → 試跑 Pilot → 驗證通過 → 大批次清理」的工作流。

## 執行步驟

### Phase 1: 盤點與規則定義 (Inventory & Rule Definition)
1. **讀取樣本**：讀取 `naver_zh_tw.jsonl` 前 10-20 行，觀察 `definition_text_zh_tw` 與 `explanation` 的雜訊特徵。
2. **清洗規則**：
   - 定義拆分多義詞 (senses) 的符號（如 `//`, `;`, 數字等）。
   - 修剪特殊空白、不可見字元、HTML tags。
   - 確認簡轉繁策略。
3. **對齊 V2 Schema**：輸出的 JSONL 需符合 `content_v2/inventory/dictionary/` 目錄下的 shard 格式 (`id`, `lemma`, `pos`, `status`, `metadata`, `definitions`)。

### Phase 2: 建立 Skill (Skill Creation)
1. 在 `content-ko/.agent/skills/mdict-dictionary-cleaning/` 建立 `SKILL.md`。
2. 撰寫具體的輸入/輸出範例與 SOP，指示 Agent 如何讀取原始 JSONL，轉換，並輸出到 V2 staging 目錄。

### Phase 3: Pilot Run (試跑驗證)
1. 挑選 Rank 1~50 的高頻詞作為 pilot batch。
2. 依照所建 Skill 進行清洗轉換。
3. 輸出到 `content-ko/content_v2/staging/dictionary/pilot_mdict.jsonl`。
4. 提供報告給 User (Controller) 驗證。

### Phase 4: Full Batch Run (全量執行)
1. 在 Pilot 通過後，分批 (Batch of ~500) 處理剩下的 6530 筆。
2. 按 POS 將結果分類寫入 `content_v2/inventory/dictionary/<pos>.jsonl`。
3. 更新 `manifest.json` 與相關索引。
