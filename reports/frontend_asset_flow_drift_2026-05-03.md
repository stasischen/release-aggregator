# Frontend Asset Flow Drift Scan (2026-05-03)

本報告整理 `release-aggregator`、`content-pipeline`、`content-ko` 與 `lingo-frontend-web` 之間關於 Frontend Asset 產生、同步與驗證的文件與指令漂移狀況。

## 1. 目前有哪些 command 可以產出或同步 frontend assets？

### `content-ko/Makefile`
*   `make export-frontend-grammar`: 透過 `scripts/ops/export_frontend_grammar.py`，直接將 grammar JSON 與 index 寫入 `../lingo-frontend-web/assets/content/grammar`。

### `content-pipeline/Makefile`
*   `make sync-video-frontend`: 透過 `scripts/sync_video_to_frontend.py`，直接將 core/i18n 的影片 JSON 複製並更新到 `../lingo-frontend-web/assets/content/production/packages/ko/video/`，同時覆寫 frontend 端的 manifests。
*   `make export-learning-library`: 輸出 learning library 至 `dist/ko`。
*   `make export-frontend-intake`: 透過 `scripts/handoff/export_frontend_intake.py` 封裝 frontend intake package 至 `release-aggregator/staging/frontend_intake`。

### `lingo-frontend-web/Makefile`
*   `make sync-video`: 本質上呼叫 `../content-pipeline/scripts/sync_video_to_frontend.py`，屬重複封裝。
*   `make sync-library`: 透過 `scripts/sync_learning_library.sh`，直接從 `../content-pipeline/dist` 拉取資料至 `assets/artifacts/learning_library`。
*   `make validate-assets`: 執行 `flutter test test/core/asset_integrity_test.dart` 驗證資產。

---

## 2. 哪些 command 是舊的、重複的、或會產生錯誤路徑？

**反模式 / 錯誤路徑：**
*   **跨 Repo 越權寫入（Bypass PRG）：** `content-ko` 的 `export-frontend-grammar` 與 `content-pipeline` 的 `sync-video-frontend` 直接修改 `lingo-frontend-web` 目錄，這會造成 git state 髒污，並且繞過了 `release-aggregator` 的 Production Release Gating (PRG) 稽核，這是嚴重的架構反模式。
*   **前端主動拉取（Pull instead of Intake）：** `lingo-frontend-web` 的 `sync-library` 與 `sync-video` 依賴上游的相對路徑與狀態。前端應該是「被動接收」發版產物，而非主動去建置管線撈取檔案。

**重複的指令：**
*   `lingo-frontend-web` 的 `sync-video` 和 `content-pipeline` 的 `sync-video-frontend` 執行完全相同的腳本。

---

## 3. 哪些 docs 還在描述舊流程？

*   `release-aggregator/docs/human-handbook/stages/S5_frontend_intake.md`
    *   **描述漂移：** 文件提到 `cd ../lingo-frontend-web` 然後執行 `npm run test:content` 來 sync/copy staged assets。這反映了舊的 pull 流程，與目前 PRG 設計（應由 PRG 決定 production bundles 並單向推送給 Frontend）有出入。

---

## 4. 哪個 repo 應該擁有哪個階段？

基於 PRG 產物地圖 (`08_PRG_ARTIFACT_MAP.md`)：

1.  **`content-ko` (Domain Source):** 擁有原始文本、字典、文法結構等。只負責輸出給 pipeline。
2.  **`content-pipeline` (Packaging):** 負責將原始內容封裝為結構化產物，並統一輸出至 `dist/` 或產生 Phase 1 staging `global_manifest.json`，**不該直接碰前端路徑**。
3.  **`release-aggregator` (Assembly & PRG):** 真正的發版中心。擁有 Phase 2 審核（release manifest），負責吃進 `dist/` 的資料，組裝成最終的 Production bundles (lesson catalog, manifests, final JSONs) 並部署。
4.  **`lingo-frontend-web` (Intake & Runtime):** 屬於純粹的消費者。只負責驗證收到的 bundles (`validate-assets`) 與展示。

---

## 5. 建議保留的一條 canonical flow 是什麼？

標準且唯一的資產產生與發佈流水線應為：

`content-pipeline/dist` (Raw Built Artifacts)
➡️ `release-aggregator` Phase 1 (`global_manifest.json` - Staging Index)
➡️ `release-aggregator` Phase 2 PRG Assembler (依據 Release Manifest 過濾與打包)
➡️ 產出最終的 `production_plan.json`、`lesson_catalog.json`、`manifest.json` 與 Production Bundles
➡️ **單向複製 (Deploy)** 至 `lingo-frontend-web/assets/content/production/`
➡️ `lingo-frontend-web` 執行 `make validate-assets` 確保完整性。

---

## 6. Codex-ready 修改清單 (Sorted by Priority)

**P0 (架構違規與嚴重繞徑修復)**
*   **檔案：** `content-ko/scripts/ops/export_frontend_grammar.py`
    *   **原因：** 嚴重違反隔離原則。
    *   **修改：** 將 `--frontend-repo` 參數移除，預設輸出到 `content-ko/artifacts/` 或由 pipeline 統一代收，交給 aggregator 打包。
*   **檔案：** `content-pipeline/scripts/sync_video_to_frontend.py`
    *   **原因：** 嚴重違反隔離原則，繞過 PRG 的發版流程。
    *   **修改：** 應改為輸出 staging pkg 至 pipeline 自己的 `dist/`，讓 aggregator PRG 去抓，而非直接寫入 `lingo-frontend-web/assets/`。

**P1 (前端職責釐清與文件更新)**
*   **檔案：** `lingo-frontend-web/Makefile` & `lingo-frontend-web/scripts/sync_learning_library.sh`
    *   **原因：** 前端不應該包含 pull script (`sync-video`, `sync-library`)。
    *   **修改：** 移除這些跨 repo 拉檔案的 scripts，前端的 Makefile 應只保留 `validate-assets` 與測試。
*   **檔案：** `release-aggregator/docs/human-handbook/stages/S5_frontend_intake.md`
    *   **原因：** 描述過時，仍記載手動 pull。
    *   **修改：** 更新為 PRG push model，說明由 PRG output 匯入前端 `assets/content/production/` 後，直接跑 `validate-assets` 即可。

**P2 (清理無用指標)**
*   **檔案：** `content-pipeline/Makefile`
    *   **原因：** 移除依賴越權 script 的 Makefile target。
    *   **修改：** 刪除 `sync-video-frontend` rule。
