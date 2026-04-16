# KO Topic Family Mockup: Time

## Purpose
This mockup defines how topic families should sit above vocabulary, grammar, patterns, sentences, and videos.

The goal is to support topic-driven discovery such as:
- 星期幾
- 月份
- 相對日期
- 幾點 / 時刻

without collapsing them into a flat vocabulary list.

## Files
- JSON mockup: [ko_topic_family_time_mockup.json](/Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/ko_topic_family_time_mockup.json)

## Key Rule
Keep these layers separate:
- `topic`: learning theme
- `vocab_item`: word
- `grammar_point`: rule / ending / structure
- `pattern_frame`: reusable sentence frame
- `sentence`: example carrier
- `video`: learning entry point

## Example
For `오늘은 토요일이에요.`:
- topic refs:
  - `topic.time.weekday`
- pattern refs:
  - `kp.time.today_is_weekday`
- grammar refs:
  - `kg.time.topic_particle_eunneun`
- vocab refs:
  - `kv.time.relative_day.today`
  - `kv.time.weekday.saturday`

This keeps `星期幾` as a reusable topic, rather than treating `토요일` as the whole lesson.

## Suggested UI Entry
1. Topic family card: `時間`
2. Child topics:
- 星期幾
- 月份
- 相對日期
- 幾點 / 時刻

Each child topic page should have:
- hero summary
- highlighted patterns
- core vocabulary grid
- related sentences
- related videos

## Why This Matters
This structure scales cleanly to:
- 顏色
- 數字
- 月份
- 日期
- 天氣
- 交通

It also supports reverse lookup later:
- topic -> which videos teach it
- topic -> which patterns belong to it
- topic -> which vocabulary is core vs optional
