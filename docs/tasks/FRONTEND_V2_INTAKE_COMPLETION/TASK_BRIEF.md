# Task Brief

## Metadata

- Task ID: FRONTEND_V2_INTAKE_COMPLETION
- Owner: release-aggregator control tower
- Target repo: `lingo-frontend-web`, `release-aggregator`, `content-ko`
- Status: in_progress
- DeepSeek routing: flash -> pro
- Created: 2026-05-03
- Last updated: 2026-05-03

## Model Routing

- DeepSeek: flash -> pro
- Reason: Use `flash` for first-pass inventory across frontend loaders, production assets, and v2 inventory files. Escalate to `pro` before accepting any data-flow, schema, release-path, or adapter-boundary decision.
- Escalation trigger: Any conclusion that changes frontend runtime loading, production artifact layout, dictionary contract, PRG promotion behavior, or release validation gates.

## 目標

把 Lingourmet frontend 的 study runtime、dictionary runtime、以及 UI 顯示資料來源收斂到 `content_v2` 衍生的穩定 contract。

完成後，前端不應在 UI/repository 任意硬組 `assets/content/production/packages/...` 實體路徑；study、dictionary、grammar、learning-library 相關 UI 應透過明確 adapter / manifest resolver 讀取 v2-derived production artifacts，並有真實 Korean v2 fixture 的驗收測試。

## 背景

目前 `content-ko/content_v2` 已經是內容 source truth，但 frontend runtime 仍有多處 legacy package layout coupling：

- Study runtime 直接用 `StudyContentLocator` 組 `assets/content/production/packages/{lang}/...`。
- Lesson registry 混用 `assets/content/production/manifest.json`、`packages/ko/lessons/modular_lessons.json`、以及硬編 `lesson_content.v1.json`。
- Dictionary runtime 仍吃 packaged `dictionary_core.json`、`dict_ko_zh_tw.json`、`Strings_zh_tw.json`、`mapping_v2.json`，尚未形成單一 v2 dictionary adapter contract。
- 現有 content validation test 使用 mock Thai data，不能證明 real Korean v2-derived production assets 可被前端 UI 正確載入與顯示。
- PRG / release aggregation 已有 `global_manifest.json` provenance path，但 production bundle promotion、frontend contract test、asset bundle output 還沒有完全封口。

## 相關檔案

- `lingo-frontend-web/lib/features/study/data/repositories/study_content_locator.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/lesson_registry_repository.dart`
- `lingo-frontend-web/lib/features/study/data/repositories/event_repository.dart`
- `lingo-frontend-web/lib/core/services/config_loader.dart`
- `lingo-frontend-web/lib/core/services/i18n_overlay_service.dart`
- `lingo-frontend-web/lib/core/repositories/dictionary_repository.dart`
- `lingo-frontend-web/lib/core/services/grammar_note_service.dart`
- `lingo-frontend-web/test/content/content_validation_test.dart`
- `lingo-frontend-web/assets/content/production/manifest.json`
- `lingo-frontend-web/assets/content/production/packages/ko/manifest.json`
- `content-ko/content_v2/`
- `release-aggregator/scripts/prg/assembler_prototype.py`
- `release-aggregator/tests/test_prg_frontend_contract.py`
- `release-aggregator/docs/review/2026-05-02_PRG_DRIFT_INVENTORY.md`
- `release-aggregator/docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md`

## 已知限制

- 不要把 UI redesign、Stitch mockup、或 visual token work 混進本任務。
- 不要一次性重構整個 frontend study feature；先定 contract boundary，再做窄範圍 replacement。
- 不要直接把 `content-ko/content_v2` raw inventory path 當成 Flutter runtime path；frontend 應吃 release/promotion 後的 stable artifact。
- 不要破壞現有 video、grammar note、dictionary overlay、learning-library 的可用 fallback。
- 不要改 public API，除非 GPT 5.5 已接受 adapter boundary 方案。
- 每次 implementation slice 必須跑 targeted Flutter tests 或記錄無法測試原因。

## 建議方案

### A

- 做法：建立 `FrontendContentContractResolver` / `V2ContentAdapter`，集中解析 `manifest.json`、lesson catalog、dictionary manifest、grammar index、learning-library index，逐步讓 study/dictionary repositories 改用 resolver。
- 優點：最符合 v2 stable contract，能逐步替換，不需要一次重寫 UI。
- 缺點：需要先定義 adapter output model，短期會有舊 loader 與新 resolver 並存。

### B

- 做法：只修 `StudyContentLocator` 與 `DictionaryRepository` 的硬編路徑，讓它們讀現有 manifest modules。
- 優點：改動小，能快速減少部分路徑 drift。
- 缺點：仍然讓 repository 負責 layout 細節，沒有真正建立 v2 contract boundary。

### C

- 做法：先暫停 frontend 改動，只補 PRG production bundle 與 asset promotion，再讓 frontend 繼續吃 production folder。
- 優點：release path 比較乾淨。
- 缺點：frontend runtime 仍可能把 production layout 當 schema，UI 顯示資料問題不會被根治。

## 決策

- Selected option: A
- Why: 本任務的核心不是把某幾個 path 修到能跑，而是讓 frontend 消費 v2-derived stable contract。Adapter/resolver boundary 才能防止之後 v2 inventory、PRG output、或 production folder layout 改動時 UI 一起壞。
- Rejected options: B 只能局部止血；C 只解 release promotion，不解 frontend coupling。

## 風險

- Risk: Adapter boundary 過大，變成跨 repo 大重構。
- Impact: 實作範圍膨脹，容易破壞現有可播放 lesson / dictionary overlay。
- Mitigation: 先用 inventory task 定義最小 resolver API，再分 study、dictionary、tests 三個 implementation slice。

- Risk: PRG output contract 與 frontend expected contract 不一致。
- Impact: release artifacts 產出後仍無法被前端穩定消費。
- Mitigation: 在 Codex implementation 前，先用 DeepSeek `flash` 做 inventory，再用 `pro` 或 GPT 5.5 裁決 production artifact target。

- Risk: 真實 v2 fixture 太大或不穩。
- Impact: Flutter test 變慢或 brittle。
- Mitigation: 選一個 small Korean v2 fixture，固定在 production test fixture 或 deterministic staging fixture。

## 驗收標準

- [ ] 有一份 frontend v2 data-flow inventory，列出 study、dictionary、grammar、learning-library 現況與 direct path coupling。
- [ ] 有一個 GPT 5.5 接受的 adapter / resolver contract，明確定義 frontend 從 v2-derived artifacts 取得 lesson metadata、lesson body、dictionary entry、translation overlay、grammar refs 的方式。
- [ ] Study runtime 不再由 UI-facing repository 任意硬組 production package path；實體 layout 解析集中在 adapter/resolver 邊界。
- [ ] Lesson registry discovery 由 manifest/contract 驅動，不再硬編 `packages/ko/lessons/modular_lessons.json` 作為獨立真相來源。
- [ ] Dictionary hub、overlay、lesson lookup 共用同一個 v2 dictionary adapter contract；若仍需 legacy packaged files，必須在 adapter 中明確標示 compatibility layer。
- [ ] PRG / sync bridge 能產出或驗證 frontend 可吃的 v2-derived production artifact，不依賴 raw `content-ko` scan 作為 production truth。
- [ ] Frontend content validation 至少載入一組真實 Korean v2-derived production fixture，覆蓋 lesson display、dictionary lookup、translation/hydration 的基本路徑。
- [ ] Targeted tests 已執行並記錄：`flutter test` 相關 frontend tests，以及 release-aggregator PRG/frontend contract tests。

## Out Of Scope

- 不做 Stitch UI visual design。
- 不做大規模課程內容重寫。
- 不做 dictionary entry quality cleanup；那屬於 `DICTIONARY_ENTRY_DRIFT_REVIEW`。
- 不做 grammar content ingestion；只處理 frontend consumption contract。
- 不直接把所有 legacy loaders 刪除；保留必要 fallback 直到 replacement 通過測試。
