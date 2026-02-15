# V5 Pipeline: Troubleshooting & Edge Cases

## ❌ Permission Denied during Sync

- **原因**: Google Sheets API 憑證失效或未授權給 Service Account。
- **對策**: 參考 `tools/backup/sync_to_gsheet.py` 中的日誌輸出，確認 Service Account 電子郵件是否有該 Spreadsheet 的編輯權限。

## ❌ Merger Output is Empty

- **原因**: `1_translation` 或 `2_atoms` 對應的語言資料夾不存在。
- **對策**: 重新執行 `python -m tools.v5.core.update_db {lang}`。

## ❌ AI Repair Loop

- **原因**: 字典中的 [TODO] 格式不符或 Ollama 響應超時。
- **對策**: 檢查 `4_dictionary/` 下的 CSV 是否為 UTF-8 編碼。
