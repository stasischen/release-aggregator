# Data Model & Schema Contracts (V5)

本文件定義了 Lingo V5 跨倉庫的資料結構契約，特別是字典與語法資料的 Core/I18n 分離體系。

## 1. 字典契約 (Dictionary Contract)

- **Core (核心語言資料)**:
    - 存儲於 `content/source/<lang>/core/dictionary/atoms/*.json`。
    - 定義穩定的 `atom_id`。
    - 包含詞性 (POS)、原形 (Lemma)、形態變化 (Surface Forms)。
- **I18n (教學與翻譯資料)**:
    - 存儲於 `content/source/<lang>/i18n/<learner_lang>/dictionary/*.json`。
    - 包含翻譯、教學註解。
    - 透過 `atom_id` 關聯核心資料。

## 2. 語法契約 (Grammar Contract)

- **Core**: 定義目標語言中的句型模式與範例。
- **I18n**: 定義學習者語言中的標題、解釋與教學邏輯。

## 3. ID 與檔案命名規範

- **Canonical IDs**: `atom_id` 與 `grammar_id` 是系統內部的唯一真理。
- **Filesystem Mapping (`fs_safe_id`)**:
    - 用於處理作業系統對特殊字元（如冒號 `:`）的限制。
    - 格式：使用雙底線 `__` 作為分隔符（例如 `ko__n-friend__01`）。
    - **禁止**: 不得將 `fs_safe_id` 用於任何業務邏輯或資料庫 lookup。

## 4. 目錄結構規範
所有 `content-<lang>` 倉庫應遵循以下路徑：
- `content/source/<lang>/core/dictionary/atoms/*.json`
- `content/source/<lang>/i18n/<learner_lang>/dictionary/*.json`
- `content/source/<lang>/core/grammar/*.json`
- `content/source/<lang>/i18n/<learner_lang>/grammar/*.json`

---
**備註**: 本文件為 Lingo 系統的「法律條文」，任何變更必須先更新 `core-schema` 倉庫。
