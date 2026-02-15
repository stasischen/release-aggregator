---
description: control-tower closeout shim
---
# Closeout Shim (Control Tower)

Active protocol source:
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/gemini_closeout_protocol.md`

Routing references:
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/closeout_frontend.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/closeout_content.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/closeout_pipeline.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/closeout_release.md`
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/closeout_schema.md`

Rules:
1. Select protocols only by touched repos.
2. Never claim done without command evidence.
3. Write undecided items to control-tower daily worklog.
