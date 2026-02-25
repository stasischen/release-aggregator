# Content Candidate Review Station Implementation Plan

## Overview
建立一個候選內容中文審核台，讓 AI 產生的韓文課程候選內容（Candidate Content）能在 Aggregator 中進行中文審核、修改與決策。

## Task IDs
- AGG-CR-001: Schema + mock data
- AGG-CR-002: Review screen MVP (Route: /content-review)
- AGG-CR-003: Filters + search + progress
- AGG-CR-004: Persistence (Local Storage)
- AGG-CR-005: Import/export (JSON)
- AGG-CR-006: Batch actions
- AGG-CR-007: Export adapters (catalog/backlog seed)

## Technical Stack
- Framework: Flutter Web
- Location: `release-aggregator/tools/content_candidate_review`
- State Management: Provider or Riverpod (based on project preference, defaulting to simple state for MVP)
- Persistence: `shared_preferences` or local JSON storage.

## Data Model (CandidateReviewItem)
- `candidate_id`: String
- `batch_id`: String
- `candidate_type`: String
- `target_level`: String
- `target_unit_id`: String
- `target_position`: Int
- `title_zh_tw`: String
- `subtitle_zh_tw`: String
- `can_do_zh_tw`: List<String>
- `review_summary_zh_tw`: String
- `novelty_rationale_zh_tw`: String
- `risk_flags_zh_tw`: List<String>
- `agent_recommendation`: String
- `scores`: Map<String, Double> (fit/novelty/learnability/reuse/engagement/cost)
- `foreign_preview`: Map<String, dynamic> (collapsible)
- `human_decision`: Enum (unreviewed/accept/revise/reject/parked)
- `human_notes_zh_tw`: String
- `updated_at`: DateTime
