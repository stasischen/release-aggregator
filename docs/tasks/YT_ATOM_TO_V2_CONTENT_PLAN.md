# YouTube Atom 轉 V2 Content 計畫 (YT Atom to V2 Content Plan)

## 任務目標
將既有存放在 `content-ko/content/core/video_atoms/` 的 V5 原型 `_atoms.json` 檔案，全面升級並轉換為符合 `content_v2` 標準的 `content_item.v1` Schema。同時，確保這些原子的對齊度通過 V2 的 atom coverage 工具驗證。

## 執行策略：Skill-Driven & Validated
在 V2 架構下，所有教學內容 (學習庫、對話、影片) 的底層儲存結構逐漸統一。我們將借鏡 Sentence Bank Atomization 的驗證機制，在轉換的同時排除任何遺漏的字典實體。

## 執行步驟

### Phase 1: 結構解析與 Skill 建立 (Schema & Skill)
1. 讀取 `content_v2/inventory/content_assets/dialogue/A1-01.json` 做為基準參考。
2. 在 `content-ko/.agent/skills/yt-atom-v2-conversion/` 建立 `SKILL.md`。
3. **Skill 規範要點**：
   - 定義 ID Scheme：`domain: "video"`, `item_id: "VIDEO_<ID>:turn_<N>"` 等。
   - 解析原 `_atoms.json`，將 `words` -> `atoms` 的對照拉平，符合 V2 `atoms: []` 的陣列規格。
   - **強制整合驗證**：在轉出 V2 檔案後，Agent 需利用與 Sentence Bank 相同的 `scripts/ops/check_atom_coverage.py` 工具，驗證這批 atom 是否完全落在 V2 字典與知識庫內。

### Phase 2: Pilot Run (試跑與孤兒檢查)
1. 針對最近剛做完的 `eF65dUUDcEQ` (Talking About Daily Routines)，取前 20 個 turn 作為資料。
2. 依照新 Skill 轉換為 `content_v2/staging/content_assets/video/eF65dUUDcEQ.json`。
3. 執行 Coverage Gate。如果出現 orphans，則需依序放入 tail dictionary 或是更新 base dictionary，確保 0 orphans 才能放行。

### Phase 3: 全量轉換 (Full Batch Conversion)
1. 待 Pilot OK 且涵蓋率過關後，使用腳本或 Agent 批次掃過剩餘的 20+ 部影片。
2. 全數輸出至 `content_v2/inventory/content_assets/video/`，並確認全數通過 atom coverage 驗證。
