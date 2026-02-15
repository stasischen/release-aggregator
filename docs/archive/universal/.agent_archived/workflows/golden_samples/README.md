# Golden Samples: Linguistic Audit Reports

This directory contains high-standard examples of manual linguistic audit reports for different phases of the V5 content pipeline. These should be used as the benchmark for all future audits.

## Phase 1: Translation Audit (`audit_report_ko_p1.md`)

- **Focus**: Semantic accuracy, cross-language consistency, and tone preservation.
- **Key Requirement**: Mandatory quotes from the source/target as proof of deep manual review.
- **Goal**: 100% semantic alignment.

## Phase 2: Atoms Audit (`audit_report_ko_p2.md`)

- **Focus**: Perfect reconstruction, suffix splitting, and POS tagging precision.
- **Key Requirement**: Proof of linguistic fixes (e.g., specific stem/ending splits).
- **Goal**: 100% reconstruction fidelity and absolute grammatical precision.

## Phase 3: Mapping Audit (`audit_report_ko_p3.md`)

- **Focus**: Semantic deduplication, homonym resolution, and dictionary-aligned segmentation.
- **Key Requirement**: Systematic split of Numbers/Units and standardizing Counter (量詞) tagging to `pos: M`.
- **Goal**: 100% dictionary-compatible mapping with manual collision locks.

---

_Standards established by the Korean Linguistic Hardening (2026-01-16)._
