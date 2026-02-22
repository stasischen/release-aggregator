# End-to-End Stages (Current)

This page describes the active stages and repo boundaries currently in use.

## Stage Table

| Stage | Name | Primary Repo | Key Output |
|---|---|---|---|
| S0 | Writer Source | `lllo` (upstream) | Source lesson materials |
| S1 | Ingestion | `content-ko` | Canonical source data |
| S2 | Segmentation + Mapping | `content-ko` | Core/I18N split + mapping artifacts |
| S3 | Build + Validate | `content-pipeline` | `dist/**` release-ready artifacts |
| S4 | Release Aggregation | `release-aggregator` | `staging/<version>/**` + `global_manifest.json` |
| S5 | Frontend Intake | `lingo-frontend-web` | Imported app assets |
| S6 | Deploy + Rollback Readiness | `lingo-frontend-web` + Ops | Production release state |

## Stage Links

- `docs/human-handbook/stages/S0_source.md`
- `docs/human-handbook/stages/S1_ingestion.md`
- `docs/human-handbook/stages/S2_segmentation_mapping.md`
- `docs/human-handbook/stages/S3_build_validate.md`
- `docs/human-handbook/stages/S4_release_aggregation.md`
- `docs/human-handbook/stages/S5_frontend_intake.md`
- `docs/human-handbook/stages/S6_deploy_rollback.md`
