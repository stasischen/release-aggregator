# LLCM-006a — Staging Frontend Intake Switch Definition

## Goal

在 `lingo-frontend-web` 定義一個明確的 Learning Library 資料來源切換機制，讓 staging 可以安全切到 pipeline `core + i18n packs`，同時保留 seed compare mode 供回歸比對。

這一步的目的不是完成所有 artifact intake，而是先把「資料入口開關」定義清楚，避免後續 `dialogue / video` staging recovery 直接覆蓋既有 seed 路徑。

## Current Repo State

`lingo-frontend-web` 已經具備主體能力：

- `LearningLibraryMode.seed / artifact`
- `LearningLibraryContentRepository` 依 mode 切到 seed loader 或 artifact data source
- `ArtifactLearningLibraryDataSource` 目前仍以單包 localized artifact 讀取
- `UniversalLauncherScreen` 已有 dev-only segmented switch

所以 `LLCM-006a` 並不是從零設計，而是把現有能力正式化為新的 staging intake switch contract，並把前端從單包 artifact intake 導向 `core + selected i18n` composition。

## Decision

正式切換語意固定為兩種 mode：

- `seed`
  - 讀 `learning_library_seed_json.dart`
  - 作為 prototype baseline
- `artifact`
  - 讀 target-language core pack + selected support-language i18n pack
  - 作為 staging recovery 驗證入口

`compare mode` 不新增第三個 enum。
它的意思是：

- 保留 `seed` 可隨時切回
- 在同一條 UI flow 下比對 `seed` 和 `artifact`
- 用於 list/detail parity 檢查，而不是雙資料源同時渲染

## Scope For LLCM-006a

本步只定義 intake switch 與驗證邊界：

1. 定義哪一層負責決定 Learning Library mode
2. 定義 staging 預設值與切換方式
3. 定義 seed / artifact composition loader 的責任邊界
4. 定義 compare workflow 的操作方式
5. 定義這一步的驗收標準

## Out Of Scope

本步不做以下事情：

- 不修 `dialogue / video` artifact 缺欄或 mapping 缺口
- 不處理 `B1+ segmentation`
- 不移除 seed mode
- 不回頭再擴充 localized finalized blob 作為新主線
- 不把 knowledge lab enrichment 併入 intake 路徑
- 不直接推 production default

這些屬於後續：

- `LLCM-006b`
- `LLCM-007a`
- `LLCM-007b`

## Switch Placement

### Source Of Truth

切換狀態的 source of truth 應維持在：

- `LearningLibraryModeController`
  - file: `lib/features/learning_library/domain/models/learning_library_mode.dart`

這樣 repository / screen / dev launcher 都共用同一個 mode。

### Consumption Layer

資料來源選擇應維持在：

- `LearningLibraryContentRepository`
  - file: `lib/features/learning_library/data/repositories/learning_library_content_repository.dart`

責任分工如下：

- `mode controller`
  - 只負責目前使用哪個來源
- `content repository`
  - 只負責依 mode 選 source
- `seed loader`
  - 繼續作為 baseline path
- `artifact data source`
  - 過渡為 staging `core + i18n` composition path

UI screen 不應自己判斷要讀 seed 還是 artifact，也不應自己手動 merge core 與 i18n。

## Recommended Switch Behavior

### Default Policy

- Dev / staging:
  - 預設可以先維持 `seed`
  - 必須可手動切到 `artifact`
- Production:
  - 目前不改 default
  - artifact mode 尚未通過 parity 前，不作為正式預設

### Activation Surface

近期建議沿用現有 dev surface：

- `UniversalLauncherScreen` segmented switch

若後續要讓 staging QA 更方便，可再補其中一種：

- debug menu toggle
- query / route parameter
- debug-only persisted preference

但 `LLCM-006a` 本身不要求一次把所有入口都做完。

## Compare Mode Workflow

`compare mode` 的標準操作方式如下：

1. 用 `seed` 打開同一個 source
2. 記錄 list/detail 是否正常顯示
3. 切到 `artifact`
4. 走同一條路徑再驗一次
5. 把差異記到 mismatch list

這裡的 compare 重點是：

- 同一個 `sourceId`
- 同一條 screen flow
- 同一組基本驗收點

不是要求 seed 與 artifact 完全 byte-for-byte 一樣，而是要確認：

- source 可見
- detail 可打開
- sentences 可顯示
- 基本 linking / metadata 不崩潰

## Contract Boundary

`LLCM-006a` 必須遵守以下邊界：

1. 正式主線改為 `target core + support i18n`，不再追加 localized finalized blob 依賴
2. 不要求 pack 先補 production-ready 欄位
3. 允許 pack 內容仍為 `staging_only`
4. readiness / segmentation 相關資訊若需要顯示，只能作為 staging debug metadata，不可破壞 `core / i18n` 邊界

## Immediate Implementation Target

對 `lingo-frontend-web` 來說，這一步最小可交付是：

1. 明確保留 `LearningLibraryMode.seed`
2. 明確保留 `LearningLibraryMode.artifact`
3. repository path 只透過 mode 做 source selection
4. `artifact` mode 內部改為 `target core + selected i18n` composition
5. dev launcher 可切換 mode 並重跑相同 source detail flow
6. artifact load failure 能明確報錯，而不是 silent fallback 回 seed

最後一點很重要：
artifact 壞掉時，不能偷偷回 seed，否則 staging parity 會失真。

## Acceptance Criteria

`LLCM-006a` 完成時，至少要滿足：

1. 前端有單一 source-of-truth mode 開關，不是各 screen 各自分叉
2. `seed` 與 `artifact` 可在同一個 app session 中切換
3. `artifact` mode 以 `core + selected i18n` 組裝，不再依賴 localized finalized blob
4. `artifact` 路徑失敗時能明確看出是 artifact failure
5. `seed` mode 仍可作為 baseline compare path
6. production 預設行為不因這次工作而被改動

## Next Task Handoff

完成 `LLCM-006a` 後，下一手應直接接：

- `LLCM-006b`
  - 把 `dialogue / video` 的 artifact loader 與 staging debug metadata 接實
- `LLCM-007a`
  - 跑 `seed` vs `artifact` parity
- `LLCM-007b`
  - 記 mismatch 與 staging acceptance gate

## Reference Files

- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/domain/models/learning_library_mode.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/data/repositories/learning_library_content_repository.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/learning_library/data/sources/artifact_learning_library_data_source.dart`
- `/Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/dev/presentation/universal_launcher_screen.dart`
