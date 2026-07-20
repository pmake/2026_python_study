import os
from dotenv import load_dotenv
from supabase import Client, create_client

# 載入 .env 檔案
load_dotenv()

# 讀取環境變數
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

# 最佳實作：提前防禦性檢查，避免執行時才拋出模糊異常
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "❌ 找不到 Supabase 設定！請確認是否已在 .env 中正確設定 SUPABASE_URL 與 SUPABASE_PUBLISHABLE_KEY"
    )

# 初始化 Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("🚀 Supabase 連接成功！網址為：", SUPABASE_URL)