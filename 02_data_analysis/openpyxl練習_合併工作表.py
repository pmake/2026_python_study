import pandas as pd
from pathlib import Path
from openpyxl.styles import PatternFill

# 1. 使用 pathlib 定義檔案路徑（現代 Python 建議作法，跨平台相容性佳）
target_dir = Path('02_data_analysis/outputs')
target_file_path = target_dir / '部門資料.xlsx'


# 2. 設定 sheet_name=None 會一次讀取所有工作表
# 這會回傳一個字典 (dict)，key 是工作表名稱，value 是對應的 DataFrame
sheets_dict = pd.read_excel(target_file_path, sheet_name=None)

# 3. 使用列表生成式 (List Comprehension) 與 .assign() 將工作表名稱保留為新欄位
# 這樣合併後才知道每一列資料原本是來自哪一個工作表
df_list = [
    df.assign(Source_Sheet=sheet_name) for sheet_name, df in sheets_dict.items()
]

# 4. 使用 pd.concat() 將所有 DataFrame 垂直合併
# ignore_index=True 可以重新重置索引，避免合併後索引重複混亂
df_combined = pd.concat(df_list, ignore_index=True)

# 檢視合併後的結果
print(df_combined.head())




# 將已建立的dataframe物件存入excel檔案的不同工作表

# 先過濾要儲存的欄位
# players_multi_conditions = players_multi_conditions.loc[:, ['firstname', 'lastname', 'ppg', 'apg', 'rpg']]

output_path = target_dir / 'combined_sheets.xlsx'


# 使用 pd.ExcelWriter 上下文管理器 (自動處理開啟與關閉)
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_combined.to_excel(writer, sheet_name="合併資料", index=False)

    

    print("多工作表合併 Excel 建立完成！")

    