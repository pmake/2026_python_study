import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

# 將 02_data_analysis 目錄加入 sys.path，以便導入 database 模組
db_dir = Path(__file__).resolve().parents[3] / "02_data_analysis"
if str(db_dir) not in sys.path:
    sys.path.append(str(db_dir))

from database import supabase

# 1. 指定雷達圖分析指標
metrics = ["ppg", "rpg", "apg", "bpg", "mpg"]

# 2. 查詢所有球員的生涯數據，用以計算各欄位在全體球員中的最大值
all_summary_response = (
    supabase
    .schema("nba")
    .table("career_summaries")
    .select("ppg, rpg, apg, bpg, mpg")
    .execute()
)
all_summary_df = pd.DataFrame(all_summary_response.data)
for col in metrics:
    all_summary_df[col] = pd.to_numeric(all_summary_df[col], errors="coerce")

# 計算各欄位的全體球員最大值
max_metrics = all_summary_df[metrics].max()

# 3. 從 Supabase 查詢目標球員：players inner join career_summaries
# 以 firstname 篩選 "LeBron", "Carmelo"，選取所有欄位
response = (
    supabase
    .schema("nba")
    .table("players")
    .select("*, career_summaries!inner(*)")
    .in_("firstname", ["LeBron", "Carmelo"])
    .execute()
)

# 4. 將回傳資料轉換為 Pandas DataFrame
df = pd.json_normalize(response.data)

# 整理欄位名稱（去除 join 產生的 career_summaries. 前綴）
df.columns = [col.replace("career_summaries.", "") for col in df.columns]

# 確保目標球員資料中的指標欄位為數值型別
for col in metrics:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. 根據「全體球員各欄位的最大值」，將數值轉換成 0-10
scaled_df = df[["firstname"] + metrics].copy()
for col in metrics:
    max_val = max_metrics[col]
    if pd.notnull(max_val) and max_val > 0:
        scaled_df[col] = (scaled_df[col] / max_val) * 10
    else:
        scaled_df[col] = 0

# 6. 將資料轉換為長表格格式 (Melt)，以便 Plotly 繪圖
df_melt = scaled_df.melt(
    id_vars="firstname",
    value_vars=metrics,
    var_name="指標",
    value_name="評分"
)

# 7. 使用 Plotly Express 繪製 line_polar 雷達圖
fig = px.line_polar(
    df_melt,
    r="評分",
    theta="指標",
    color="firstname",
    line_close=True,
    markers=True,
    title="LeBron James vs Carmelo Anthony 生涯數據雷達圖 (以全體球員最大值標準化 0-10)",
    labels={
        "firstname": "球員",
        "指標": "能力指標",
        "評分": "標準化評分 (0-10)"
    }
)

# 區域半透明填滿以增強視覺可讀性
fig.update_traces(fill="toself", opacity=0.4)

# 8. 顯示圖表
fig.show()
