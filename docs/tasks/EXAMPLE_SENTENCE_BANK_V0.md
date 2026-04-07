# Example Sentence Bank v0 Draft

## Goal

定義可被 `knowledge / pattern / topic / vocab / source sentence drill-down` 共用的例句庫草案。

本草案回答三件事：

1. 例句是否應從 `knowledge_item.example_bank` 抽離
2. 有 `slot` 的句子與沒有 `slot` 的句子是否要分兩套 schema
3. `example sentence` 和 `pattern_frame` 的責任邊界怎麼切

---

## Executive Decision

### 1. 例句應抽成共用資產

是。可重用例句應放進獨立 `example sentence bank`，不要長期留在 `knowledge_item.example_bank`。

### 2. 有 slot / 無 slot 不要拆成兩套 sentence schema

不建議拆成兩套完全不同規格。

建議做法：

- 共用一個 `example_sentence` base schema
- 需要 slot 化時，加 optional `frame_projection` / `slot_projection`

也就是：

- 每一筆都是句子
- 只有部分句子同時也是某個 frame 的「可參數化實例」

### 3. `pattern_frame` 與 `example_sentence` 不同

- `pattern_frame` 是教學框架，例如 `오늘은 N요일이에요`
- `example_sentence` 是具體句子，例如 `오늘은 토요일이에요.`

不要把 frame 當 sentence，也不要把 sentence 當 frame 本體。

---

## Why Shared Schema Is Better

如果把「slot sentence」和「plain sentence」拆成兩個 entity，常見問題會是：

- 同一句在 drill-down 時要查兩套表
- source sentence 與 example sentence 難以共用
- 後續要從真實句子自動抽 slot projection 時，會變成 duplicated storage
- 某些句子既是完整句，又能回投成 frame，身份會衝突

共用 schema 的好處是：

- 所有例句都可被同一套查詢、排序、TTS、難度與 link 邏輯處理
- 只有可泛化的句子才補 `slot_projection`
- 沒有 slot 的句子完全不受影響

---

## Entity Model

建議至少有三層：

1. `pattern_frame`
2. `example_sentence`
3. `example_sentence_link`

### `pattern_frame`

教學框架與可替換槽位定義。

例：

```json
{
  "id": "kp.time.today_is_weekday",
  "surface": "오늘은 N요일이에요",
  "kind": "pattern_frame"
}
```

### `example_sentence`

具體句子實例。

例：

```json
{
  "id": "ex.ko.time.today_is_saturday.v1",
  "surface_ko": "오늘은 토요일이에요.",
  "translation_zh_tw": "今天是星期六。"
}
```

### `example_sentence_link`

句子與其他 graph entity 的連結。

例：

```json
{
  "id": "link.ex.ko.time.today_is_saturday.v1.pattern",
  "source_id": "ex.ko.time.today_is_saturday.v1",
  "target_id": "kp.time.today_is_weekday",
  "relationType": "example_of"
}
```

---

## Proposed Schema

## 1. Base `example_sentence`

```json
{
  "id": "ex.ko.time.today_is_saturday.v1",
  "target_lang": "ko",
  "support_langs": ["zh_tw"],
  "surface_ko": "오늘은 토요일이에요.",
  "translation_zh_tw": "今天是星期六。",
  "level": "A1",
  "register": "polite",
  "source_type": "derived_from_source",
  "source_sentence_ref": "video:79Pwq7MTUPE:v_009",
  "dictionary_atom_refs": [
    "ko:n:오늘",
    "ko:p:은",
    "ko:n:토요일",
    "ko:cop:이다"
  ],
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "topic_refs": ["topic.time.weekday"],
  "quality_flags": {
    "segmentation_ready": true,
    "translation_reviewed": true,
    "tts_ready": true
  }
}
```

### Required Fields

- `id`
- `target_lang`
- `surface_ko`
- `level`
- `source_type`

### Strongly Recommended

- `translation_zh_tw`
- `dictionary_atom_refs`
- `knowledge_refs`
- `topic_refs`
- `quality_flags`

---

## 2. Optional `frame_projection`

只有當句子可以穩定投影回某個教學框架時才加。

```json
{
  "frame_projection": {
    "pattern_frame_ref": "kp.time.today_is_weekday",
    "slot_projection": [
      {
        "slot_id": "weekday",
        "slot_surface": "토요일",
        "slot_semantic_type": "weekday",
        "slot_refs": ["kv.time.weekday.saturday"]
      }
    ]
  }
}
```

### Rule

- 沒有穩定 slot 的句子：`frame_projection` 直接省略
- 可回投成某 frame 的句子：補 `pattern_frame_ref + slot_projection`

所以 `오늘은 토요일이에요.` 就是：

- 一句正常例句
- 同時也是 `오늘은 N요일이에요` 的一個 slotized instance

---

## Slot vs Non-Slot Decision

## A. Plain sentence

例：

```json
{
  "id": "ex.ko.greeting.annyeong.v1",
  "surface_ko": "안녕하세요.",
  "translation_zh_tw": "您好。",
  "knowledge_refs": ["kp.daily.greeting.annyeong"]
}
```

這種句子：

- 沒有必要做 slot
- 就是固定塊

### Recommendation

只存 base sentence，不要硬補空的 slot structure。

## B. Slot-capable sentence

例：

```json
{
  "id": "ex.ko.time.today_is_saturday.v1",
  "surface_ko": "오늘은 토요일이에요.",
  "translation_zh_tw": "今天是星期六。",
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "frame_projection": {
    "pattern_frame_ref": "kp.time.today_is_weekday",
    "slot_projection": [
      {
        "slot_id": "weekday",
        "slot_surface": "토요일",
        "slot_semantic_type": "weekday",
        "slot_refs": ["kv.time.weekday.saturday"]
      }
    ]
  }
}
```

這種句子：

- 本質仍是 sentence
- 只是額外提供 frame-aware metadata

### Recommendation

共用 base schema，加 optional projection。不要拆成另一種 `templated_sentence` 主類。

---

## Boundary With `pattern_frame`

### `pattern_frame` owns

- canonical frame
- slot definitions
- semantic slot constraints
- teaching explanation
- transform/drill metadata

### `example_sentence` owns

- concrete surface sentence
- translation
- source traceability
- segmentation / atom refs
- whether this instance can be projected into a frame

### Anti-pattern

不要把這種句子：

- `오늘은 토요일이에요.`

直接存成 pattern 的主體，只因為它有 slot potential。

因為它同時可能：

- 來自真 source sentence
- 被 topic detail 引用
- 被 knowledge detail 引用
- 被 shadowing/typing 使用

這些都比較像 sentence asset，不是 frame asset。

---

## Extraction Example

### Before

```json
{
  "id": "kp.time.today_is_weekday",
  "surface": "오늘은 N요일이에요",
  "summary_zh_tw": "最直接的星期表達句型，適合做主題頁第一個高亮框架。",
  "topic_refs": ["topic.time.weekday"],
  "example_bank": [
    {
      "ko": "오늘은 토요일이에요.",
      "zh_tw": "今天是星期六。",
      "sentence_ref": "video:79Pwq7MTUPE:v_009"
    }
  ]
}
```

### After

`knowledge item`

```json
{
  "id": "kp.time.today_is_weekday",
  "surface": "오늘은 N요일이에요",
  "summary_zh_tw": "最直接的星期表達句型，適合做主題頁第一個高亮框架。",
  "topic_refs": ["topic.time.weekday"],
  "example_sentence_refs": ["ex.ko.time.today_is_saturday.v1"]
}
```

`example sentence`

```json
{
  "id": "ex.ko.time.today_is_saturday.v1",
  "surface_ko": "오늘은 토요일이에요.",
  "translation_zh_tw": "今天是星期六。",
  "source_sentence_ref": "video:79Pwq7MTUPE:v_009",
  "knowledge_refs": ["kp.time.today_is_weekday"],
  "topic_refs": ["topic.time.weekday"],
  "frame_projection": {
    "pattern_frame_ref": "kp.time.today_is_weekday",
    "slot_projection": [
      {
        "slot_id": "weekday",
        "slot_surface": "토요일",
        "slot_semantic_type": "weekday",
        "slot_refs": ["kv.time.weekday.saturday"]
      }
    ]
  }
}
```

---

## Validation Rules

### Blocker

- `id` missing
- `surface_ko` missing
- `frame_projection.pattern_frame_ref` exists but target frame does not exist
- `slot_projection.slot_id` not declared by referenced frame

### Warning

- no translation
- no `dictionary_atom_refs`
- slot-capable sentence missing `slot_refs`
- one sentence linked to too many unrelated knowledge items without priority signal

---

## Migration Guidance

### Immediate

- 把現有 `knowledge_item.example_bank` 中可重用句子抽出
- knowledge item 改存 `example_sentence_refs`
- 保留 `summary/explanation/usage_notes` 在 knowledge item

### Short Term

- 先只要求 `dictionary_atom_refs`
- `frame_projection` 先手工補高價值句子
- 不要求每句都 slotize

### Later

- 加入排序權重，例如 `canonical`, `beginner_safe`, `high_frequency`
- 加入多語系 i18n pack
- 允許同一句對應多個 frame projection，但要有 primary/secondary priority

---

## Final Recommendation

你的例子 `오늘은 토요일이에요.` 很適合做成：

- 一筆 `example_sentence`
- 可選的 `frame_projection`
- 對應 frame `오늘은 N요일이에요`

所以我的建議是：

- `slot` 與 `non-slot` 句子共用同一個 sentence schema
- 只在有教學價值、而且 slot 邊界穩定時補 `frame_projection`
- 不要拆兩套主 schema

這樣最穩，也最容易和現有 `sentence / knowledge / pattern / topic` graph 接起來。

---

## Related Docs

- [ARCHITECTURE_IDEA_REVIEW_2026-04-07.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/ARCHITECTURE_IDEA_REVIEW_2026-04-07.md)
- [LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md)
- [LEARNING_LIBRARY_ARTIFACT_SPEC_V0.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/LEARNING_LIBRARY_ARTIFACT_SPEC_V0.md)
- [TLG_022_PATTERN_INDEX_CONTRACT_SPEC.md](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TLG_022_PATTERN_INDEX_CONTRACT_SPEC.md)
