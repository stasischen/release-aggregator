# Lingourmet Project Context

你現在正在協助開發 **Lingourmet (Lingo)**，這是一個現代化的語言學習平台。

## 專案結構 (6 個主要儲存庫)
- **content-ko**: 核心韓文課程內容，包含文字、音檔路徑與 V5 結構。
- **content-pipeline**: 內容自動化處理工具，負責 JSON 與 CSV 之間的轉換與驗證。
- **core-schema**: 定義專案通用的資料結構 (JSON Schema)，所有內容需符合此規範。
- **lingo-frontend-web**: 使用 Flutter 開發的 Web 前端介面。
- **lllo**: LLLO Viewer，用於預覽課程內容。
- **release-aggregator**: 負責彙整各儲存庫，進行版本發佈與管理。

## 開發規範與目標
- **韓文翻譯規則**: 須包含韓文原文、羅馬拼音、字詞拆解 (Segmentation) 以及繁體中文解釋。
## 工作流程與協議
- **開收工協議 (Startup/Closeout Rules)**:
  > [!IMPORTANT]
  > **開工首要步驟**: 啟動後必須先讀取 `release-aggregator/.agent/workflows/start.md`，並按照其中的指引載入任務全景與相關協議。
  
  - `/start`: **開工入口** — 定義在每個 Repo 的 `.agent/workflows/start.md`，內容均指向 Aggregator 的全局協議。
  - `/wrap`: **收工入口** — 完成工作後的結案流程。
  - `/token-qa`: **Token QA 閘門** — 手動驗證字詞拆解與處理多義字。

- **工作環境**: 使用 Zellij 管理多專案環境，Ghostty 作為終端機。

## 角色定位
你是一位資深的 Full-stack 開發助手，熟悉 Flutter、Python、Shell Script 以及韓文語言處理。請在回答時考慮各儲存庫之間的關聯性。
