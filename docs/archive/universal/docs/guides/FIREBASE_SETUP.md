# Firebase Configuration Guide / Firebase 設定指南

既然你對 Firebase 配置不熟悉，這份文件會帶你一步步完成設定。我們會使用 **FlutterFire CLI**，這是目前官方推薦最簡單的方法。

## 🛠️ Step 1: 準備工作 (Prerequisites)

在終端機執行以下檢查，確保你有安裝必要的工具：

1.  **Firebase CLI**:
    *   **推薦方式 (Mac)**: 使用 Homebrew 安裝，比較不會有權限問題。
        ```bash
        brew install firebase-cli
        ```
    *   **檢查版本**:
        ```bash
        firebase --version
        ```
    *   (替代方案): 如果沒有 Homebrew，可用 npm: `npm install -g firebase-tools`。

2.  **登入 Firebase**:
    ```bash
    firebase login
    ```
    *   這會開瀏覽器讓你登入 Google 帳號。選你要用的帳號並授權。

3.  **FlutterFire CLI**:
    ```bash
    dart pub global activate flutterfire_cli
    ```
    *   這會安裝 Dart 版的設定工具。

---

## 🚀 Step 2: 專案初始化 (Initialization)

1.  **在專案根目錄執行**:
    ```bash
    flutterfire configure
    ```

2.  **互動式選單操作**:
    *   **Select a Firebase project**:
        *   選 `<create a new project>` (建立新專案)。
        *   輸入專案名稱 (例如: `lingourmet-universal` - 只能小寫英文、數字、連字號)。
    *   **Select platforms**:
        *   用上下鍵移動，空白鍵 (Space) 選取/取消。
        *   **務必選取**: `android`, `ios`, `macos` (web 可選可不選)。
        *   按 Enter 確認。

3.  **Android Package Name**:
    *   它會問你 Android 的套件名稱。通常預設是 `com.example.lingourmet_universal`。
    *   **建議修改**：如果要上架，最好改成你自己的網域反寫，例如 `com.stasischen.lingourmet`。
    *   (如果不確定，直接按 Enter 用預設，但未來改很麻煩)。

---

## ✅ Step 3: 確認結果

完成後，你會發現專案裡多了幾個東西：
*   `lib/firebase_options.dart`: 這是自動生成的設定檔，裡面包含 API Keys。
*   `android/app/google-services.json`: Android 專用設定。
*   `ios/Runner/GoogleService-Info.plist`: iOS 專用設定。
*   `macos/Runner/GoogleService-Info.plist`: macOS 專用設定。

---

## 📝 Step 4: 啟用功能 (Console Setup)

回到 [Firebase Console](https://console.firebase.google.com/) 網頁：

1.  點選剛剛建立的專案。
2.  **Authentication**:
    *   點左側 `Authentication` -> `Get started`。
    *   `Sign-in method` 分頁 -> 啟用 **Google** 與 **Anonymous (匿名)**。
3.  **Firestore Database**:
    *   點左側 `Firestore Database` -> `Create database`。
    *   Location 選 `asia-east1` (台灣) 或 `us-central1`。
    *   Start in **Test mode** (測試模式，方便開發)。

搞定這些後，告訴我一聲，我們就可以開始寫 Code 把 Firebase 接上去了！
