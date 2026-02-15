# 🎫 Review Request: [Task ID]

## 📊 執行摘要
- **狀態**: 待審查 (Ready for Review)
- **負責人**: [Agent Name]
- **Commit**: [Hash] (請填寫最後一個 commit hash)
- **Finding IDs**: [F-xxxx, F-yyyy]

## 🧪 測試證據
- [ ] **單元測試**: 通過 [X] 個 / 失敗 [Y] 個
- [ ] **整合測試**: 通過 [X] 個 / 失敗 [Y] 個
- [ ] **Lint 檢查**: 是否乾淨？ (Yes/No)

### 關鍵測試輸出 (Log Snapshot)
```text
(請貼上 flutter test 的關鍵輸出，證明測試通過)
```

## 📝 變更清單
### 修改的檔案
- `lib/...`: [簡述修改內容]
- `test/...`: [簡述修改內容]

### 新增的檔案
- `lib/...`: [用途]

## ✅ 驗收標準 (Acceptance Criteria)
- [ ] [條件 1]
- [ ] [條件 2]
- [ ] [條件 3]

## 🚫 非本次範圍 (Out of Scope)
- [明確列出這次不處理的項目，避免 scope creep]

## 👷 給 Architect 的交接事項
- **重點關注**: [請 Architect 特別檢查的邏輯或邊界情況]
- **驗證方式**: 執行 `flutter test [specific_test_file]`
- **潛在風險**: [是否有未解的 TODO 或取捨]
- **Rollback Plan**: [若發生回歸，如何快速回退]

---
*由 Builder 填寫，提交 REVIEW 前必須完成*
