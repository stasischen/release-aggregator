# Windows Build Fix: flutter_tts CMake Patch

## 問題描述 (Problem Description)

`flutter_tts` 插件的 `CMakeLists.txt` 文件損壞，導致 Windows 構建失敗。

The `flutter_tts` plugin's `CMakeLists.txt` is corrupted, causing Windows build failures.

## 錯誤信息 (Error Messages)

```
Parse error. Expected "(", got identifier with text "install"
LNK2019: Unresolved external symbol RoGetActivationFactory
```

## 根本原因 (Root Cause)

插件嘗試下載 NuGet 包但 CMake 語法錯誤，同時缺少必要的 WinRT 庫鏈接。

The plugin attempts to download NuGet packages but has malformed CMake syntax and missing WinRT library links.

## 修復步驟 (Fix Steps)

### 自動修復 (需在每台新機器執行一次)

### Automatic Fix (Run once on each new machine)

```powershell
# 在項目根目錄執行 (Run in project root)
cd e:\Githubs\Lingourmet_universal\lingourmet_universal

# 1. 找到 flutter_tts 插件目錄
$pubCache = "$env:LOCALAPPDATA\Pub\Cache\hosted\pub.dev"
$pluginPath = Get-ChildItem -Path $pubCache -Directory -Filter "flutter_tts-*" | Select-Object -First 1

# 2. 覆蓋 CMakeLists.txt
$cmakeFile = Join-Path $pluginPath.FullName "windows\CMakeLists.txt"
$fixedContent = @"
cmake_minimum_required(VERSION 3.14)
set(PROJECT_NAME "flutter_tts")
project(`${PROJECT_NAME} LANGUAGES CXX)
set(PLUGIN_NAME "flutter_tts_plugin")
add_library(`${PLUGIN_NAME} SHARED "flutter_tts_plugin.cpp")
apply_standard_settings(`${PLUGIN_NAME})
target_compile_definitions(`${PLUGIN_NAME} PRIVATE FLUTTER_PLUGIN_IMPL)
target_include_directories(`${PLUGIN_NAME} INTERFACE "`${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(`${PLUGIN_NAME} PRIVATE flutter flutter_wrapper_plugin)
if (WIN32)
    target_link_libraries(`${PLUGIN_NAME} PRIVATE runtimeobject windowsapp)
endif()
if(MSVC)
    target_compile_options(`${PLUGIN_NAME} PRIVATE "/await")
endif()
"@
Set-Content -Path $cmakeFile -Value $fixedContent -Encoding UTF8

# 3. 清理並重建
flutter clean
flutter pub get
```

### 手動位置 (Manual Location)

如果自動腳本失敗，請手動編輯：
If the automatic script fails, manually edit:

```
C:\Users\<YOUR_USERNAME>\AppData\Local\Pub\Cache\hosted\pub.dev\flutter_tts-4.2.3\windows\CMakeLists.txt
```

## 為什麼需要在每台機器執行 (Why Run on Each Machine)

這個文件位於 **Pub Cache**（Flutter 包緩存），不會被 Git 追蹤。每台機器首次運行 `flutter pub get` 後都需要手動修復。

This file is in the **Pub Cache** (Flutter package cache), not tracked by Git. Each machine needs the fix after first `flutter pub get`.

## 替代方案 (Alternative Solution)

如果您經常需要清理緩存，可以考慮：
If you frequently clean cache, consider:

1. **Fork flutter_tts** 並發布修復版本
2. **使用 dependency_overrides** 指向本地修復版本
3. **提交 PR** 到官方倉庫修復上游問題

4. **Fork flutter_tts** and publish a fixed version
5. **Use dependency_overrides** to point to a local fixed version
6. **Submit a PR** to the official repo to fix upstream

## 驗證修復 (Verify Fix)

```powershell
# 應該成功構建 (Should build successfully)
flutter run -d windows
```

如果仍然失敗，請檢查：
If still failing, check:

- CMake 版本 >= 3.14
- Visual Studio 2019/2022 已安裝
- Windows SDK 已安裝
