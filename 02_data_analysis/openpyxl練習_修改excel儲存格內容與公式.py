import pandas as pd
import openpyxl
from pathlib import Path

def modify_excel(file_path, save_path):
    try:
        # 1. 讀取現有的 Excel 檔案
        # data_only=False 表示我們要讀取的是公式本身，而不是公式計算後的值
        workbook = openpyxl.load_workbook(file_path, data_only=False)
        
        # 2. 選擇工作表
        # 可以使用 workbook.active 選擇目前作用中的工作表
        # 或者使用 workbook['工作表名稱'] 指定特定工作表，例如 sheet = workbook['Sheet1']
        sheet = workbook.active
        
        print(f"成功讀取檔案。目前作用中的工作表為: {sheet.title}")

        # 3. 修改指定儲存格的「文字內容」
        # 假設我們要將 A1 儲存格的文字改為 "本月總收入"
        sheet['E2'].value = "平均銷售額"
        
        # 你也可以用 row 和 column 數字來指定儲存格 (例如第 2 列第 5 欄就是 E2)
        # sheet.cell(row=2, column=2, value="平均銷售額")

        # 4. 修改指定儲存格的「公式」
        # 假設我們要將 E3 儲存格設定為計算 C3/D3 的公式
        sheet['E3'].value = "=C3/D3"
        
        # 5. 儲存檔案
        # 建議另存新檔，避免直接覆蓋原始檔案而造成資料遺失
        workbook.save(save_path)
        workbook.close()
        print(f"檔案已成功修改並儲存至: {save_path}")

    except FileNotFoundError:
        print(f"找不到檔案：{file_path}，請確認檔案路徑是否正確。")
    except Exception as e:
        print(f"發生錯誤：{e}")


# ==========================================
# 執行區域
# ==========================================
if __name__ == "__main__":
    # 【優雅技巧】使用 pathlib 處理路徑，取代傳統的 os.path 字串拼接
    BASE_DIR = Path.cwd()
    work_dir = BASE_DIR / '02_data_analysis' / 'outputs'
    print(work_dir)
    
    # 運用 / 運算子優雅地串接路徑
    template_file_path = work_dir / '業務分析報告表格.xlsx'
    output_file_path = work_dir / '業務分析報告表格_修改.xlsx'

    # 執行函式
    modify_excel(template_file_path, output_file_path)
    print(f"✅ 報告已成功生成並儲存至：{output_file_path}")