# Codex Task Packet

## Objective

After the content/artifact inventory returns, define and implement the narrowest frontend
step that moves Knowledge Lab from old artifact-backed source/detail UI toward an
index-first Knowledge-First Lab.

Do not start frontend code until `TASK_BRIEF.md`, `TASKS.json`, and this packet exist.

## Immediate Codex Scope

Current approved scope:

1. Keep release-aggregator task artifacts in sync.
2. Review Gemini content/artifact inventory.
3. Draft Knowledge-First Lab UI acceptance matrix.
4. Prepare a narrow frontend implementation brief.

Frontend code is not approved in this packet yet.

## Likely Frontend Implementation Scope

The next frontend implementation should likely touch only:

- `lib/features/learning_library/presentation/**`
- `lib/features/learning_library/data/**`
- targeted tests under `test/features/learning_library/**`

Implementation should avoid:

- lesson runtime data format
- `content-ko` content edits
- `content-pipeline` edits
- dictionary mapping cache removal
- broad design-system refactors

## Expected Product Shape

Knowledge Lab should become a knowledge-first browser:

- Home: indexed entry points for Grammar, Pattern, Usage, Topic, Vocab.
- Search/filter: support kind, subcategory, level, and tags.
- Knowledge detail: explanation, examples, related topics, related sources/sentences.
- Topic detail: related knowledge, vocab sets, example sentences, source reverse lookup.
- Vocab detail: teaching selection layer with optional dictionary atom refs.

The UI may reuse existing Learning Library repository snapshots, but screens must not
perform core/i18n merge logic.

## Validation

At minimum, the implementation packet must specify targeted Flutter tests for:

- artifact-mode Knowledge Lab home renders from real Korean assets
- knowledge index list renders more than seed sample count
- selecting a knowledge item opens detail
- detail can show related sentences/sources when refs exist
- missing optional vocab_sets does not crash the whole Knowledge Lab unless the contract says it is required

