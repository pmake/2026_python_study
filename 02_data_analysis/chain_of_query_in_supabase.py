# 💡 鏈式查詢範例：過濾、排序與限制筆數
from database import supabase
import pandas as pd


response = (
    supabase
    .schema('public') # 明確指定要查詢的schema，未指定時會使用預設值
    .table("orders")
    .select("orderid, employeeid, customerid, orderdate")  # 選擇特定欄位
    .eq("employeeid", 3)  # WHERE total_amount >= 1000
    .order("orderdate", desc=True)  # ORDER BY created_at DESC
    .limit(10)  # LIMIT 10
    .execute()
)

# 直接轉為 Pandas DataFrame
df = pd.DataFrame(response.data)
print(df)