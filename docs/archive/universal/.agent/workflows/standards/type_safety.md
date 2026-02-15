---
description: Type Safety & Data Contract Guidelines
---

# Type Safety & Data Contract Guidelines

## Core High-Level Rule
**"No Garbage In, No Hidden Garbage Out"**

當處理 Content Atoms 或 Dictionary Entries 時，agent 絕對不能偽造分類資料以繞過驗證門檻。

## Rules

1.  **Strict POS Classification**
    -   不要將 `_WORD_` 或 `_UNK_` 原子轉換為通用類型（如 `_E_` 或 `_N_`），除非經過語言驗證。
    -   驗證必須來自：
        -   **Deterministic Lookup**: 一個硬編碼的已知詞彙映射表（例如 `DE_POS_MAP`）。
        -   **Morphological Analysis**: 像 `kiwipiepy`、`spacy` 或 `mecab` 這樣的函式庫來決定標籤（例如 `VV` -> `V`）。
        -   **User Confirmation**: 顯式的使用者輸入。
    -   如果驗證失敗，請將原子保持為 `_WORD_` 或 `_UNK_`，並讓建置失敗。不要忽略錯誤。

2.  **ID Immutability**
    -   一旦 Atom ID（例如 `ko_V_가다`）在字典中建立，它就是真理之源。
    -   不要透過更改字典 ID 來「修復」內容以符合錯誤的資料（例如，不要將 `ko_E_...` 改為 `ko_N_...`，即使內容使用了 N）。應修復內容以符合字典。

3.  **Gatekeeper Integrity**
    -   驗證門檻（如 `_check_dictionary_mapping_integrity`）的存在是為了阻止不良資料進入。
    -   除非使用者明確指示用於除錯建置，否則不得關閉、放寬或繞過這些門檻。
    -   如果門檻失敗，請修復 **資料**，而不是 **門檻**。

## Workflow for Missing Types

如果你遇到 `_WORD_` 或 `_UNK_` 錯誤：

1.  **Analyze**: 識別詞彙（例如 `Bier`, `trinken`）。
2.  **Map**: 建立映射策略（例如「Bier 是名詞」）。
3.  **Repair**: 執行腳本，將此映射應用於重新命名內容 CSV 中的 Atoms。
4.  **Sync**: 執行 `sync` 將有效的 Atoms 推送到字典中。