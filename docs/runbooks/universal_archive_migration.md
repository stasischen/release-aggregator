# Universal Archive Migration Runbook

## Goal
Consolidate all authoritative process/docs into control tower (`release-aggregator/docs`) and prevent agents from using monorepo docs as live protocol.

## Policy
- Canonical docs: `release-aggregator/docs/**`
- Archived docs: `release-aggregator/docs/archive/universal/**`
- `Lingourmet_universal` is historical only and non-authoritative.

## Source and Target
- Source: `/Users/ywchen/Dev/Lingourmet_universal`
- Target: `/Users/ywchen/Dev/lingo/release-aggregator/docs/archive/universal`

## Migration Scope
Archive these paths from universal:
- `docs/planning/**`
- `docs/handoffs/**`
- `docs/guides/**`
- `docs/project/**`
- `.agent/workflows/**`
- `.agent/templates/**`

Do not migrate runtime/product code from monorepo.

## Step 1: Dry Run Inventory
```bash
cd /Users/ywchen/Dev/lingo/release-aggregator
bash scripts/migrate_universal_docs_to_control_tower.sh --dry-run
```

## Step 2: Execute Migration (Copy Only)
```bash
cd /Users/ywchen/Dev/lingo/release-aggregator
bash scripts/migrate_universal_docs_to_control_tower.sh --apply
```

## Step 3: Update Archive Index
- Update `docs/archive/universal/INDEX.md`
- Record date, source commit, and migrated paths.

## Step 4: Lock Monorepo as Non-Authoritative
In `Lingourmet_universal`:
- Keep only archive notices and pointer links for process docs.
- Do not keep active `.agent` workflow as source of truth.

## Step 5: Enforce Agent Prompt Guardrail
Use this line in Gemini session start:

`禁止讀取或修改 /Users/ywchen/Dev/Lingourmet_universal 的協議文件；所有協議只讀 /Users/ywchen/Dev/lingo/release-aggregator/docs。`

## Success Criteria
- All active protocol links point to control tower.
- Universal docs are archived and discoverable only via archive index.
- New sessions no longer reference monorepo workflows.
