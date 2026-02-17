# PLAN

```xml
<plan id="AGGREGATOR-BOOTSTRAP" version="1.0">
  <task id="AGG-001" status="pending" repo="release-aggregator" type="docs">
    <title>Finalize GSD orchestration docs</title>
    <scope>
      Update startup, stage, closeout, and reference-order documents.
    </scope>
    <validation>
      <step>Links resolve from docs/index.md and runbooks/README.md</step>
      <step>Protocol docs include execution_mode rules</step>
    </validation>
    <deliverables>
      <file>/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/gsd_multi_repo_workflow.md</file>
    </deliverables>
  </task>

  <task id="AGG-002" status="pending" repo="content-ko" type="bootstrap">
    <title>Create repo-level state files</title>
    <scope>
      Add REQUIREMENTS.md, STATE.md, and PLAN.md in active repo.
    </scope>
    <validation>
      <step>All 3 files exist at repo root</step>
      <step>PLAN.md uses XML task structure</step>
    </validation>
    <deliverables>
      <file>/Users/ywchen/Dev/lingo/content-ko/REQUIREMENTS.md</file>
      <file>/Users/ywchen/Dev/lingo/content-ko/STATE.md</file>
      <file>/Users/ywchen/Dev/lingo/content-ko/PLAN.md</file>
    </deliverables>
  </task>
</plan>
```
