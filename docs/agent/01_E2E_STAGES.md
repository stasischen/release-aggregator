# Agent E2E Stages (English Only)

| Stage | Name | Primary Repo | Key Output |
|---|---|---|---|
| S0 | Writer Source | `lllo` | Source lesson materials |
| S1 | Ingestion | `content-ko` | Canonical source artifacts |
| S2 | Segmentation + Mapping | `content-ko` | Token/mapping artifacts |
| S3 | Build + Validate | `content-pipeline` | `dist/**` artifacts |
| S4 | Release Aggregation | `release-aggregator` | `staging/<version>/**` + `global_manifest.json` |
| S5 | Frontend Intake | `lingo-frontend-web` | Imported frontend assets |
| S6 | Deploy + Rollback | Frontend + Ops | Production cut with rollback target |
