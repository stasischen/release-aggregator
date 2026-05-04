# Content Dictionary Coverage Drift Report

Date: 2026-05-05

Scope:
- Frontend runtime dictionary package: `lingo-frontend-web/assets/content/production/packages/ko`
- Content dictionary inventory: `content-ko/content_v2/inventory/dictionary/2026-05-04`
- Atomized video source: `content-ko/content/core/video_atoms`

## Summary

The video atoms are present in frontend video assets, and mapping ids exist for many particles/endings. The product issue is not atomization loss.

The drift is between atom coverage and dictionary i18n coverage:
- Mapping answers "which atom id is this surface?"
- Dictionary i18n must answer "how should this atom be explained to the learner?"

For many high-frequency Korean function atoms, the inventory has ids but no usable `zh_tw` glossary:

```json
{
  "atom_id": "ko:p:는",
  "definitions": {"zh_tw": []},
  "translation": {"zh_tw": null}
}
```

This causes frontend dictionary surfaces to show `No definition found` even when the video atom is correctly segmented.

## Evidence

Frontend video atom example:

File:
`lingo-frontend-web/assets/content/production/packages/ko/video/core/ko_v1_vlog_pzqtJI-FxJg_christmas_cards.json`

First turn:

```json
{
  "id": "v_001",
  "text": {"ko": "안녕하세요. 여러분. 재림이에요."},
  "content": {
    "atoms": [
      {"id": "ko:adj:안녕하다+ko:e:시+ko:e:어요", "text": "안녕하세요", "pos": "adj+e+e"},
      {"id": "ko:pron:여러분", "text": "여러분", "pos": "pron"},
      {"id": "ko:prop:재림+ko:cop:이다+ko:e:에요", "text": "재림이에요", "pos": "prop+cop+e"}
    ]
  }
}
```

Content inventory examples:

`content-ko/content_v2/inventory/dictionary/2026-05-04/e.jsonl`

```json
{"atom_id":"ko:e:어요","definitions":{"zh_tw":[]},"translation":{"zh_tw":null}}
```

`content-ko/content_v2/inventory/dictionary/2026-05-04/p.jsonl`

```json
{"atom_id":"ko:p:을","definitions":{"zh_tw":[]},"translation":{"zh_tw":null}}
{"atom_id":"ko:p:는","definitions":{"zh_tw":[]},"translation":{"zh_tw":null}}
{"atom_id":"ko:p:에","definitions":{"zh_tw":[]},"translation":{"zh_tw":null}}
```

Counterexample where content is complete:

`content-ko/content_v2/inventory/dictionary/2026-05-04/e.jsonl`

```json
{"atom_id":"ko:e:시","definitions":{"zh_tw":[{"gloss":"（尊稱）"}]},"translation":{"zh_tw":"（尊稱）"}}
```

`content-ko/content_v2/inventory/dictionary/2026-05-04/pron.jsonl`

```json
{"atom_id":"ko:pron:여러분","definitions":{"zh_tw":[{"gloss":"各位；大家。"},{"gloss":"各位；諸位"}]}}
```

## Coverage Snapshot

After syncing the current dictionary package into frontend:

| Metric | Count |
| --- | ---: |
| Unique video component atom ids used | 1,989 |
| Missing from frontend dictionary package | 623 unique / 2,084 occurrences |
| Present but empty `zh_tw` meaning | 43 unique / 5,232 occurrences |

Highest-frequency empty definitions:

| Atom id | Occurrences | Required content type |
| --- | ---: | --- |
| `ko:e:어요` | 1,142 | functional ending glossary |
| `ko:e:아요` | 549 | functional ending glossary |
| `ko:p:을` | 493 | particle glossary |
| `ko:p:는` | 442 | particle glossary |
| `ko:p:에` | 422 | particle glossary |
| `ko:p:를` | 361 | particle glossary |
| `ko:p:가` | 321 | particle glossary |
| `ko:p:이` | 320 | particle glossary |
| `ko:p:은` | 227 | particle glossary |
| `ko:p:도` | 226 | particle glossary |
| `ko:e:었` | 157 | tense ending glossary |
| `ko:p:에서` | 120 | particle glossary |

Highest-frequency missing ids:

| Atom id | Occurrences | Notes |
| --- | ---: | --- |
| `ko:n:것` | 135 | common bound noun |
| `ko:e:요` | 94 | polite ending |
| `ko:adv:이렇게` | 54 | common adverb |
| `ko:n:거` | 39 | colloquial bound noun |
| `ko:e:x` | 34 | invalid/placeholder atom id; should be remediated |
| `ko:n:저` | 27 | likely POS mismatch; should be pronoun |
| `ko:n:여러분` | 26 | POS mismatch; inventory has `ko:pron:여러분` |
| `ko:prop:재림` | 15 | proper noun; needs display policy |

## Required Content Fix

Content side should treat video/sentence atoms as consumers of the dictionary inventory.

For each atom id emitted by:
- `content-ko/content/core/video_atoms/*.json`
- Sentence Bank atomized examples

The dictionary inventory should provide:
- Core entry in `content_v2/inventory/dictionary/2026-05-04/{pos}.jsonl`
- Non-empty `definitions.zh_tw[]` for learner-facing dictionary display
- Non-empty `translation.zh_tw` when a concise label is possible
- POS-canonical id alignment, for example avoid `ko:n:여러분` if canonical is `ko:pron:여러분`

## Suggested Seed Glossary

These are suggested zh_tw starter glosses for content review, not final contract text.

| Atom id | Suggested zh_tw gloss |
| --- | --- |
| `ko:p:이` / `ko:p:가` | 主格助詞，標示句子主語。 |
| `ko:p:은` / `ko:p:는` | 主題助詞，標示談論的主題或對比。 |
| `ko:p:을` / `ko:p:를` | 受詞助詞，標示動作的對象。 |
| `ko:p:에` | 助詞，標示時間、地點、方向或目的地。 |
| `ko:p:에서` | 助詞，標示動作發生的地點或起點。 |
| `ko:p:도` | 助詞，表示「也」。 |
| `ko:p:의` | 所有格助詞，表示「的」。 |
| `ko:p:로` / `ko:p:으로` | 助詞，表示方向、手段、材料或身份。 |
| `ko:p:랑` / `ko:p:이랑` / `ko:p:하고` | 口語助詞，表示「和、跟」。 |
| `ko:p:한테` / `ko:p:에게` | 助詞，表示對象「給、向」。 |
| `ko:p:까지` | 助詞，表示「到、直到、連...也」。 |
| `ko:p:부터` | 助詞，表示「從...開始」。 |
| `ko:p:만` | 助詞，表示「只、只有」。 |
| `ko:p:마다` | 助詞，表示「每、每逢」。 |
| `ko:p:보다` | 比較助詞，表示「比...」。 |
| `ko:e:어요` / `ko:e:아요` | 非格式體禮貌語尾，用於現在或一般敘述。 |
| `ko:e:에요` / `ko:e:여요` | 禮貌敘述語尾，常接在이다或하다類變化後。 |
| `ko:e:요` | 禮貌語尾，使句子語氣客氣。 |
| `ko:e:었` / `ko:e:았` | 過去時標記。 |
| `ko:e:겠` | 推測、意志或未來語氣標記。 |
| `ko:e:고` | 連接語尾，表示「然後、並且」。 |
| `ko:e:아서` / `ko:e:어서` | 連接語尾，表示原因或動作順序。 |
| `ko:e:시` / `ko:e:으시` | 尊敬語標記，用來尊敬主語。 |
| `ko:e:ㄴ` / `ko:e:은` | 冠形語尾，修飾名詞，常表示已完成或狀態。 |
| `ko:e:는` | 冠形語尾，修飾名詞，常表示現在或進行。 |
| `ko:e:ㄹ` / `ko:e:을` | 冠形語尾，修飾名詞，常表示未來、意圖或可能。 |
| `ko:e:게` | 副詞化語尾，讓前面的詞修飾動作或狀態。 |
| `ko:e:기` | 名詞化語尾，把動作或狀態變成名詞。 |
| `ko:e:면` / `ko:e:으면` | 條件語尾，表示「如果」。 |
| `ko:e:는데` | 背景/轉折語尾，表示「但是、而且、先說背景」。 |
| `ko:e:나요` | 禮貌疑問語尾。 |
| `ko:e:거나` | 連接語尾，表示選擇「或」。 |
| `ko:e:네` | 感嘆/發現語尾。 |
| `ko:affix:-들` | 複數後綴，表示多個人或事物。 |
| `ko:affix:-님` | 尊稱後綴。 |

## Recommended Gates

Add a content-side gate before frontend sync:

1. Collect all component atom ids from `content/core/video_atoms/*.json`.
2. Collect all component atom ids from Sentence Bank artifacts.
3. Load `content_v2/inventory/dictionary/{version}/manifest.json`.
4. Fail if a used atom id is missing from inventory, except approved placeholders.
5. Fail if a used atom id has empty `definitions.zh_tw` and empty `translation.zh_tw`, except approved proper nouns.
6. Emit a top-N occurrence report so content editors can fix the highest-impact atoms first.

Suggested threshold for current app QA:
- P0: any top-50 occurrence atom has no zh_tw definition.
- P1: more than 1% of video atom component occurrences have no zh_tw definition.
- P2: proper nouns missing a display policy.

## Separate Bridge Issue

Release sync previously skipped dictionary assets unless `--include-dictionary` was passed. That made frontend carry stale dictionary packages even when `content-pipeline/dist` had newer ids.

Recommended bridge rule:
- `release-aggregator make sync-frontend-assets` should include dictionary assets by default for v2 QA.
- Validation should compare frontend dictionary package against current content inventory coverage.

