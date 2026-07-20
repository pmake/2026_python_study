import os
from dotenv import load_dotenv
from supabase import Client, create_client
from supabase import create_client, Client, ClientOptions

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

# 直接在 ClientOptions 中指定 schema，未指定的情況下預設為public
options = ClientOptions(schema="nba")

# 初始化 Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
print("🚀 Supabase 連接成功！網址為：", SUPABASE_URL)