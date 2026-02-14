# Repository Map

The Lingo system is split into specialized repositories to ensure clear ownership and scalability.

| Repo Name | Role | Primary Owner | Canonical Docs |
| :--- | :--- | :--- | :--- |
| `core-schema` | JSON Schemas & Validation | Architects | `docs/CONTRACT_DICTIONARY_GRAMMAR.md` |
| `content-ko` | Korean Source & Ingestion | Content Team | `README.md` |
| `content-pipeline` | Build & CI/CD | DevOps / Infra | `README.md` |
| `release-aggregator`| Release & Docs Hub | Release Manager | `docs/index.md` |
| `lingo-frontend-web`| Frontend & Asset Intake | Frontend Team | `.agent/skills/` |

## Navigation Policy
Each repository's README must link back to the [Control Tower Index](./index.md) for cross-repo workflows.
