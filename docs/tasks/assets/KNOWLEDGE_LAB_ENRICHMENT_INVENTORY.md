# Knowledge Lab Enrichment Inventory

## 1. Source Coverage (Staging)

| Source ID | Type | Status | Enrichment Level |
| :--- | :--- | :--- | :--- |
| `A1-01` | Dialogue | Staging/Recovered | **Low** (Sparse links, low vocab density) |
| `79Pwq7MTUPE` | Video | Staging/Recovered | **Low** (Basic metadata only) |
| `a1_01_intro` | Article | Staging/Recovered | **Low** (Basic vocab set only) |

## 2. Knowledge Item Coverage (Grammar/Patterns)

### Grammar (`kg.grammar.*`)

- **Particle**: `subject`, `object`, `topic`, `also`, `at_time_place`, `at_place_action`, `and_with_hago`.
- **Copula**: `present_formal`, `present_informal`, `present_polite_informal`.
- **Negation**: `short_an`, `short_mot`, `long_ji_anta`.
- **Tense**: `future_geoyeyo`, `past_ass_oss`.
- **Honorific**: `suffix_ssi` (only).

### Patterns (`kp.*`)

- **Greetings**: `annyeong`, `bangawoyo`.
- **Questions**: `polite_question`.

### Expressions (`ke.*`)

- **Greetings**: **EMPTY** directory.

## 3. Topic Family Coverage

- **Time (`topic.time.*`)**:
  - `clock_time`
  - `relative_day`
  - `weekday`
- **Other families**: **NONE** (Location, Identity, Profession, Family are all missing).

## 4. Link Density (Sample: A1-01)

- **Total Sentences**: ~40 in core dialogue.
- **Linked Knowledge/Patterns**: 8 items linked across 5 sentences.
- **Unlinked High-Value Grammar**:
  - `~에` / `~에서` (Location) - *Available in core but unlinked in A1-01*.
  - `~을/를` (Object) - *Available in core but unlinked in A1-01*.
  - `~으시` (Honorific) - *Missing item*.
  - `~요?` (Echo question) - *Missing item*.

## 5. Vocab Set Density (Sample: A1-01)

- **Current items**: `신입생`, `첫날`, `서울`, `부산` (4 items).
- **Missing Core Vocab**: `선생님`, `의사`, `학교`, `電腦室`, `網路`, `搬家`, `期待` (~15 items).

## 6. Technical Integrity (JSON State)

- **TODOs**: None found in core/i18n packs so far, but content is sparse.
- **Translations**: Basic `zh_tw` present for items found.
- **Schema Compliance**: All files checked so far follow the `core/i18n` split contract.
