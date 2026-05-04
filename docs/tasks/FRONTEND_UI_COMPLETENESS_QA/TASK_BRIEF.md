# Task Brief

## Metadata

- Task ID: FRONTEND_UI_COMPLETENESS_QA
- Owner: release-aggregator control tower
- Target repo: `lingo-frontend-web`
- Status: in_progress
- DeepSeek routing: flash -> pro
- Created: 2026-05-04
- Last updated: 2026-05-04

## Goal

Close the UI/product completeness gaps found after `FRONTEND_V2_INTAKE_COMPLETION`.
The frontend must present real v2-derived content through product routes without seed-only
defaults, dead routes, obvious placeholders, or collapsed dictionary ambiguity.

## Findings To Address

1. Learning Library still defaults to seed mode.
2. Video cards push `/video/player`, but the router only registers `/study/video/player`.
3. Video list `See all` still displays a coming-soon snackbar.
4. Dictionary UI has backend candidate/homograph data but no disambiguation UI.
5. Modular lesson runtime still exposes pilot placeholders for article/runtime preview surfaces.

## Constraints

- Do not change lesson data format without a separate brief.
- Do not touch `content-ko` or `content-pipeline`.
- Do not remove `mapping_v2` origin cache until dictionary core-origin migration Phase 3 validation passes.
- Do not unify domain adapter semantics; only improve product UI completeness and route/default behavior.
- Keep changes narrow and testable.

## Acceptance Criteria

- Learning Library product path defaults to artifact mode or reads an explicit frontend config/env switch.
- Video card navigation opens the registered player route.
- Video list has no visible coming-soon action for real content browsing.
- Dictionary disambiguation has a scoped follow-up design or an implemented minimal candidate picker using existing service APIs.
- Modular runtime placeholders are either hidden from product routes or tracked as pilot-only with explicit task ownership.
- Targeted Flutter tests or documented validation are added for changed product behavior.

