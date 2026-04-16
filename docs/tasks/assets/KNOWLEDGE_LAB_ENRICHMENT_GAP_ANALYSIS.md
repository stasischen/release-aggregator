# Knowledge Lab Enrichment Gap Analysis

## 1. High-Value Knowledge Gaps

### Missing Essential Items (A1-1)

- **Honorific System**: `~으시` (verb suffix), `~이사/가` (copula), and honorific nouns (`그분`, `댁`, etc) are pervasive in basic dialogue but missing in the lab.
- **Essential Greetings**: `안녕하세요` (Hello) and `감사합니다 / 고맙습니다` (Thank you) lack dedicated knowledge entries with teaching notes.
- **Echo Questions**: `~요?` (e.g. "부산요?") is a common conversational pattern not currently captured.

### Granularity & Depth

- **Particle Nuances**: Existing items like `~은/는` (Topic) and `~이/가` (Subject) are present, but their contrastive usage in a single source is not highlighted.
- **Explanation Depth**: i18n explanations are factual but lacking "learner-centric" tips (e.g., common mistakes or social context).

## 2. Topic-to-Source Coverage Gaps

- **Place/Location**: `A1-01` relies on locations (`學校`, `辦公室`, `首爾`, `釜山`), but there is no `topic.place` family to aggregate these.
- **Identity/Profession**: `A1-01` introduces `신입생`, `선생님`, `의사`. No `topic.identity` family exists to link these career/role terms.
- **Social Distance/Family**: `A1-01` mentions `저희 아버지`, `어머니`. No `topic.family` exists.

## 3. Link Quality Gaps

- **Missing Logical Links**: Several sentences in `A1-01` use particles (`~을/를`, `~에`) that are available in the core lab but are not linked.
- **Lack of Retrieval Links**: There are no links from `topics` back to the specific "Golden Example" sentences in the sources, making retrieval less effective for the learner.
- **Relation Incompleteness**: `knowledge` items are rarely linked to each other (e.g., `copula` could link to `honorific_copula`).

## 4. Vocab Set Selection Gaps

- **Teaching Value**: The current selection of 4 items for `A1-01` misses the most important verbs (`오다`, `살다`, `이다`) and high-frequency nouns (`선생님`, `수업`).
- **Surface Coverage**: No specialized "verbs of existence" or "action verbs" sets are derived from the first dialogue.

## 5. Retrieval / Review Support Gaps

- **Learner Notes**: The `i18n` packs lack a "Common Confusion" or "Quick Tip" field that could be used for flashcards or retrieval prompts.
- **Contextualization**: Links describe *what* is used, but not *why* it's significant in that specific context (e.g., why `~에서` was used for `부산에서 왔어요` vs `~에`).
