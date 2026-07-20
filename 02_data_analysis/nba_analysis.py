# 💡 鏈式查詢範例：過濾、排序與限制筆數
from database import supabase
import pandas as pd


response = (
    supabase
    .schema('nba') # 單次查詢時動態指定 Schema的方式
    .table("players")
    .select("*")  # 選擇特定欄位
    .limit(10)  # LIMIT 10
    .execute()
)

# 直接轉為 Pandas DataFrame
df = pd.DataFrame(response.data)
print(df)