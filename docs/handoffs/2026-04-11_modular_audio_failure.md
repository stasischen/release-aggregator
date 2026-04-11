# Handoff: Modular Knowledge Lab Audio Failure (2026-04-11)

## Context
正在開發 `release-aggregator/docs/tasks/mockups/modular/` 中的知識文庫 Viewer。目前核心阻斷點在於：**使用者環境 (Safari/macOS) 的音訊與 TTS 持續失效**。

## Accomplishments (Hardening History)
我們已經嘗試過以下加固手段，但皆未解決使用者的靜音問題：
1. **原生 TTS 加固**：實作了 `window.ttsUtterances` 全域引用以防止 Safari 的 Garbage Collection。
2. **同步備援路徑 (Sync Fallback)**：在 `app_v2.js` 中實作了同步判斷邏輯。如果偵測到路徑無效（如 `unknown.mp3`），直接同步調用 `speakKo` 確保不丟失 User Gesture。
3. **引擎預熱 (Priming)**：加入 `primeAudioEngine()`。在使用者第一次點擊頁面任何位置時，觸發無聲語音與音軌，試圖解鎖 Origin 的播放授權。
4. **事件委派 (Event Delegation)**：將所有 `onclick` 屬性移除，改用 `document.body.addEventListener('click', ...)`，以維護最純潔的授權鏈。
5. **版本管理**：目前檔案已推進至 `v20260411-10`。

## Remaining / Clues for Next Agent
雖然主控台顯示 `TTS Engine: Started Speaking`，但使用者回報「依然無聲」。
1. **檢查 `localhost` 授權**：某些版本的 Safari 會針對 `localhost` 原生阻斷音訊，即使有手勢也一樣。
2. **測試不同語音**：目前程式碼偏好 `Yuna`。請嘗試強制切換到系統預設韓文語音，排除特定 Voice 損毀的可能性。
3. **雲端備援重啟**：如果原生 `speechSynthesis` 在該機器上被永久鎖死，可能需要重新考慮 Phase 1 的雲端 TTS (Google Cloud) 方案，但必須確保留住 User Gesture。
4. **檢查靜音鍵**：排除最基本的使用者環境硬體/系統靜音設定。

## Key Files
- [index.html](file:///Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/index.html) (Version: v20260411-10)
- [js/tts.js](file:///Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/tts.js) (Priming & Speak logic)
- [js/app_v2.js](file:///Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/app_v2.js) (Event delegation & Sync fallback)
- [js/renderers/core.js](file:///Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/mockups/modular/js/renderers/core.js) (Data attributes for audio)

## Next Steps
1. 啟動 `python3 -m http.server 8000`。
2. 讓使用者檢查 Safari 的「這網站的設定...」是否已將「自動播放」設為「允許所有自動播放」。
3. 嘗試在 `tts.js` 中完全不指定 Voice，由瀏覽器決定。
