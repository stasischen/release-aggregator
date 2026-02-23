# Human Handbook: Start Here
# 人類手冊：從這裡開始

Purpose: a human-readable, current flow from content generation to deployment.
目的：提供「人可讀」且「目前最新」的內容產生到部署流程。

Last reviewed: 2026-02-23
最後檢視日期：2026-02-23

## Canonical Reading Order
## 正式閱讀順序

1. `docs/human-handbook/01_E2E_STAGES.md`
2. `docs/human-handbook/02_TOOL_CATALOG.md`
3. `docs/human-handbook/03_STAGE_CHECKLISTS.md`
4. `docs/runbooks/release_cut_and_rollback.md`

## Not Canonical (Historical)
## 非現行（歷史文件）

- Historical planning docs are archived in `docs/archive/legacy/`.
- 歷史規劃文件已歸檔於 `docs/archive/legacy/`。

## Current Snapshot
## 目前流程快照

1. Source content is authored upstream (`lllo`) and ingested in `content-ko`.
1. 上游 `lllo` 產生內容，於 `content-ko` 做 ingestion。
2. `content-ko` performs preflight-gated review, gold QA, and staged dictionary/mapping promotion.
2. `content-ko` 執行具 preflight gate 的 review、gold QA，並以 staged candidate 方式 promotion dictionary/mapping。
3. `content-pipeline` builds artifacts into `dist/`.
3. `content-pipeline` 產出 `dist/`。
4. `release-aggregator` runs `scripts/release.sh` and `scripts/release.py`.
4. `release-aggregator` 透過 `scripts/release.sh` / `scripts/release.py` 聚合發版。
5. Manifest is validated against `core-schema`.
5. 以 `core-schema` 驗證 manifest。
6. `lingo-frontend-web` performs intake and production checks.
6. `lingo-frontend-web` 進行接收與上線驗證。
