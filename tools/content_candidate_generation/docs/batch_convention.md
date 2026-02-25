# Batch Directory Convention

All content generation batches should follow this directory structure to ensure consistency across API and Agent flows.

## Directory Root
Storage location: `docs/batches/{batch_id}/`

`batch_id` format: `YYYYMMDD_{level}_{units}_{run_tag}`
Example: `20260225_A1_U04_lessons_v1`

## File Manifest

| Filename | Stage | Description | Mandatory |
| :--- | :--- | :--- | :--- |
| `generation_brief.json` | Input | Defines goals, targets and constraints. | Yes |
| `gap_report.json` | Analysis | Analysis of existing content gaps (Agent flow). | No |
| `candidate_packs.api.raw.json` | Generation | Raw output from API generator. | API Flow |
| `candidate_packs.agent.raw.json` | Generation | Raw output from Agent generator. | Agent Flow |
| `candidate_packs.normalized.json` | Normalize | Canonical schema version of candidates. | Yes |
| `qa_report.json` | QA | Results of automated QA checks. | Yes |
| `review_ready_bundle.json` | Export | Final bundle for review station import. | Yes |
| `review_results.json` | Review | Exported results from the review station. | Yes (after review) |
| `accepted_candidates.json` | Post-Review | Filtered list of candidates marked as 'Accepted'. | Yes (after review) |
| `generation_report.json` | Metadata | Stats about the generation run (time, cost, etc). | Yes |

## Workflow Steps

1. **Briefing**: Create `generation_brief.json`.
2. **Generation**: Run API/Agent generator to produce `candidate_packs.*.raw.json`.
3. **Normalization**: Transform raw output to `candidate_packs.normalized.json`.
4. **QA**: Run QA tool to produce `qa_report.json`.
5. **Bundling**: Produce `review_ready_bundle.json`.
6. **Review**: (Human step) Use Review Station.
7. **Adopting**: Use adapters to turn `accepted_candidates.json` into catalogs or backlogs.
