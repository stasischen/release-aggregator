# Pattern Library Sync Guide

## Files

- Canonical data: `ko_survival_pattern_library_v1.json`
- Human-readable doc: `ko_survival_pattern_library_v1.md`
- Codec script: `/Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py`

## Convert JSON -> Markdown

```bash
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py json-to-md \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json \
  --output /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.md
```

## Convert Markdown -> JSON

```bash
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py md-to-json \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.md \
  --output /Users/ywchen/Dev/lingo/release-aggregator/staging/ko_survival_pattern_library_v1.roundtrip.json
```

## Round-Trip Check

```bash
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py md-to-json \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.md \
  --output /Users/ywchen/Dev/lingo/release-aggregator/staging/ko_survival_pattern_library_v1.roundtrip.json

jq -S . /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json > /Users/ywchen/Dev/lingo/release-aggregator/staging/orig.sorted.json
jq -S . /Users/ywchen/Dev/lingo/release-aggregator/staging/ko_survival_pattern_library_v1.roundtrip.json > /Users/ywchen/Dev/lingo/release-aggregator/staging/rt.sorted.json
diff -u /Users/ywchen/Dev/lingo/release-aggregator/staging/orig.sorted.json /Users/ywchen/Dev/lingo/release-aggregator/staging/rt.sorted.json
```
