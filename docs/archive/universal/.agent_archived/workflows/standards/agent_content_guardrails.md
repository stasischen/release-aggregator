# Content Pipeline Guardrails (AI Agent Self-Check)

# 內容管線防波堤 (AI Agent 自我檢查表)

> [!IMPORTANT] > **READ THIS BEFORE PROCESSING ANY CONTENT (YARN/CSV/DICT).** > **在處理任何內容（YARN/CSV/DICT）之前，必須閱讀此文件。**

## 🛑 1. The "Target Language First" Principle / 「目標語言優先」原則

In Phases 1 and 2, focus ONLY on the target language linguistically.
在第一和第二階段，語言學上僅專注於目標語言。

- **Rule**: `yarn -> csv -> chunk` extraction MUST NOT include translations.
- **規則**：`yarn -> csv -> chunk` 提取過程**絕對不能**包含翻譯。
- **Why**: Keeps the mapping pure and prevents English/Learner contamination during atomization.
- **原因**：保持映射纯淨，防止在原子化過程中受到英文或學習者語言的污染。

## ⚠️ 2. Choice Line Format (`->`) / 選項行格式 (`->`)

- **Format**: `-> Target Language Text #line:ID`
- **Rule**: Choices must be in the target language (e.g., Korean, German). English belongs in the `//` comment on the next line.
- **規則**：選項必須使用目標語言。英文應放在下一行的 `//` 註解中。
- **Extraction**: When generating CSV, extract the target text ONLY into `text_source`. `trans_en` should be handled in Phase 3.5 Enrichment.
- **提取**：生成 CSV 時，僅將目標文本提取至 `text_source`。`trans_en` 應在 Phase 3.5 增強階段處理。

## 🧪 3. Atomization & Reconstruction / 原子化與重構

- **Strict Rule**: `verify_reconstruction.py` must pass with 100% accuracy.
- **嚴格規則**：`verify_reconstruction.py` 必須以 100% 準確率通過。
- **Manual Patches**: Always check if a manual patch exists before assuming LLM error.
- **手動修補**：在假設 LLM 出錯之前，先檢查是否存在手動修補檔。

## 🔄 4. Pipeline Execution / 管線執行

- **Never** skip the `Linguistic Audit Protocol`.
- **絕對不要**跳過「語言稽核程序」。
- **Consistency**: Use `python -m tools.v5.core.update_db <lang>` followed by `merger` and `audit_view` for validation.
- **一致性**：使用 `update_db` 同步內容，接著使用 `merger` 與 `audit_view` 進行視覺驗證。

## 🤖 5. Agent Anti-Patterns (Avoid These!) / Agent 反模式（切記避免！）

1. **mixing Logic**: Trying to translate AND atomize at the same time. (❌)
2. **Ignoring Errors**: Proceeding with Phase 2 if Phase 1 reconstruction failed. (❌)
3. **Manual CSV Edits**: Editing `1_scenario_csv` manually instead of fixing Yarn. (❌)
4. **Indentation Loss**: Losing the space before `->` or `[[jump]]` which breaks Yarn logic. (❌)

## 🔗 6. Phase Connection Integrity / 階段銜接完整性

Each phase MUST 100% connect to the previous one.
每個階段必須 100% 銜接前一個階段。

- **Yarn -> CSV**: Every `#line:ID` in Yarn must exist in the generated CSV in `1_translation/` and `2_atoms/`.
- **CSV -> Full View**: Every row in `5_full_view/` MUST have a valid `text_source` and `trans_zh_TW/en/ja/es/ru/id`.
- **CSV -> Dictionary**: Every unique Atom ID (surface + pos) used in Phase 2 must be synced to Phase 4 (Dictionary).
- **Dictionary -> Build**: The final builder MUST successfully embed dictionary definitions into the atoms JSON.

---

**Last Updated**: 2026-01-16 (V5 Modular Alignment)
