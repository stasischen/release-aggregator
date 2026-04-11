# Verification Note: Bucket C1 Merge Targets (V1)

## Overview
本文件記錄 `kg-mig-010` Bucket C1 中 3 個 `duplicate_existing` 項目在 `content-ko` 銀行中的存在性驗證結果。

## Findings

### Item 1: `빵하고 우유를 샀어요.`
- **Status**: `verified_unique`
- **Canonical ID**: `ex.ko.grammar.particle.and_with_hago.bread_and_milk.v1`
- **File Path**: `content/core/learning_library/example_sentence/ex.ko.grammar.particle.and_with_hago.bread_and_milk.v1.json`
- **Verdict**: Safe for direct reference update.

### Item 2: `화장실이 어디예요?`
- **Status**: `verified_unique`
- **Canonical ID**: `ex.ko.pattern.facility.toilet_query.v1`
- **File Path**: `content/core/learning_library/example_sentence/ex.ko.pattern.facility.toilet_query.v1.json`
- **Verdict**: Safe for direct reference update.

### Item 3: `여기 앉아도 돼요?`
- **Status**: **`ambiguous_existing_duplicate`**
- **Collision Candidates**:
  1. `ex.ko.grammar.permission.sit_here.v1`
     - Path: `content/core/learning_library/example_sentence/ex.ko.grammar.permission.sit_here.v1.json`
  2. `ex.ko.pattern.social_basic.sit_here.v1`
     - Path: `content/core/learning_library/example_sentence/ex.ko.pattern.social_basic.sit_here.v1.json`
- **Verdict**: **BLOCKER**. 既存銀行中已存在同表面文字但不同路徑與 ID 的重複項。在未清理銀行重複項並指定唯一目標前，不可執行 Decoupling 寫入。

## Implementation Impact
此次驗證確認了 C1 具備 2 筆安全合併項。針對「這裡可以坐嗎？」的歧義，建議下一階段 implementation 先跳過 (Skip/Pause) 該項的寫入，直到 `content-ko` 重複項被手動合併或清理。
