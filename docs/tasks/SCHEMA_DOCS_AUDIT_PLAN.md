# Schema 與技術文件盤點同步計畫 (Schema & Docs Audit Plan)

## 任務目標
隨著 `content_v2` 架構 (Dictionary, Sentence Bank, Knowledge Lab) 的快速推展與上線，相關的 JSON Schema 文件與技術說明文檔 (Markdown) 可能產生資訊落差 (Drift)。
本任務負責跨庫 (content-ko, core-schema, release-aggregator) 進行全面盤點，確保所有的合約、Schema 檔案與開發者手冊都是最新、最一致的版本。

## 執行步驟

### Phase 1: Snapshot & Map (現況快照與對應)
1. **收集 V2 真實資料**：抓取 `content_v2` 目錄下最具代表性的樣本 (例如 A1-01.json, EX-001.json, G-KO-PROMISE.json, dictionary manifest)。
2. **對照 Schema 庫**：前往 `core-schema/schemas` 尋找對應的定義檔（如 `dictionary_core.schema.json`, `atom.schema.json` 等）。
3. **對照技術文檔**：檢索 `content-ko/docs/tech/` 與 `release-aggregator/docs/guides/` 下的所有架構與 Schema 說明檔。

### Phase 2: Gap Analysis (斷層分析)
1. 找出尚未定義到 `core-schema` 中的 V2 結構 (例如 content_v2 JSON 中出現了新的 tagging 或 provenance 欄位)。
2. 找出舊版技術文件中仍在使用 `assets/content/production` 或 Legacy V4/V5 術語的落後段落。

### Phase 3: Alignment Execution (同步更新)
1. **文件更新**：更新或建立正式的 `CONTENT_V2_INVENTORY_CONTRACT.md` 等，取代過時筆記。
2. **Schema 修補**：產出 `core-schema` 缺漏的 json schema 給後續 PR 納入。
3. 把前端架構文件 (如剛剛在 mac 上完成的 frontend realignment plan) 中的核心資料綁定結論，反饋回後端的合約說明中。
