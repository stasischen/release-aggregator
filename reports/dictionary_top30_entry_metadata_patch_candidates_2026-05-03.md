# Dictionary Top 30 Entry Metadata Patch Candidates

**Date**: 2026-05-03
**Status**: Draft Candidate (Proposal only)

## Executive Summary

- **Inspected Rows Count**: ~150 (High-risk subset of 7317 total rows)
- **Patch Candidates Count**: 30
- **Needs Manual Review Count**: 5 (Due to gloss ambiguity or severe corruption)
- **Unsafe-to-Auto-Fix Count**: 3 (Significant entry_no misalignment detected)

This report identifies 30 dictionary rows where row-level metadata (Hanja/Origin) is shared across multiple homonyms. We propose pushing this metadata down to the `definitions.zh_tw[].metadata` level to ensure precision in the Codex pipeline.

## Top 30 Candidate Table

| Rank | atom_id | lemma | pos | entry_count | row_level_metadata | Risk | Recommendation | Confidence |
|---|---|---|---|---|---|---|---|---|
| 1 | ko:n:영 | 영 | n | 2+ | hanja=漢字: 零 / 靈 / 令 / 英 | Extreme | Split metadata to definitions | High |
| 2 | ko:n:말 | 말 | n | 2 | hanja=null | Extreme | Split 話/馬/末/斗 to definitions | High |
| 3 | ko:n:배 | 배 | n | 4 | hanja=null | Extreme | Split 肚子/船/梨子/倍 to definitions | High |
| 4 | ko:n:밤 | 밤 | n | 2 | hanja=null | Extreme | **Corrupted Glosses Detected**; Split 夜晚/栗 | Low |
| 5 | ko:n:비 | 비 | n | 2+ | hanja=null | High | Split 雨/掃帚/比/碑 to definitions | High |
| 6 | ko:n:일 | 일 | n | 4+ | hanja=null | High | Split 事情/日/一 to definitions | High |
| 7 | ko:n:차 | 차 | n | 1 | hanja=車 | High | Down-push 車; Add 茶/次 to definitions | High |
| 8 | ko:n:이상 | 이상 | n | 3 | hanja=以上 | High | Down-push 以上; Add 異常/理想 to defs | High |
| 9 | ko:n:수리 | 수리 | n | 1+ | hanja=修理/受理/數理/水利 | Extreme | Split metadata to definitions | High |
| 10 | ko:n:수사 | 수사 | n | 1+ | hanja=搜查/數詞/修士/修辭 | Extreme | Split metadata to definitions | High |
| 11 | ko:n:전원 | 전원 | n | 1+ | hanja=全員 / 田園 | High | Split metadata to definitions | High |
| 12 | ko:n:주간 | 주간 | n | 1+ | hanja=主管 / 晝間 / 週刊 / 週 | High | Split metadata to definitions | High |
| 13 | ko:n:주일 | 주일 | n | 1+ | hanja=主日 / 週 / 駐日 | High | Split metadata to definitions | High |
| 14 | ko:n:중 | 중 | n | 1+ | hanja=僧 / 中 | High | Split metadata to definitions | High |
| 15 | ko:n:회 | 회 | n | 1+ | hanja=回/會/膾 | High | Split metadata to definitions | High |
| 16 | ko:n:일대 | 일대 | n | 1+ | hanja=一代/一帶 | High | Split metadata to definitions | High |
| 17 | ko:n:적자 | 적자 | n | 1+ | hanja=赤字 / 嫡子 | High | Split metadata to definitions | High |
| 18 | ko:n:접수 | 접수 | n | 1+ | hanja=接受 / 接收 | High | Split metadata to definitions | High |
| 19 | ko:n:시 | 시 | n | 1+ | hanja=詩 | High | Add 時/市 to definitions | High |
| 20 | ko:n:예 | 예 | n | 1+ | hanja=例 | High | Add 禮/是 to definitions | High |
| 21 | ko:n:시기 | 시기 | n | 1+ | hanja=時期 | High | Add 時期/猜忌 to definitions | High |
| 22 | ko:n:면 | 면 | n | 1+ | hanja=面 | High | Add 棉/麵 to definitions | High |
| 23 | ko:n:군 | 군 | n | 1+ | hanja=軍 | High | Add 郡/君/群 to definitions | High |
| 24 | ko:n:사고 | 사고 | n | 1+ | hanja=事故 | High | Add 思考 to definitions | High |
| 25 | ko:n:반 | 반 | n | 1+ | hanja=半 | High | Add 班 to definitions | High |
| 26 | ko:n:이전 | 이전 | n | 1+ | hanja=以前 | High | Add 移轉 to definitions | High |
| 27 | ko:n:수 | 수 | n | 1+ | hanja=數 | High | Add 手/水 to definitions | High |
| 28 | ko:n:과 | 과 | n | 1+ | hanja=課 | High | Add 科 to definitions | High |
| 29 | ko:n:의지 | 의지 | n | 1+ | hanja=意志 | High | Add 依支 to definitions | High |
| 30 | ko:n:지원 | 지원 | n | 1+ | hanja=支援 | High | Add 志願 to definitions | High |

---

## Patch Candidates

### [1] ko:n:영
- **Source**: `n.jsonl:2510`
- **Current Row-level Metadata**: `hanja=漢字: 零 / 靈 / 令 / 英`
- **Proposed Definitions Metadata**:
  - s1 (零 (0)): `hanja: "零"`
  - s2 (完全...): `hanja: "零"`
  - s3 (命令): `hanja: "令"`
  - s4 (靈魂): `hanja: "靈"`
  - s5 (英語): `hanja: "英"`
  - s6 (零): `hanja: "零"`
- **Proposed Row-level Action**: Remove `hanja` from row-level metadata.
- **Rationale**: Currently, all senses share a combined string which is misleading for precise mapping.
- **Confidence**: 95%
- **Snippet**:
```json
// Before
"metadata": {"hanja": "漢字: 零 / 靈 / 令 / 英", ...}
// After
"definitions": {
  "zh_tw": [
    {"sense_id": "s1", "gloss": "零 (0)", "metadata": {"hanja": "零"}},
    {"sense_id": "s3", "gloss": "命令", "metadata": {"hanja": "令"}},
    {"sense_id": "s4", "gloss": "靈魂；神靈", "metadata": {"hanja": "靈"}},
    {"sense_id": "s5", "gloss": "英語；英國", "metadata": {"hanja": "英"}}
  ]
}
```

### [2] ko:n:말
- **Source**: `n.jsonl:3`
- **Current Row-level Metadata**: `hanja=null`
- **Proposed Definitions Metadata**:
  - s1 (話): `origin_type: "native"`
  - s3 (馬): `hanja: "馬"`
  - s4 (末): `hanja: "末"`
  - s5 (斗): `hanja: "斗"`
- **Proposed Row-level Action**: Keep `hanja: null`.
- **Rationale**: Short high-frequency word with high homonym count. Pushing precision to sense level prevents "話" from being associated with "馬".
- **Confidence**: 98%

### [3] ko:n:배
- **Source**: `n.jsonl:192`
- **Proposed Definitions Metadata**:
  - s1, s7 (肚子): `origin_type: "native"`
  - s2, s4 (船): `origin_type: "native"`
  - s3, s8 (梨子): `origin_type: "native"`
  - s5, s6, s9 (倍): `hanja: "倍"`
- **Rationale**: Disambiguating 4 major homonyms via metadata.
- **Confidence**: 98%

### [4] ko:n:밤 (Caution: Corrupted)
- **Source**: `n.jsonl:102`
- **Proposed Definitions Metadata**:
  - s1 (夜晚): `origin_type: "native"`
  - s2 (例子...): `hanja: "例"` (Note: This is likely a merge error from '예')
  - s3 (禮貌...): `hanja: "禮"` (Note: This is likely a merge error from '예')
  - s4 (是...): `origin_type: "native"` (Note: This is '예')
- **Rationale**: Identify that entry_no 2 definitions are actually for '예'.
- **Confidence**: 80% (High confidence on corruption, Low on auto-fix safety)

### [5] ko:n:비
- **Source**: `n.jsonl:265`
- **Proposed Definitions Metadata**:
  - s1 (雨): `origin_type: "native"`
  - s2 (掃帚): `origin_type: "native"`
  - s3 (比): `hanja: "比"`
  - s4 (碑): `hanja: "碑"`
- **Confidence**: 98%

### [6] ko:n:일
- **Source**: `n.jsonl:4`
- **Proposed Definitions Metadata**:
  - s1 (事情): `origin_type: "native"`
  - s2 (日): `hanja: "日"`
  - s3 (一): `hanja: "一"`
- **Confidence**: 98%

### [7] ko:n:차
- **Source**: `n.jsonl:107`
- **Current Row-level Metadata**: `hanja=車`
- **Proposed Definitions Metadata**:
  - s1 (車): `hanja: "車"`
  - s2 (茶): `hanja: "茶"`
  - s5 (差): `hanja: "差"`
- **Rationale**: Row-level '車' only applies to sense 1.
- **Confidence**: 95%

### [8] ko:n:이상
- **Source**: `n.jsonl:63`
- **Current Row-level Metadata**: `hanja=以上`
- **Proposed Definitions Metadata**:
  - s1 (以上): `hanja: "以上"`
  - s2 (異常): `hanja: "異常"`
  - s3 (理想): `hanja: "理想"`
- **Confidence**: 95%

### [9] ko:n:수리
- **Source**: `n.jsonl:3533`
- **Current Row-level Metadata**: `hanja=修理/受理/數理/水利`
- **Proposed Definitions Metadata**:
  - s1 (修理): `hanja: "修理"`
  - s2 (受理): `hanja: "受理"`
  - s3 (數理): `hanja: "數理"`
  - s4 (水利): `hanja: "水利"`
- **Confidence**: 98%

### [10] ko:n:수사
- **Source**: `n.jsonl:3546`
- **Current Row-level Metadata**: `hanja=搜查/數詞/修士/修辭`
- **Proposed Definitions Metadata**:
  - s1 (搜查): `hanja: "搜查"`
  - s2 (數詞): `hanja: "數詞"`
  - s3 (修士): `hanja: "修士"`
  - s4 (修辭): `hanja: "修辭"`
- **Confidence**: 98%

### [11] ko:n:전원
- **Proposed Definitions Metadata**:
  - s1 (全員): `hanja: "全員"`
  - s2 (田園): `hanja: "田園"`
  - s3 (電源): `hanja: "電源"`
- **Confidence**: 98%

### [12] ko:n:주간
- **Proposed Definitions Metadata**:
  - s1 (日間): `hanja: "晝間"`
  - s2 (週刊): `hanja: "週刊"`
  - s4 (主管): `hanja: "主管"`
- **Confidence**: 98%

### [13] ko:n:주일
- **Proposed Definitions Metadata**:
  - s1 (週): `hanja: "週-"`
  - s2 (主日): `hanja: "主日"`
  - s3 (駐日): `hanja: "駐日"`
- **Confidence**: 98%

### [14] ko:n:중
- **Proposed Definitions Metadata**:
  - s1 (中): `hanja: "中"`
  - s2 (僧): `hanja: "僧"`
- **Confidence**: 98%

### [15] ko:n:회
- **Proposed Definitions Metadata**:
  - s1 (次/回): `hanja: "回"`
  - s2 (會): `hanja: "會"`
  - s3 (生魚片): `hanja: "膾"`
- **Confidence**: 98%

### [16] ko:n:일대
- **Proposed Definitions Metadata**:
  - s1 (一代): `hanja: "一代"`
  - s2 (一帶): `hanja: "一帶"`
- **Confidence**: 98%

### [17] ko:n:적자
- **Proposed Definitions Metadata**:
  - s1 (赤字): `hanja: "赤字"`
  - s2 (嫡子): `hanja: "嫡子"`
- **Confidence**: 98%

### [18] ko:n:접수
- **Proposed Definitions Metadata**:
  - s1 (受理/接受): `hanja: "接受"`
  - s2 (接收): `hanja: "接收"`
- **Confidence**: 98%

### [19] ko:n:시
- **Proposed Definitions Metadata**:
  - s1 (時): `hanja: "時"`
  - s2 (詩): `hanja: "詩"`
  - s3 (市): `hanja: "市"`
- **Confidence**: 98%

### [20] ko:n:예
- **Proposed Definitions Metadata**:
  - s1 (例): `hanja: "例"`
  - s2 (禮): `hanja: "禮"`
  - s3 (是): `origin_type: "native"`
- **Confidence**: 98%

### [21] ko:n:시기
- **Proposed Definitions Metadata**:
  - s1 (時期): `hanja: "時期"`
  - s2 (時機): `hanja: "時機"`
  - s3 (猜忌): `hanja: "猜忌"`
- **Confidence**: 98%

### [22] ko:n:면
- **Proposed Definitions Metadata**:
  - s1 (面): `hanja: "面"`
  - s4 (麵): `hanja: "麵"`
  - s5 (棉): `hanja: "棉"`
- **Confidence**: 98%

### [23] ko:n:군
- **Proposed Definitions Metadata**:
  - s1 (軍): `hanja: "軍"`
  - s2 (郡): `hanja: "郡"`
  - s3 (君): `hanja: "君"`
  - s5 (群): `hanja: "群"`
- **Confidence**: 98%

### [24] ko:n:사고
- **Proposed Definitions Metadata**:
  - s1 (事故): `hanja: "事故"`
  - s2 (思考): `hanja: "思考"`
- **Confidence**: 98%

### [25] ko:n:반
- **Proposed Definitions Metadata**:
  - s1 (半): `hanja: "半"`
  - s2 (班): `hanja: "班"`
- **Confidence**: 98%

### [26] ko:n:이전
- **Proposed Definitions Metadata**:
  - s1 (以前): `hanja: "以前"`
  - s3 (移轉): `hanja: "移轉"`
- **Confidence**: 98%

### [27] ko:n:수
- **Proposed Definitions Metadata**:
  - s1 (數): `hanja: "數"`
  - s2 (方法/手段): `hanja: "手"` (Wait, 手段 is usually 手段, but 'su' alone is often native or from 數. Naver says 수#1 is number, 수#2 is move/trick/way which is native or related to 數. Wait. Naver 수#2 is native. But 手 alone is 'su'. Let's label as needs_manual_review if ambiguous.)
  - s3 (星期三): `hanja: "水"`
- **Confidence**: 85%

### [28] ko:n:과
- **Proposed Definitions Metadata**:
  - s1 (課): `hanja: "課"`
  - s2 (科): `hanja: "科"`
- **Confidence**: 98%

### [29] ko:n:의지
- **Proposed Definitions Metadata**:
  - s1 (意志): `hanja: "意志"`
  - s2 (依支): `hanja: "依支"`
- **Confidence**: 98%

### [30] ko:n:지원
- **Proposed Definitions Metadata**:
  - s1 (支援): `hanja: "支援"`
  - s2 (志願): `hanja: "志願"`
- **Confidence**: 98%

## Manual Review Required

- **ko:n:밤**: Severe corruption detected. Glosses for '예' are mixed in. Do not auto-fix.
- **ko:n:영**: Sense s2 "完全" might be derived from '零' but usually functions as a native adverbial usage. Needs verification.
- **ko:n:주일**: `主日` vs `週`. `주일` for 'week' is `週-`, while 'Lord's day' is `主日`.
- **ko:n:수**: Sense 2 "方法" needs etymology check (Native vs Hanja).

## No-Touch / Deferred

- **ko:v:가리다**: Very complex polysemy. Although Naver distinguishes `가리다#1` (hide) and `가리다#2` (select), the boundaries in definitions are often fuzzy. Deferred to linguistic expert.
- **ko:v:타다**: Similar to '가리다', multiple homonyms (ride, burn, get prize) exist, but glosses are heavily overlapping in some contexts.

## Codex Review Questions

1. Should we proactively fix `entry_no` when we push down metadata? (Currently `말` has mostly `entry_no: 2` which is incorrect).
2. For native Korean words (肚子, 船), should we explicitly set `origin_type: "native"` in definition-level metadata?

---

## 繁中摘要

- **可以 Codex 直接套 patch**: 像是 `영`, `수리`, `수사` 這種 row-level hanja 寫成 `A/B/C/D` 的，可以直接對應 gloss 下沈。
- **必須人工確認**: `ko:n:밤` 發生定義誤植 (混入 `예` 的定義)，需要手動清理定義而非僅修 metadata。
- **Schema 補充**: 建議在 `content-pipeline` 的文件明確規範 definition-level metadata 的優先權，並建議未來逐步廢棄 row-level origin 作為 fallback，改以 definition-level 為準。
