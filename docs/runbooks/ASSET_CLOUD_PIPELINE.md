# Asset Cloud Pipeline: TTS 音檔雲端轉碼與同步指南

本 Runbook 說明如何將本地韓語 TTS 音檔 (`.mp3`) 轉換為高效能的 **WebM (Opus)** 格式，並同步至 **Firebase Storage** 與 **Firestore**。

---

## 1. 核心自動化邏輯 (The Pipeline)

我們使用的 `sync_cloud_assets.py` 腳本執行以下連鎖動作：

1. **轉碼 (Encoding)**：使用 FFmpeg 將 MP3 (約 128kbps) 轉為 WebM/Opus (24kbps)，體積縮小 70%+。
2. **存儲 (Storage)**：上傳轉碼後的檔案至 Firebase Storage，並設置為公共讀取（或配發 URL）。
3. **索引 (Indexing)**：讀取本地的 `*.sentences.json` 時間軸數據。
4. **同步 (Database)**：將 URL 與時間軸整合，寫入 Firestore `lessons/{lesson_id}/sentences/{audio_id}`。

---

## 2. 環境準備與 Firebase 金鑰設定

### Step 2.1: 安裝依賴

確保已在 `content-pipeline` 目錄下執行：

```powershell
python -m pip install firebase-admin pydub static-ffmpeg
```

### Step 2.2: 獲取 Firebase 服務帳戶金鑰 (必做)

為了讓腳本能代表你上傳檔案，需要設定 Service Account：

1. 開啟 [Firebase Console](https://console.firebase.google.com/)。
2. 點擊左上角齒輪 **專案設定 (Project Settings)**。
3. 切換至 **服務帳戶 (Service Accounts)** 標籤頁。
4. 點擊 **產生新的私密金鑰 (Generate New Private Key)**。
5. 這會下載一個 `.json` 檔案。

### Step 2.3: 放置金鑰與路徑設定

1. 在 `content-pipeline` 下建立 `credentials` 資料夾（如果不存在）。
2. 將下載的金鑰重新命名為：`firebase-adminsdk.json`。
3. 移動到以下路徑：
    `e:\Githubs\lingo\content-pipeline\credentials\firebase-adminsdk.json`

---

## 3. 執行同步操作

確保你在 `content-pipeline` 目錄下，執行以下指令：

```powershell
# 同步 A1-01 課次的所有音檔與數據
python scripts/assets/sync_cloud_assets.py
```

### 腳本行為說明

- **快取 (Cache)**：轉碼後的 `.webm` 會暫存在 `.cache/opus_conversion` 資料夾，避免重複計算。
- **跳過已上傳檔**：透過 MD5 檢查，若雲端已有相同檔案則不重複上傳，節省流量。

---

## 4. 前端 Viewer 整合建議

上傳完成後，你可以直接在 Firestore 中看到每句對話對應的 `audio_url`。

### 數據結構範例 (Firestore: `lessons/A1-01/sentences/L01-D1-01`)

```json
{
  "id": "L01-D1-01",
  "audio_url": "https://storage.googleapis.com/...",
  "full_text": "안녕하세요!...",
  "sentences": [
    { "text": "안녕하세요!", "start_ms": 100, "duration_ms": 2187 }
  ]
}
```

---

## 5. 常見問題 (Q&A)

* **Q: 轉碼很慢嗎？**
  - A: 第一次轉碼需要時間，但腳本會快備份已轉碼的檔案。
- **Q: 如果我想更改 Bitrate (音質)？**
  - A: 修改 `sync_cloud_assets.py` 中的 `"-b:a", "24k"` 參數。
- **Q: 為什麼不用 MP3？**
  - A: Opus 在相同低碼率下的清晰度遠高於 MP3，且能顯著減少學生開啟頁面的等待時間。
