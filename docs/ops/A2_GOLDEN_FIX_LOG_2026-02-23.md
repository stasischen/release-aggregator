# A2 Gold Standard Audit & Fix Report (2026-02-23)

## 1. 核心問題摘要 (Executive Summary)

在審核 `content/gold_standards/dialogue/A2/` 下的對話金標檔案時，發現大量不符合 **V5 Data Standardization Protocol** 的標記。這些問題主要集中在詞性 (POS) 誤植、Unicode 字符不統一、以及原子分解不完全。

當前 Pipeline 報錯數：**1215 Errors**。

## 2. 識別出的主要問題模式 (Identified Patterns)

### A. 嚴重詞性標記錯誤 (Major POS Mismatch)
| 模式 | 當前標記 (Wrong) | 修正標記 (Target) | 理由 |
| :--- | :--- | :--- | :--- |
| `있다` | `ko:v:있다` | `ko:adj:있다` | V5 協議：存在/擁有為形容詞 |
| `없다` | `ko:v:없다` | `ko:adj:없다` | V5 協議：不存在為形容詞 |
| `아니다` | `ko:v:아니다` | `ko:adj:아니다` | V5 協議：否定為形容詞 |
| `어때요` | `ko:adj:어떻다+ko:e:었+ko:e:어요` | `ko:adj:어떻다+ko:e:어요` | 時制錯誤：現在式不應含 `었` |
| `해요` | `ko:v:하다+ko:e:었+ko:e:어요` | `ko:v:하다+ko:e:어요` | 時制錯誤：現在式被標為過去式 |
| `오늘/어제/내일` | `ko:adv:*` | `ko:n:*` | 字典一致性：當前標註為名詞 (N) |

### B. Unicode 兼容字符問題 (Character Normalization)
大量詞尾使用的 `ㄹ` 字符為 Unicode Compatibility Jamo (U+1105 `ᄅ`)，而非標準諺文字母 (U+3139 `ㄹ`)。
- **原因**: 導致 Pipeline 找不到字典中收錄的 `ko:e:ㄹ` (U+3139)。
- **修正**: 將所有 `gold_final_atom_id` 中的 `\u1105` 替換為 `\u3139`。

### C. 原子化分解爭議 (Decomposition Decisions)
- **-ㄹ게요**: A1 與當前字典傾向於單一原子 `ko:e:ㄹ게요`。
  - **初次嘗試**: 拆分為 `ko:e:ㄹ+ko:e:게요`。
  - **修正後**: 改回 `ko:e:ㄹ게요` 以符合現有 A1 數據與字典存量。
- **複合名詞/助詞**:
  - `ko:n:식당이요` -> `ko:n:식당+ko:p:이+ko:p:요` (必須拆分)
  - `ko:n:때마다` -> `ko:n:때+ko:p:마다` (必須拆分)

## 3. 實施記錄 (Implementation Log)

### Batch 01 (2026-02-23)
- **修正範圍**: 全量 A2-01 至 A2-25。
- **重點**:
  - U+1105 轉 U+3139。
  - `있다/없다/아니다` POS 修正。
  - `어때요/해요` 時制過度修正回歸。
  - `식당이요`, `때마다` 二階分解。
- **結果**: 錯誤數從 1215 降至 1151。

### Batch 02 (2026-02-23)
- **修正範圍**: 全量 A2-01 至 A2-25。
- **重點**:
  - `오늘/어제/내일` POS 從 `adv` 統一修正為 `n`。
  - `왜` POS 從 `pron` 修正為 `adv`。
  - 回退 `-ㄹ게요` 分解，維持 `ko:e:ㄹ게요`。
  - `으시` 規格化為 `시`。
- **結果**: 錯誤數從 1151 降至 **1098**。剩餘錯誤均為字典實體缺失。

## 4. 識別出的字典缺失 (Dictionary Gaps)

以下原子在 A2 金標中頻繁出現，但當前字典 `content/core/dictionary/atoms/` 中並未收錄，需後續補齊：

### A. 動詞/形容詞 (V/ADJ)
- `ko:v:조심하다`
- `ko:adj:까다롭다`
- `ko:v:긴장되다`
- `ko:adj:힘들다` (注意：部分檔案標記為 `ko:adj:힘들`)
- `ko:v:설거지하다`

### B. 名詞 (N)
- `ko:n:엄마`, `ko:n:식당`, `ko:n:학기`, `ko:n:교수님`, `ko:n:풋살`, `ko:n:문명`, `ko:n:역사`
- `ko:n:먹기` (動名詞)

### C. 專有名詞 (PROP)
- `ko:prop:준호`, `ko:prop:스미스`, `ko:prop:태국`, `ko:prop:마야`

---
*Status: Initial Audit Complete. Ready to execute surgery.*
