# Handoff Document: 保母薪資單與工時統計專案 (02_data_analysis)

## 專案狀態概觀 (Project Overview)
已完成對 `02_data_analysis/專案需求定義.md` 的完整 `/grill-with-docs` 審查與決策對齊。
所有業務邊界、轉場加時演算法、假日班規範、工時單位與 Excel 跨表驗證公式已全數確認，並建立了完整的領域字典與架構決策紀錄 (ADRs)。
目前已產出 [實作計劃 (implementation_plan.md)](file:///C:/Users/User/.gemini/antigravity-ide/brain/5c2147e8-1cb4-4178-b759-a52c02d953c2/implementation_plan.md)，使用者已確認無誤，準備進入 Python 程式寫入與 Excel 生成階段。

---

## 關鍵參考文件 (Artifacts & Reference Docs)

- **需求文件**：[專案需求定義.md](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/%E5%B0%88%E6%A1%88%E9%9C%80%E6%B1%82%E5%AE%9A%E7%BE%A9.md)
- **領域名詞字典**：[CONTEXT.md](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/CONTEXT.md)
- **實作計畫**：[implementation_plan.md](file:///C:/Users/User/.gemini/antigravity-ide/brain/5c2147e8-1cb4-4178-b759-a52c02d953c2/implementation_plan.md)
- **架構決策紀錄 (ADRs)**：
  1. [ADR 0001: 假日班平日出勤之薪資計算與異常稽核處理](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/docs/adr/0001-handling-weekend-shift-weekday-attendance.md)
  2. [ADR 0002: 轉場加時之地址切換判斷邏輯與有效欄位定義](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/docs/adr/0002-transit-time-address-transition-calculation.md)
  3. [ADR 0003: 工時單位以分鐘儲存並透過 Excel 公式轉換為小時](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/docs/adr/0003-work-hours-unit-minutes-and-excel-formula-conversion.md)
  4. [ADR 0004: 每日工時明細表採用完整日曆日期補全](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/docs/adr/0004-full-calendar-dates-padding-in-daily-details.md)

---

## 輸入與輸出檔案 (Input & Output Files)
- **輸入檔**：
  - `02_data_analysis/outputs/好寶寶系統設定.xlsx`（包含 Sheet: `員工總表` 與 Sheet: `假日定義`）
  - `02_data_analysis/outputs/服務紀錄總表.xlsx`（包含 Sheet: `Sheet1`）
- **目標輸出檔**：
  - `02_data_analysis/outputs/薪資單.xlsx`
- **主要腳本位置**：
  - [專案練習.py](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/%E5%B0%88%E6%A1%88%E7%B7%B4%E7%BF%92.py)

---

## 下一步接續工作 (Next Steps)
接手 Agent 請依據 [implementation_plan.md](file:///C:/Users/User/.gemini/antigravity-ide/brain/5c2147e8-1cb4-4178-b759-a52c02d953c2/implementation_plan.md) 執行以下步驟：
1. 修改 [專案練習.py](file:///c:/Users/User/Desktop/Python0730/2026_python_study/02_data_analysis/%E5%B0%88%E6%A1%88%E7%B7%B4%E7%BF%92.py)，實作：
   - 讀取系統設定（員工總表與假日定義）。
   - 按保母、日期、時間排序並計算同日轉場加時。
   - 計算常日班/假日班與平日/假日的工時分段（分鐘數）。
   - 使用 `openpyxl` 建立個別員工明細 Sheet（31天完整日曆數據）、`員工工時統計表`（`/60` Excel 公式）、`驗證用資料表`（SUM 與 SUMIF 跨表公式對比）以及 `異常情況` 工作表。
2. 執行腳本：`.venv\Scripts\python.exe 02_data_analysis/專案練習.py`。
3. 驗證產出的 `薪資單.xlsx` 結構與公式正確性。

---

## 建議 Skill (Suggested Skills)
- `tdd` (Test-Driven Development)：可用於驗證工時分段計算邏輯與轉場地址切換邏輯的單元測試。
