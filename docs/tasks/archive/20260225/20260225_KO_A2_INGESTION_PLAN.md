# Implementation Plan - content-ko A2 Ingestion & V5 Standardization

此計畫旨在匯入 `lllo` 中的 A2 課程內容，並完成 V5 原子化標籤的初期映射與審核。

## Proposed Changes

### [Component] content-ko Scripts & Ingestion

#### [MODIFY] [run_rule_tests.py](file:///e:/Githubs/lingo/content-ko/tests/run_rule_tests.py)

- 修復 `ModuleNotFoundError`: 將 `from scripts.core.tokenizer import KoreanTokenizer` 改為 `from engine.tokenizer import KoreanTokenizer`。

#### [MODIFY] [run_mapping_pipeline.py](file:///e:/Githubs/lingo/content-ko/scripts/ops/run_mapping_pipeline.py)

- 修復報告名稱硬編碼：將 `f"A1_Validation_{timestamp}"` 改為更能反映掃描內容的名稱（例如根據 `ALLOWED_LEVEL_PREFIXES`）。

#### [EXECUTE] Manual Full Audit (V5 Surgeon 模式)

由於 Gemini API 全量審核較慢，本階段改採 **Agent-driven GSD Surgeon** 模式執行：

1. **Prep Inputs**：執行 `python scripts/review/01_prep_inputs.py --lesson A2-XX`，將引擎映射結果（Engine candidates）導出至 `dialogue_inputs/`。
2. **Build Baseline**：執行 `03_build_gold.py` 建立初始 Gold Baseline（此時尚未進行人工修正）。
3. **Dump Surgery**：執行 `04_gsd_surgeon.py dump` 產出簡化版的 `surgery_A2-XX.json` 供 Agent 審閱。
4. **Agent Review (V5 Surgery)**：
   - 由 Agent (Antigravity) 讀取 `surgery_A2-XX.json`。
   - 根據 `KO_DATA_STANDARDIZATION_PROTOCOL.md` 規範，對每一條 Token 進行「全量人工校對」。
   - 重點修正：對 `세요`, `았어요`, `이에요` 等進行原子化手術拆解。
5. **Apply & Lock**：執行 `orchestrator.py apply` 正式合併修正並鎖定 A2 Golden Baseline。

#### [EXECUTE] Ingestion

- 執行 `python scripts/ops/import_lllo_raw.py`。
- 預期產出：
  - `content/core/dialogue/A2/*.json`
  - `content/core/grammar/ko__g__a2__*.json`

#### [EXECUTE] Dictionary & Verification (Stage 3 & QA 詳細流程)

1. **Atoms Synchronization (Atom 同步)**：
   - 執行 `python scripts/ops/build_dictionary.py`。
   - 掃描 Stage 2 的所有 `final_atom_id`，若在 `content/core/dictionary/atoms/` 找不到對應的 JSON，則自動產出骨架檔案。
   - 確保所有 V5 Atoms 都有正式的 ID 定義與詞類歸檔。
2. **Reconstruction Audit (還原度審計)**：
   - 執行 `python scripts/ops/audit_reconstruction.py`。
   - 這是最後的「品質門檻」。系統會模擬讀取 A2 課文，根據 Atoms 組合出字串，並與 `lllo` 原始碼進行「逐字比對」 (Byte-for-byte check)。
   - **目標**：A2 課程必須達到 100% 還原（Pass Rate = 1.0）。
3. **Handoff Artifact Generation (產出遞交文件)**：
   - 產出 `artifacts/stage3/handoff.stage-03.json`。
   - 包含機器可讀的指標：`empty_senses_count`（是否有漏掉的語意）、`schema_valid` 等。
4. **Gates Final Check (門檻總結)**：
   - 確認 `unresolved_ratio` <= 0.10。
   - 確認 `reconstruction_pass_rate` >= 0.98 (A級標準)。

#### [EXECUTE] Mapping Pipeline (Stage 2 詳細流程)

1. **Tokenization (語彙切分)**：
   - 讀取 `content/core/dialogue/A2` 中的 JSON 課程原始碼。
   - 使用 `KoreanTokenizer` 將韓文句子切割為語節 (Eojeol)。
2. **Atomic Mapping & Rules Engine (原子化映射與規則引擎)**：
   - **字典查表**：優先比對 `mapping_*.json` 中的已知詞條。
   - **語法拆解 (Heuristic Parsing)**：若字典無匹配，由 `RulesEngine` 依據 `engine/rules/*.json` 定義的規則（如：語幹 + 詞尾 `았/었`, `-네요`）進行原子化拆解。
   - **標記轉換**：將拆解結果轉換為 V5 規範的 Atom IDs（例如 `ko:v:하다` + `ko:e:yo:어요`）。
3. **QA Gates 驗證**：
   - **還原度檢查 (Reconstruction Check)**：確保拆解後的 Atoms 重新組合後，字面必須與原始 Surface Form 100% 一致。
   - **重複檢查**：確保同一個詞在不同上下文中沒有產生衝突的 ID。
4. **輸出產物**：
   - `artifacts/stage2/lessons/A2-*.jsonl`：每課的斷句結果。
   - `reports/A2_Validation_*.txt`：包含未解析比例 (Unresolved Ratio) 與還原成功率。

## Verification Plan

### Automated Tests

- 執行 `python tests/run_rule_tests.py` 確保規則引擎基礎功能正常。
- 執行 `python scripts/ops/audit_reconstruction.py` 驗證 A2 內容是否能 100% 還原（目標 pass rate >= 0.98）。

### Manual Verification

- 使用 `content-ko/scripts/tools/dict_viewer/index.html` 預覽 A2 課程，確認斷句與詞典彈窗基本正確。
- 檢查 `reports/` 下生成的最新驗證報告，確認 `unresolved_ratio` 低於 10%。
