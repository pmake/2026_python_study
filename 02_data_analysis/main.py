from database import supabase
import pandas as pd




def fetch_orders_as_dataframe() -> pd.DataFrame:
    """從 Supabase 抓取 orders 資料並轉換為 Pandas DataFrame"""
    response = supabase.table("orders").select("*").execute()
    data = response.data

    # 防禦性檢查：處理 RLS 導致回傳空陣列的情況
    if not data:
        print("⚠️ 警告：成功連線但取得 0 筆資料！")
        print("💡 請確認 Supabase 後台 orders 表的 RLS (Row Level Security) 是否已設定 SELECT Policy。")
        return pd.DataFrame()

    # 優雅轉為 Pandas DataFrame
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    df_orders = fetch_orders_as_dataframe()

    if not df_orders.empty:
        print(f"✅ 成功抓取 {len(df_orders)} 筆訂單資料！")
        # 檢視前 5 筆資料與基本資訊
        print(df_orders.head())
        print("\n資料表結構資訊：")
        print(df_orders.info())