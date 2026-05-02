# PRG 產物地圖
# PRG Artifact Map

本頁說明 Production Release Gating（PRG）相關檔案各自的角色。  
This page explains the role of each file in the Production Release Gating (PRG) flow.

## 一句話總結

- `release manifest` 決定哪些課可以發版
- `global_manifest.json` 是 Phase 1 staging 的 provenance index
- `staging candidate` 提供可建置、可驗證的候選內容，但 production mode 必須透過 `global_manifest.json` 進入 PRG
- `production artifacts` 是最後真正發出去的產物
- `mockup viewer` 只是 UI / runtime 測試資料，不是發版決策來源

## 主要產物

| 產物 | 常見路徑 | 作用 | 是否為真實決策來源 |
|---|---|---|---|
| Release Manifest | `staging/production_release_gating/prd.release_manifest.json` 或 `staging/prg_pilot/pilot_allowlist.json` | 這是發版 allowlist。只有被列入的 `lesson / unit` 才能進 production。 | 是 |
| Phase 1 Staging Index | `release-aggregator/staging/<version>/global_manifest.json` | Phase 1 release output 的權威索引。包含 artifact path、hash、source commit、pipeline/schema provenance。 | 是，作為 staging provenance source |
| Staging Candidate Inventory | Phase 1 staging output derived from `global_manifest.json` | staging 端候選內容池。用來建置、驗證、對照，不負責決定能不能發版。 | 否 |
| Production `manifest.json` | 目前：`staging/prototype_output/manifest.json`；未來目標：`lingo-frontend-web/assets/content/production/manifest.json` | production 端實際讀取的資產清單。它是產物，不是決策來源。 | 否，屬於輸出 |
| Production `lesson_catalog.json` | 目前：`staging/prototype_output/lesson_catalog.json`；未來目標：`lingo-frontend-web/assets/content/production/lesson_catalog.json` | production 端的課程中繼資料。包含單元、排序、標題、標籤等資訊。 | 否，屬於輸出 |
| Production plan | `staging/prototype_output/production_plan.json` | PRG prototype 目前的第三個輸出。記錄 gaps、allowlisted lessons、packaged artifact hash/provenance。 | 否，屬於審核輸出 |
| Production bundles | 未來目標：`lingo-frontend-web/assets/content/production/packages/ko/**` | 實際被打包到 production 的 lesson JSON 與相關資產。PRG prototype 尚未輸出 bundles。 | 否，屬於未來輸出 |
| Viewer mockup data | `tools/modular-viewer/**`、`docs/tasks/mockups/**` | UI / runtime 測試與模擬資料。可用於驗證 viewer 行為，但不決定發版資格。 | 否 |

## 每個檔案在做什麼

### 1. Release Manifest

Release Manifest 是唯一回答「這一課能不能發版」的檔案。

常見欄位：

- `unit_id`
- `lesson_id`
- `release_status`
- `content_type`
- `course_type`
- `source_refs`
- `contract_version`
- `viewer_verified`
- `qa_gate_passed`
- `staging_only`
- `notes`

它回答的是：

- 哪些課可以進 production？
- 哪些只能留在 staging？
- 這筆資料有沒有通過 QA 與 viewer 驗證？

參考：

- [PRG_001_RELEASE_MANIFEST_SCHEMA.md](../tasks/assets/PRG_001_RELEASE_MANIFEST_SCHEMA.md)

### 2. Staging Candidate Inventory

這是 staging 端的候選內容池。production mode 下，PRG 不直接掃 raw directory；它從 Phase 1 `global_manifest.json` 建立 candidate inventory。

它可能包含：

- dialogue
- video
- article
- 其他還沒進 production 的內容類型

它回答的是：

- 內容能不能建置？
- 內容是否已在磁碟上？
- 內容是否符合 staging / candidate 的結構？

參考：

- [PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md](../tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md)

### 3. Production `manifest.json`

這是**輸出產物**，不是決策來源。

production 端的 `manifest.json` 會被 app / frontend bundle 在 runtime 讀取，用來知道哪些資產被發佈。

它回答的是：

- 這次發了哪些 asset？
- 這些 lesson JSON 的路徑是什麼？

它應該由 Release Manifest 推導出來，而不是人工直接改。

參考：

- [PRG_003_MANIFEST_MIGRATION_PATH.md](../tasks/assets/PRG_003_MANIFEST_MIGRATION_PATH.md)

### 4. Production `lesson_catalog.json`

這也是**輸出產物**。

它包含已發佈課程的教學結構與中繼資料，例如：

- 單元排序
- 課程排序
- 標題
- 標籤
- 顯示用 metadata

它回答的是：

- 這些課要怎麼組織？
- 前端要顯示哪些 metadata？

參考：

- [PRG_003_MANIFEST_MIGRATION_PATH.md](../tasks/assets/PRG_003_MANIFEST_MIGRATION_PATH.md)

### 5. Production bundles

這是未來實際被包進 production 的 lesson JSON 和相關資產。當前 PRG prototype 先產出 `production_plan.json` 作為審核與 provenance trace，不直接輸出 bundles。

它回答的是：

- 這次到底發了哪些 lesson JSON？
- 這些 lesson 帶了哪些配套資產？

參考：

- [PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md](../tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md)

### 6. Viewer mockup data

這些檔案是給開發、QA、UI 模擬用的。

常見位置：

- `tools/modular-viewer/data/**`
- `docs/tasks/mockups/**`

用途包括：

- 驗證 viewer render
- 測試 UI 行為
- 重現 runtime 狀態

它們不是 release decision 的來源。

參考：

- [UNIFIED_LESSON_VIEW_ARCHITECTURE.md](../tasks/assets/UNIFIED_LESSON_VIEW_ARCHITECTURE.md)

## 課是什麼

在這條 PRG 線裡，這裡的「課」是指 **lesson / unit blueprint**。

更精確地說：

- `unit_id` 表示較大的教學單元
- `lesson_id` 表示單元中的具體課
- lesson / unit blueprint 定義整體教學包長什麼樣
- `dialogue`、`video`、`article`、`grammar-heavy` 則是可以放進這個 blueprint 的內容型別

所以：

- `dialogue` 檔不等於一課
- `video` 檔不等於一課
- `article` 檔不等於一課
- 課是把這些素材組合起來的教學單位

### 白話模型

- `blueprint` = 這一課怎麼設計
- `content_type` = 這一課裡面的素材類型
- `release manifest` = 哪些 blueprint 可以發
- `production artifacts` = 最終打包出來的結果

例如：

- `bonus_video` 單元可能包含一個或多個 video lessons
- dialogue 型單元可能包含多條對話與輔助 metadata
- article 型單元可能包含文章正文與關聯字彙 / review 資料

關鍵原則是：

- release gate 綁在 **lesson / unit blueprint**
- 不是綁在單一 raw source file

## 流程總覽

```text
content-pipeline/dist
  -> Phase 1 release.py staging
  -> global_manifest.json
  -> Phase 2 release manifest + candidate inventory derived from global_manifest.json
  -> PRG prototype assembler
  -> manifest.json / lesson_catalog.json / production_plan.json
  -> future production bundles
```

`viewer mockup data` 是旁路的測試資料，不在 release decision 主鏈上。

## 實務判斷

- 如果一個檔案回答的是「能不能發」，它屬於 release manifest 層
- 如果一個檔案回答的是「staging 裡有什麼」，它屬於 staging candidate 層
- 如果一個檔案回答的是「最後 app 會拿到什麼」，它屬於 production artifacts 層
- 如果一個檔案回答的是「UI 測試時要長什麼樣」，它屬於 mockup / viewer data 層
