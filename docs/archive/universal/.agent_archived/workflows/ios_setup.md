---
description: Guide for setting up and building the iOS application with local signing or personal team.
---

# iOS Build & Setup Guide

由於 iOS 開發需要 Apple 簽署憑證，你需要使用 Xcode 設定你的開發者帳號 (或免費的 Personal Team)。

Since iOS development requires Apple signing certificates, you need to configure your developer account (or free Personal Team) using Xcode.

## 1. Environment Cleanup (已完成 / Done)

我們已經移除舊的 `DEVELOPMENT_TEAM` ID 並將 Bundle ID 修改為 `com.local.lingourmet`。
We have already removed the stale `DEVELOPMENT_TEAM` ID and updated the Bundle ID to `com.local.lingourmet`.

## 2. Xcode Configuration (Xcode 設定)

1.  Open the workspace / 開啟工作區:
    ```bash
    open lingourmet_universal/ios/Runner.xcworkspace
    ```

2.  Select Project Target / 選擇目標:
    - Click **Runner** (top left file navigator)
    - Click **Runner** (under Targets)
    - Select **Signing & Capabilities** tab.

3.  Configure Signing / 設定簽署:
    - **Team**: Select your Personal Team (Log in via Xcode Settings > Accounts if needed).
    - **Bundle Identifier**:
        - Use `com.local.lingourmet` (or append your name, e.g., `com.local.lingourmet.yourname` to make it unique).
        - Ensure both `Debug`, `Release`, and `Profile` (if visible) configurations use the same ID.

## 3. Provisioning (佈建)

-   Xcode will automatically generate a provisioning profile ("Managed by Xcode").
-   If you see "Failed to register bundle identifier", change the Bundle ID to something more unique.

## 4. Running on Device (實機測試)

1.  Connect your iPhone/iPad.
2.  Select your device in Xcode (top bar).
3.  Click **Run** (Play button) or use Flutter:
    ```bash
    flutter run -d <device_id>
    ```

**Note**: For free accounts (Personal Team), the provisioning profile is valid for **7 days**. You may need to rebuild/install after that.
**注意**: 免費帳號 (Personal Team) 的憑證有效期為 **7 天**。過期後需重新安裝。
