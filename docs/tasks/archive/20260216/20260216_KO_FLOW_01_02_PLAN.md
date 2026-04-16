# KO-FLOW-01 + KO-FLOW-02 Implementation Plan

> **建立日期**: 2026-02-16
> **目的**: 記錄設計原因，讓未來的 Agent 和開發者可以理解為什麼這樣做。

## Goal

Lock canonical ID format and define staging data model — the two foundational tasks that all downstream mapping/dictionary work depends on.

> 鎖定 ID 格式與定義中間資料模型。這兩件事是所有後續 Mapping 和字典工作的根基，如果不先固定，後面做的東西都有可能要重做。

---

## KO-FLOW-01: Freeze ID/Path Policy (`core-schema`)

### [MODIFY] dictionary_core.schema.json / dictionary_i18n.schema.json

> **為什麼？** 目前的 `atom_id` regex 同時接受舊格式 (`ko_N_friend`) 和新格式 (`ko:n:친구`)。這導致兩種格式共存，下游工具無法預期 ID 長什麼樣子。收緊 regex 到只接受冒號格式，從 schema 層面強制統一。

### [MODIFY] atom.schema.json

> **為什麼？** `atom.schema` 是前端 lesson 資料的基礎單位。目前的 `id` pattern 同時允許 `:` 和 `__`，但根據政策只有 `:` 是 canonical，`__` 只能出現在 `fs_safe_id`。從 schema 層面區分這兩者。

### [MODIFY] examples (dictionary_core, dictionary_i18n, grammar_core)

> **為什麼？** 現有範例用的是 `ko:hello:01`，但實際 `mapping.json` 裡用的是 `ko:n:안녕` (POS-based)。範例應該反映真實用法，否則照著範例寫會產出不一致的資料。

### [NEW] ID_POLICY.md

> **為什麼？** 目前 ID 規範散落在兩處文件，而且只是簡短提及。需要一份獨立的政策文件，讓所有 Repo 有唯一的參考來源。

---

## KO-FLOW-02: Define Staging Data Model (`content-ko`)

### [NEW] data/staging/README.md

> **為什麼？** `data/staging/` 裡的檔案沒有文件說明。README 明確定義三種 staging 檔案的角色：候選、已確認、衝突。

### [NEW] staging schemas (token_candidates, mapping_accepted, mapping_conflicts)

> **為什麼？**
> - **token_candidates**: 確保每個候選 token 都帶有來源追蹤和上下文
> - **mapping_accepted**: 「已確認的映射」格式統一，下游字典生成器可以放心消費
> - **mapping_conflicts**: 低置信度的映射不應該被丟掉也不應該靜默接受，放入 conflicts 可追蹤每個未解決的歧義
