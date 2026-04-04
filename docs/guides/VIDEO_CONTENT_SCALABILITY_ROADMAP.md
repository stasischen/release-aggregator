# Video Content Scalability Roadmap (影片內容擴展路線圖)

本文檔記錄了 Lingo 影片學習模組從初期到成熟期的技術演進規劃，旨在應對影片量從數十部增加到數千部時的效能與管理挑戰。

---

## 階段一：索引分片 (Shard Indexing)
**目標範圍**: ~100-200 部影片
**核心策略**: 避免單一大型索引檔案引起的載入延時。

- **分片產生**: 由 `content-pipeline` 在建置時根據類別自動產生 `index_vlog.json`, `index_music.json` 等小檔案。
- **按需載入 (On-demand Loading)**: 前端 App 僅在切換至對應類別或點擊「See all」時，才從 `assets/` 請求對應的分片 JSON。
- **輕量級首頁**: 首頁只載入每個類別前 5 部影片的精簡索引 (Pre-warmed Hero Index)。

---

## 階段二：建立專屬 Content Registry
**目標範圍**: ~500+ 部影片
**核心策略**: 將影片管理與前端程式碼解耦，轉向內容驅動（Content-driven）。

- **自動化 Metadata 生成**: 強化 `batch_fetch_yt.py`，自動從 YouTube API 抓取字數、詞彙難度分佈 (Hapax legomena count) 等統計資訊，輔助判定 CEFR/TOPIK 分級。
- **內容審核台 (Content Staging)**: 影片導入不再直接進入 `Production`。所有新影片先存入 `content-staging`，通過流水線驗證（字體規範、語速檢測、標點符號自動校正）後才准予發佈。
- **資產編號系統**: 導入專屬的 `Lingo Video ID` 與版本控制，確保 I18N 翻譯能穩定追蹤來源異動。

---

## 階段三：雲端檢索與 API 化
**目標範圍**: 1000+ 部影片
**核心策略**: 當靜態資產 (Static Assets) 無法滿足搜尋與個性化需求時，轉向服務化。

- **雲端資料庫**: 將所有影片 Metadata 存放在 Firestore 或類似的雲端 NoSQL 資料庫。
- **動態搜尋 API**: 支援關鍵字搜尋、難度過濾、主題組合篩選。
- **智慧推薦系統**: 根據使用者目前的詞彙庫 (Mastery Vocabulary) 覆蓋率，自動推薦其能聽懂 80% 以上內容的影片。

---

## 當前執行狀態 (Active Status)
- [x] **2026-04-04**: 完成分級與類別標準化 (v1-v6 / CEFR)。
- [/] **2026-04-04**: 實作「階段一」的自動化索引生成邏輯（Ingestion Metadata Enrichment）。
