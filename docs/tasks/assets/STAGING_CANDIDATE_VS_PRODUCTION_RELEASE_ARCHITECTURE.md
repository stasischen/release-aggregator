# Staging Candidate vs Production Release Architecture

## Goal

把目前「pipeline 只要掃到 `core` 的 `dialogue` / `video` 就把全部內容丟進 production」的模式，改成可控的分層發版架構。

核心目標是：

- staging 先收全量可驗證內容
- production 只收已明確 allowlist 的 lesson / unit
- release 決策不再綁 raw source 全掃描

## Problem Statement

目前 production 產物主要反映的是全量 source 掃描與同步。

具體表現：

- `manifest.json` 與 `lesson_catalog.json` 仍然以大量 source / lesson 列表直接描述 production 可用內容
- `dialogue` / `video` 一旦進入 `core` 並被 pipeline 掃到，就很容易被同步到 production 資產
- production 邊界沒有先經過 lesson / unit 級別的 release gate

結果是：

- staging recovery 和 production publish 混在一起
- 內容可見不等於可發佈
- unit refactor 還沒完成時，source 就先被全量放進 production

## Core Decision

採用以下固定決策：

```text
build everything to staging
publish only allowlisted lessons to production
```

含義如下：

- 所有可 intake 的內容先進 staging
- production 不再直接吃 raw source 全量掃描結果
- release 必須經過 lesson / unit allowlist
- staging_only 內容可以存在，但不代表可發版

## Four-Layer Architecture

### 1. Candidate Build Layer

職責：

- 從 `content-ko` / source truth 產出 canonical candidate artifacts
- 做 normalization、linking、validation、readiness metadata 標記
- 允許 `dialogue` / `video` / `article` 等內容全部先進 staging candidate

這一層只負責「可建置」，不負責「可發佈」。

### 2. Staging Catalog

職責：

- 收錄所有 staging candidate
- 讓內容可見、可盤點、可抽樣驗證
- 保留 `staging_only`、`readiness_flag`、`segmentation_status` 等狀態

這一層回答的是：

- 內容是否已可 intake
- 內容是否已可驗證
- 內容是否已達發版條件

但它仍然不是 production gate。

### 3. Release Manifest

職責：

- 定義哪些 lesson / unit 可以進 production
- 只列已通過驗證的 allowlisted lessons
- 作為 production assembler 的唯一輸入來源

這一層是 release 決策層，不是 raw source inventory。

### 4. Production Assembler

職責：

- 只讀 release manifest
- 把 manifest 指定的 lessons / units 打包成 production 資產
- 不直接掃全量 `core/dialogue` 或 `core/video`

這一層負責最後輸出，不負責決定誰能上線。

## Why Gate On Lesson / Unit, Not Raw Source

production gating 必須綁在 lesson / unit，而不是 raw source，原因很直接：

1. 使用者實際消費的是課，不是 source file。
2. 一課可能對應多個 source，release decision 需要對齊教學單位。
3. raw source 只代表材料，lesson / unit 才代表經過課程設計後的可發佈產品。
4. unit refactor 的進度本來就是逐課推進，gate 綁 lesson 才能和重構節奏一致。
5. source 級 gating 會把 staging recovery、candidate build、production publish 混成一條線，難以控制。

結論：

- source 只適合做建置與驗證
- lesson / unit 才適合做 production release gate

## Release Manifest Contract

建議最小欄位如下：

```json
{
  "unit_id": "a1_unit_01_intro_identity",
  "lesson_id": "ko_l1_dialogue_a1_01",
  "release_status": "production",
  "content_type": "dialogue",
  "course_type": "lesson",
  "source_refs": [
    "src.ko.dialogue.a1_01"
  ],
  "contract_version": "core+i18n-vNext-1",
  "viewer_verified": true,
  "qa_gate_passed": true,
  "staging_only": false
}
```

建議欄位說明：

- `unit_id`
  - 課程單元 id，作為最上層教學組織單位
- `lesson_id`
  - 前端與 manifest 主要追蹤 id
- `release_status`
  - 例如 `draft`, `staging_only`, `production`
- `content_type`
  - 例如 `dialogue`, `video`, `article`
- `course_type`
  - 例如 `lesson`, `bonus`, `supplemental`
- `source_refs`
  - 對應的 raw source ids
- `contract_version`
  - 發版所依據的內容 contract 版本
- `viewer_verified`
  - 是否已通過 viewer / frontend 驗證
- `qa_gate_passed`
  - 是否已通過 QA gate
- `staging_only`
  - 是否只允許存在於 staging

可選補充欄位：

- `level`
- `topic_refs`
- `knowledge_refs`
- `prerequisite_unit_ids`
- `published_at`
- `notes`

## Relationship To Current Mainline

這個架構必須和目前主線對齊，而不是另起一條平行線。

對齊方式如下：

- staging recovery 照常先做
- `dialogue` / `video` 先進 staging catalog
- unit refactor 完成一課，就把該課加入 release manifest
- production assembler 只吃 manifest 中已 allowlisted 的課

這表示：

- 內容先可見
- 再可驗證
- 最後才可發佈

## Non-Goals

本文件不處理：

- `B1+ segmentation` 規則本身
- `knowledge lab` 的 enrichment / expansion
- `CONTENT_V5_MIGRATION_L0`
- 單一 source 的 taxonomy 重整
- frontend UI 樣式調整

## Immediate Recommendation

下一步應先做 `release manifest gate`，不要直接再掃全量 source 進 production。

最小落地順序：

1. 定義 release manifest schema
2. production assembler 改讀 manifest
3. staging catalog 只做 candidate 收錄
4. 新增 lesson / unit allowlist 機制
5. unit refactor 完成一課，就補一課進 manifest

## Summary

這個架構的本質是把「能建」和「能發」分開。

- `candidate build` 解決內容進 staging
- `staging catalog` 解決內容可見與可驗證
- `release manifest` 解決發版決策
- `production assembler` 解決最終輸出

如果 production 還在直接掃全量 `dialogue` / `video`，就代表 release gate 仍然缺失。
