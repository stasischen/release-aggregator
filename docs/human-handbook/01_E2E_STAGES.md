# End-to-End Stages (Current)
# 端到端階段（現行）

This page defines active stages and repo boundaries.
本頁定義目前啟用中的階段與 repo 邊界。

## Stage Table
## 階段總表

| Stage | Name | 中文名稱 | Primary Repo | Key Output |
|---|---|---|---|---|
| S0 | Writer Source | 內容來源 | `lllo` (upstream) | Source lesson materials |
| S1 | Ingestion | 匯入正規化 | `content-ko` | Canonical source data |
| S2 | Segmentation + Mapping | 分詞與映射 | `content-ko` | Core/I18N split + mapping artifacts |
| S3 | Build + Validate | 建置與驗證 | `content-pipeline` | `dist/**` release-ready artifacts |
| S4 | Release Aggregation | 發版聚合 | `release-aggregator` | `staging/<version>/**` + `global_manifest.json` |
| S5 | Frontend Intake | 前端接收 | `lingo-frontend-web` | Imported app assets |
| S6 | Deploy + Rollback Readiness | 部署與回滾準備 | `lingo-frontend-web` + Ops | Production release state |

## Stage Pages
## 階段文件

- `docs/human-handbook/stages/S0_source.md`
- `docs/human-handbook/stages/S1_ingestion.md`
- `docs/human-handbook/stages/S2_segmentation_mapping.md`
- `docs/human-handbook/stages/S3_build_validate.md`
- `docs/human-handbook/stages/S4_release_aggregation.md`
- `docs/human-handbook/stages/S5_frontend_intake.md`
- `docs/human-handbook/stages/S6_deploy_rollback.md`
