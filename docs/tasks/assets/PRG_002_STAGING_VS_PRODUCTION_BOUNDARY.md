# PRG-002: Staging Catalog vs. Production Manifest Boundary

## Goal

Define a clear division of responsibility between the **Staging Catalog** and the **Production Manifest**. Staging is an inventory of all buildable content (candidates), while Production is a subset of verified, final instructional designs.

## 1. Boundary Matrix

| Feature | Staging Catalog | Production Manifest |
| :--- | :--- | :--- |
| **Name** | `stg.candidate_inventory.json` | `prd.release_manifest.json` |
| **Logic** | Build-driven (Automatic scanning) | Decision-driven (Explicit allowlist) |
| **Scope** | All content in `content-ko` (including B1+ segmentation-in-progress) | Only `production-ready` units and lessons. |
| **Gating Level** | Content Integrity (Core + I18N check) | QA + Instructional Verification |
| **Target Audience** | Internal QA, Reviewers, In-situ Verification | Final App Users |
| **Content Units** | `raw source` & `lesson` | `lesson` & `unit` |

## 2. Decision Hierarchy

1. **Source is just material**: The existence of `src.ko.dialogue.a1_01` in the core repository does not constitute a "lesson" for the end-user.
2. **Instructional Design is the product**: A `lesson` / `unit` is the smallest unit of instructional delivery. Gating must happen at this layer because an instructionally complete unit may require multiple sources or specific metadata that isn't fully captured by raw source file scanning alone.
3. **Fail-Closed**: If a lesson is not in the `prd.release_manifest.json` with `release_status: production`, the Production Assembler MUST NOT include it even if the source is otherwise valid.

## 3. Workflow Diagram

```mermaid
graph TD
    A[content-ko / source truth] -->|Pipeline Build| B[Staging Candidate Artifacts]
    B --> C[Staging Catalog / Full Inventory]
    C -->|Inst. Review & QA| D{Release Decision}
    D -->|Allowlist| E[Production Release Manifest]
    E -->|Production Assembler| F[Production Bundle / Frontend Assets]
    D -- x |Omitted/Draft| G[Remains Staging Only]
```

## 4. Key Takeaways for Developers

- **Staging** is for "Can I build it?"
- **Production** is for "Should I release it?"
- **Production Assembler** should NEVER scan `core/dialogue` or `core/video` directly for production releases. Its ONLY source of truth for "what to include" is the Production Release Manifest.
