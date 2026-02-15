---
description: Phase 1 SOP: Professional Translation & Review
---
# Phase 1 Translation: Standard Operating Procedure (SOP)

本階段負責生成並驗證 `1_translation` 中的內容。
This phase handles generation and validation of content in `1_translation`.

## 🔄 Workflow

> [!IMPORTANT]
> **ANTI-AUTOPILOT RULES (防偷懶守則)**
>
> 1. **Sequential Execution**: DO NOT translate all languages in one go. You MUST process them one by one.
> 2. **Mandatory Gates**: After translating EACH language, you MUST call `notify_user` for review before starting the next language.
> 3. **Manual Override**: Act as a **Professional Linguistic Expert**. If you produce "machine-like" or "translationese" content, it is a FAILURE.
> 4. **Audit Report**: You MUST create and update local `audit_report_{lang}_p1.md` as you work.

## 2. Field Definitions (欄位定義)

| Column        | Description                                                         | Example      |
| :------------ | :------------------------------------------------------------------ | :----------- |
| `line_id`     | **[Unique Key]** Yarn Line ID (#line:xxxx).                         | `line:001`   |
| `speaker`     | **[Metadata]** Speaker name or Paragraph ID (P1..).                 | `Lisa`, `P1` |
| `type`        | **[Content Type]** `dialogue`, `option`, or `sentence`.             | `dialogue`   |
| `text_source` | **[Source Text]** Original text in source language.                 | `안녕하세요` |
| `trans_zh_TW` | **[Target 1]** Traditional Chinese translation.                     | `你好`       |
| `trans_en`    | **[Target 2]** English translation.                                 | `Hello`      |
| `trans_ja`    | **[Target 3]** Japanese translation.                                | `こんにちは` |
| `trans_es`    | **[Target 4]** Spanish translation.                                 | `Hola`       |
| `trans_ru`    | **[Target 5]** Russian translation.                                 | `Привет`     |
| `trans_...`   | **[Target N]** Other languages depend on config (e.g., `trans_id`). | `...`        |
| `status`      | **[Workflow]** `TODO` or `reviewed`.                                | `reviewed`   |

> **Note**: The `trans_{lang}` columns are dynamic! They change based on the Source Language and `tools/v5/utils/constants.py`. The table above is just an example for Korean Source.
> **注意**：`trans_{lang}` 欄位是動態的！它們會根據來源語言與 `constants.py` 改變。上表僅為韓語來源的範例。

## 3. Formatting Rules (格式規範) ⚠️

為了確保 CSV 解析穩定（特別是譯文中包含逗號時），本階段**所有** CSV 檔案必須嚴格遵守以下格式：
To ensure stable CSV parsing (especially when translations contain commas), **ALL** CSV files in this phase must strictly follow these rules:

1. **Strict Double Quoting**: **所有**欄位（包含 Header）必須使用雙引號引導。
    - **ALL** fields (including Header) MUST be wrapped in double quotes (`"field"`).
2. **Encoding**: UTF-8 without BOM (or UTF-8-sig if strictly required by tool).
3. **No Trailing Spaces**: 移除欄位前後的多餘空格。

---

## 4. Workflow (工作流)

### 1. Update Database (同步)

先執行同步以確保 CSV 存在且格式正確。
Run sync first to ensure CSVs exist and are formatted correctly.

```bash
python -m tools.v5.core.update_db {lang}
```

> [!CAUTION] > **STRICT BAN ON BATCH SCRIPTS (嚴禁批次腳本)**
>
> - You remain strictly FORBIDDEN from using `batch_translate` or `llm_client` loops to fill content.
> - **Reason**: Local LLMs produce "Garbage In".
> - **Action**: If you see `[TODO]`, YOU (The Agent) must write/translate it manually in the CSV using `multi_replace`.
> - **Sequence**: Process one column (one language) at a time.

### 2. Validation (初檢)

使用驗證腳本檢查是否有明顯錯誤（如缺失標頭、空翻譯、報價格式錯誤）。
Use validation script to check for obvious errors (missing headers, empty translations, quoting issues).

```bash
python -m tools.v5.1_translation.validation {lang}
```

### 3. Audit & Repair (審查與修復)

如果驗證失敗或需要人工校對 (Manual Audit)：

### Step 0: Setup Audit Report (建立報告與佇列)

- **Mandatory (必讀)**: You MUST read the [Audit Report Template](./audit_report_template.md) and refer to the [Golden Sample](../../golden_samples/audit_report_ko_p1.md).
- **Rule**: Before checking ANY file, you MUST create/populate `audit_report_{lang}_p1.md`.
- **Status**: Mark all as `⚪ Pending`.
- **Reason**: To ensure formatting consistency and prevent skipping files.

### Step 1: Sequential Verification (逐一驗證)

- **Process**: Pick the first `Pending` file from the top.
- **Action**:
  1. `view_file {file}.csv`
  2. **Semantic Check**: Compare Source vs Target (Context, Tone, Accuracy).
  3. **Evidence**: You MUST quote the specific text you verified in the chat.
     - ✅ "Verified: Source 'Apple' matches Target 'Fuji' (Row 5)."
- **GATE (Sequential Review)**: After translating/verifying a SINGLE language (column), you MUST call `notify_user` for approval before moving to the next language.

### 🏆 Golden Sample: Semantic Verification (黃金範例)

Below is the **Minimum Standard** of verification evidence. You MUST verify ALL columns.

> **File**: `ko_l1_culture_005_hanok` (ID/Korean Check)
>
> **Row 2 ("Hanok is trad house")**
>
> - **Src**: `한옥은 한국의 전통 집이다.`
> - **EN**: `Hanok is a traditional Korean house.` ✅
> - **ZH**: `韓屋是韓國的傳統房屋。` ✅
> - **JA**: `韓屋は韓国の伝統的な家です。` ✅
> - **ES**: `Hanok es una casa tradicional coreana.` ✅
> - **RU**: `Ханок — традиционный корейский дом.` ✅
> - **ID**: `Hanok adalah rumah tradisional Korea.` ✅
>
> **Row 3 ("Wood and Earth")**
>
> - **Src**: `나무와 흙으로 만든다.`
> - **EN**: `It is made of wood and earth.` ✅
> - **ZH**: `用木頭和泥土建造。` ✅
> - **ID**: `Terbuat dari kayu dan tanah.` ✅
>
> _(...continue for all rows)_

### Step 2: Update Table (更新狀態)

- Mark as 🟢 (Pass) or 🔴 (Fail).
- If 🔴 Fail -> **Stop & Repair immediately** -> Re-verify -> Mark 🟢.

1. **Repair Content**:
    - 直接修改 CSV 檔案。
    - **CAUTION**: 手動編輯後，請確保維持「全欄位雙引號」格式。建議使用確定性工具修復引號。
    - 修正後，務必重新執行 Step 2 驗證。

### 4. Final Gate (終檢)

必须看到 `✅✅ PASSED` 才能進入下一階段。
Must see `✅✅ PASSED` to proceed.

---

## 5. Article Segmentation Rules (文章分段規則)

For Article content (`0_writer/article/*.md`), the CSV generation follows specific granularity rules:

1. **Granularity**: **Sentence Level** (句子層級).
    - Each CSV row represents one sentence.
    - **NOT** Paragraph level.
2. **Paragraph IDs**:
    - The `speaker` column is used to store Paragraph IDs (`P1`, `P2`, `P3`...).
    - Example: `P1` = First Paragraph, `P2` = Second Paragraph.
3. **Type**:
    - `type` column MUST be `sentence`.

## 📚 Linguistic Standards (語言標準)

各語言的具體審查標準（敬語、語法、常見錯誤）請參閱以下專家工作流：
Refer to the expert workflows below for specific language standards (honorifics, grammar, common errors):

- **Korean (KO)**: [Audit Korean SOP](../../linguistics/audit_ko_content.md)
- **Thai (TH)**: [Audit Thai SOP](../../linguistics/audit_th_content.md)
- **German (DE)**: [Audit German SOP](../../linguistics/audit_de_content.md)

- **詳細規格**：參閱 `technical/universal/engineering/chunk_spec.md`
- **目標檔案**：`lingostory_universal/content/1_translation/{lang}/chunks_source.csv`

如果遇到成語（Idiomatic Expression）或高頻詞塊（Chunks）：

1. **保持翻譯自然**：在主 CSV 的 `trans_{lang}` 欄位正常翻譯完整句子。
2. **收錄原則 (Selection Principles)**：
    - **非單字原則 (Multi-word Only)**：嚴格排除單一單字，單字由 Phase 4 Dictionary 處理。
    - **ID 命名規範**：必須遵循 `{lang}_chunk_{sub_type}_{lemma}` 格式（如 `th_chunk_idm_jai_dee`）。
3. **登錄格式**：將短語原文、詞性、各語種翻譯與標籤加入 `chunks_source.csv`。
    - 確保所有欄位執行 **Strict Double Quoting**。
4. **Sync**: 此文件是 Phase 4 `chunks.csv` 的 **Source of Truth**。

## 6. Handover (交接與門禁) ⚠️

在宣佈 Phase 1 完成前，Agent 必須確保：

1. **Configuration Check (配置檢查)**:
    - 檢查 `tools/v5/utils/constants.py` 中的 `BIG5_LANGUAGES` 或 `SUPPORTED_LANGUAGES` 是否已包含本階段所有新增的語系欄位。
    - **警告**: 若未註冊即進入 Phase 2，所有手動填寫的內容將被 `update_db.py` 永久刪除！
2. **Sign-off Artifact**:
    - 在根目錄建立 `verified_p1.txt`。
    - 內容必須包含對「全引號格式」、「印尼語對齊」與「配置註冊」的明確確認。
3. **No Sign-off, No Phase 2**: 禁止在缺少此文件的狀況下啟動任何 Phase 2 自動化腳本。

---

- **Next Step**: 完成後，請閱讀 [Phase 2 Atoms SOP](../2_atoms/2_atoms_sop.md)。
