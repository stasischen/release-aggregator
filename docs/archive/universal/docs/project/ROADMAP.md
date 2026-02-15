# Project Roadmap & Implementation Guide / 專案路線圖與開發指南

This document defines the strategic path for Lingourmet Universal, detailing the transition from a purely local experience to a cloud-synced, multi-platform language learning suite.
本文件定義了 Lingourmet Universal 的策略路徑，詳述了從純本地體驗轉向雲端同步、多平台語言學習套件的過程。

## 🧭 Core Vision / 核心願景
To provide a seamless, "offline-first" learning experience that syncs progress across devices while maintaining high performance and data privacy.
提供無縫的「離線優先」學習體驗，在保持高效能和數據隱私的同時，實現跨設備進度同步。

---

## 🏗️ Phase 1: Architectural Foundation (Technical Debt) / 第一階段：架構基礎（技術債清理）
*Standardize the app to support complex state and external data.*
*標準化 App 架構以支援複雜狀態與外部數據。*

### 1.1 Centralized Authentication Layer / 集中化身份驗證層
- **Implement `AuthService`**: Generic interface for auth status.
- **實作 `AuthService`**：用於處理身份驗證狀態的通用介面。
- **State Management**: Create `authNotifierProvider` to handle `Initial`, `Unauthenticated`, `Authenticated(User)`, and `Error` states.
- **狀態管理**：建立 `authNotifierProvider` 來處理 `初始`、`未驗證`、`已驗證(使用者)` 及 `錯誤` 狀態。
- **Route Guarding**: Integrate with `GoRouter` to redirect unauthenticated users if necessary.
- **路由守衛**：與 `GoRouter` 整合，在必要時重定向未驗證的使用者。

### 1.2 Repository Pattern Enforcement / 強制執行 Repository 模式
- **Refactor `Study`**: Move JSON asset loading and processing from Notifiers to a `LessonRepository`.
- **重構 `Study` 模塊**：將 JSON 資產的載入與處理從 Notifier 移至 `LessonRepository`。
- **Refactor `SRS`**: Move SM-2 logic and Drift interactions to an `SrsRepository`.
- **重構 `SRS` 模塊**：將 SM-2 邏輯與 Drift 資料庫交互移至 `SrsRepository`。

---

## 🔑 Phase 2: Authentication & Identity / 第二階段：身份驗證與識別
*Allow users to claim their data.*
*讓使用者能夠認領並保存其數據。*

### 2.1 Firebase & Google Integration / Firebase 與 Google 整合
- **Platform Config**: Setup Android/iOS in Google Cloud Console & Firebase.
- **平台配置**：在 Google Cloud Console 與 Firebase 中設定 Android/iOS 專案。
- **Google Sign-In**: Implement `google_sign_in` flow.
- **Google 登入**：實作 `google_sign_in` 流程。
- **Account Linking**: Allow users to start as guests and later "link" their Google account to persist data.
- **帳號關聯**：允許使用者先以訪客身份開始，稍後再「關聯」其 Google 帳號以持久保存數據。

### 2.2 Profile Management / 個人資料管理
- **Avatar Sync**: Store Peep configuration (JSON) in the cloud.
- **個人頭像同步**：將 Peep 配置 (JSON) 儲存於雲端。
- **User Settings**: Sync learner/target language preferences.
- **使用者設定**：同步母語與目標語言偏好。

---

## ☁️ Phase 3: Cloud Synchronization / 第三階段：雲端同步
*The bridge between local Drift and remote Firestore.*
*連接本地 Drift 與遠端 Firestore 的橋樑。*

### 3.1 Cloud-Sync Architecture / 雲端同步架構
- **Offline-First**: Drift remains the source of truth for UI.
- **離線優先**：Drift 仍作為 UI 的單一事實來源。
- **Sync Engine**: Implementation of a background sync service using `workmanager` or periodic Riverpod triggers.
- **同步引擎**：使用 `workmanager` 或週期的 Riverpod 觸發器實作後台同步服務。
- **Data Shape**: Firestore collections mirroring `Flashcards`, `Decks`, and `ReviewLogs`.
- **數據結構**：在 Firestore 中建立對應 `Flashcards`、`Decks` 和 `ReviewLogs` 的集合。

### 3.2 Conflict Resolution / 衝突解決
- **Timestamp Strategy**: Use `updatedAt` for last-write-wins.
- **時間戳策略**：使用 `updatedAt` 進行「最後寫入者勝 (Last-Write-Wins)」策略。
- **Delta Sync**: Only upload cards that changed since the last sync.
- **增量同步**：僅上傳自上次同步以來發生變更的卡片。

---

## 🎯 Phase 4: Engagement & Extensions / 第四階段：參與度與擴展
*Advanced features to boost retention.*
*提升使用者留存率的進階功能。*

### 4.1 Gamification / 遊戲化
- **Daily Streaks**: Calculated on server to prevent local spoofing.
- **每日連勝**：在伺服器端計算以防止本地端竄改。
- **XP System**: Award points for lesson completion and flashcard accuracy.
- **經驗值 (XP) 系統**：根據課程完成度和單字卡準確率授予點數。

### 4.2 Voice-Enabled Learning / 語音驅動學習
- **STT Integration**: Leverage `speech_to_text` for "Dictation" modes in flashcards.
- **STT 整合**：利用 `speech_to_text` 為單字卡提供「聽寫」模式。
- **Pronunciation Feedback**: Compare user audio input with tts output.
- **發音回饋**：將使用者的語音輸入與 TTS 輸出進行比較。

---

## 📅 Roadmap Timeline / 路線圖時程表

| Milestone / 里程碑 | Deliverables / 交付成果 | Status / 狀態 |
| --- | --- | --- |
| **OTA Content Delivery / OTA 內容交付** | Layered Pack Architecture, Zip Download / 分層壓縮包架構 | 🔥 In Progress / 進行中 |
| **Foundation / 基礎支柱** | Auth Layer, Repository Refactor / 驗證層、重構 Repository | ✅ Complete / 已完成 |
| **Identity / 身份識別** | Google Login, Firebase Setup / Google 登入、Firebase 設定 | ✅ Complete / 已完成 |
| **Sync / 雲端同步** | Cloud SRS Data, Profile Backup / 雲端 SRS 數據、資料備份 | 🧊 Future / 未來計畫 |
| **Growth / 成長擴展** | Streaks, Leaderboards, Voice Support / 連勝、排行榜、語音支援 | 🧊 Future / 未來計畫 |

> 📖 **Detailed OTA Implementation Plan**: See [OTA_ARCHITECTURE_PLAN.md](./OTA_ARCHITECTURE_PLAN.md)
