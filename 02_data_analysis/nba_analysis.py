# 💡 鏈式查詢範例：過濾、排序與限制筆數
from database import supabase
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Literal

# 1. 定義查詢參數（使用 Literal 提供更安全的型別檢查）
Conference = Literal["West", "East"]
target_conf: Conference = "West"
team_full_name: str = "Los Angeles Lakers"

response = (
    supabase
    .schema('nba') # 單次查詢時動態指定 Schema的方式
    .table("players")
    # 使用supabase !inner語法，join teams table 選擇回傳特定欄位, 例中要求傳回fullname, 留空則不傳回teams table的任何欄位
    # players和teams在資料庫中必須有設定關聯的外鍵，此例已在supabase設定好了teamid為foreign key，背後會先用外鍵去關聯然後用team_full_name過濾
    # supabase中的RLS如果有開，也要設定能讀取的policy才能正常從外部查詢
    .select("*, teams!inner(fullname,confname)")  
    .eq('teams.fullname', team_full_name)
    .eq('teams.confname', target_conf)
    .execute()
)

# 直接轉為 Pandas DataFrame
df = pd.DataFrame(response.data)
print(df)


if df.empty:
    print('查無資料，未產生csv檔。')
else:
    # 將嵌套的 json 欄位展開為平坦欄位 (Flatten)
    # 使用 「串列生成式（List Comprehension）」搭配「多欄位同時指派」
    # Pandas 支援將一個包含 Tuple 的 List（例如 [('Lakers', 'West'), ('Celtics', 'East')]）直接賦值給多個欄位 df[["team_name", "conf_name"]]，
    # 它會自動將第一位對應到 team_name，第二位對應到 conf_name。
    if 'teams' in df.columns:
        df[['fullname', 'confname']] = [ 
            (x.get('fullname'), x.get('confname')) if isinstance(x, dict) else (None, None) for x in df['teams']
              ]
        
        df = df.drop(columns=['teams']) # 刪除原始嵌套欄位
    

    output_dir =  Path('02_data_analysis/outputs')
    output_dir.mkdir(parents=True, exist_ok=True) # 自動建立資料夾(若不存在)

    # 加上時間戳記，避免覆蓋舊檔案
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # '/'是path物件的特殊符號，用以便利的跨平台串接路徑，會自動依平台轉換正確的路徑
    file_path = output_dir / f'lakers_players_west_{timestamp}.csv'

    # 4. 儲存為 CSV
    df.to_csv(
        file_path,
        index=False,  # 關鍵設定：不儲存 Pandas 自動產生的數字索引列 (0, 1, 2...)
        encoding="utf-8-sig",  # 關鍵設定：加上 BOM 頭，確保 Excel 打開中文時不亂碼
    )

    print(f"✅ 成功將 {len(df)} 筆資料匯出至：{file_path.resolve()}")