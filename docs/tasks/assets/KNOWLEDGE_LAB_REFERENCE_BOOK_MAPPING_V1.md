# Knowledge Lab Reference Book Mapping V1

## 1. Mapping Grammar Items (Beginner / Endings)

Source: `reports/youtube_beginner_grammar/clean_md/*.md`
Source: `reports/youtube_connective_endings/clean_md/*.md`

| Source Field | Target Bank | Knowledge Item Field | Role |
| :--- | :--- | :--- | :--- |
| **# Title** | N/A | `id` (Slug) | Identifying Key |
| **Description** | N/A | `summary_zh_tw` | High-level goal |
| **Usage Rules** | N/A | `explanation_md_zh_tw` | Core Markdown content |
| **Examples (KO/ZH)** | `example_sentence` bank | `example_sentence_refs` | **Canonical** reusable examples |
| **Draft Examples** | `example_bank` | N/A | **Transitional** / Migration source |

## 2. Transition Plan (From Migration to Canonical)

目前的作者流程與自動化導入（如 `kg-mig-010`）應區分「來源」與「終點」：

1.  **Migration Source (`example_bank`)**: 
    - 舊有的 JSON 或 CSV 數據若帶有行內例句，應先暫存於 `example_bank`。
    - 這是 **過渡性質** 的存儲，不應作為長期維護對象。
2.  **Canonical Destination (`example_sentence` bank)**:
    - 具備重複利用價值、結構完整的例句，應提取至 `content-ko/content/core/learning_library/example_sentence/`。
    - 提取後，Knowledge Item 中應使用 `example_sentence_refs` 進行引用。

## 3. Mapping Survival Patterns

Source: `ko_survival_pattern_library_v1.json`

| Source Field | Core ID / Ref | I18n Field | Note |
| :--- | :--- | :--- | :--- |
| **`pattern_id`** | `id` | N/A | Normalized semantic slug |
| **`frame`** | `frame` | N/A | The visual pattern frame |
| **`examples`** | `example_sentence_refs` | N/A | Link to global sentence bank |

## 4. Normalization Rules

1.  **Strict Contract**: 禁止在 JSON 頂層發明自訂 metadata 欄位。
2.  **Semantic Slugs**: 使用具備語義的名稱（如 `copula_polites`）而非無序編號。
3.  **Markdown Validation**: 確保匯入的 `explanation_md_zh_tw` 符合 [Markdown Profile](../guides/KNOWLEDGE_LAB_MARKDOWN_PROFILE_V1.md)。
4.  **No Direct Example Text**: 最終狀態下，Knowledge Item JSON 不應直接包含 `surface_ko` 例句文字，應全數透過 `example_sentence_refs` 引用。
