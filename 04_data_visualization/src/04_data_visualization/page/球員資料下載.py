import sys
from pathlib import Path
import io
import streamlit as st
import pandas as pd

# ==========================================
# 導入 database 模組 (Supabase 連線)
# ==========================================
current_dir = Path(__file__).resolve().parent
for parent in [current_dir] + list(current_dir.parents):
    db_candidate = parent / "02_data_analysis"
    if db_candidate.exists() and str(db_candidate) not in sys.path:
        sys.path.append(str(db_candidate))
        break

# ==========================================
# 資料載入與快取函式 (3 表 Inner Join)
# ==========================================
@st.cache_data(ttl=600, show_spinner="正在從 Supabase 取得 NBA 球員、球隊與生涯數據...")
def load_all_players_full_data():
    """
    從 Supabase 查詢 nba schema 中的 3 張表：
    1. players (球員基本資料)
    2. career_summaries (生涯數據統計，以 personid 做 inner join)
    3. teams (所屬球隊資料，以 teamid 做 inner join)
    選取所有欄位並平坦化為 Pandas DataFrame。
    """
    try:
        from database import supabase
    except Exception as err:
        return None, f"導入 database.py 失敗：{err}"

    try:
        # 使用 Supabase !inner 語法執行 3 表 Inner Join 查詢所有欄位
        response = (
            supabase
            .schema("nba")
            .table("players")
            .select("*, career_summaries!inner(*), teams!inner(*)")
            .execute()
        )

        raw_data = response.data
        if not raw_data:
            return None, "資料庫未回傳任何球員資料。"

        # 展平巢狀 JSON 結構
        df = pd.json_normalize(raw_data)

        # 移除重複欄位 (若兩表皆有相同鍵值)
        df = df.loc[:, ~df.columns.duplicated()]

        # 建立全名欄位 (firstname + lastname)
        df["player_name"] = (
            df["firstname"].fillna("").astype(str).str.strip()
            + " "
            + df["lastname"].fillna("").astype(str).str.strip()
        ).str.strip()

        # 數值型態清理與轉換
        numeric_cols = [
            "career_summaries.ppg", "career_summaries.rpg", "career_summaries.apg",
            "career_summaries.bpg", "career_summaries.spg", "career_summaries.mpg",
            "career_summaries.points", "career_summaries.totreb", "career_summaries.assists",
            "career_summaries.steals", "career_summaries.blocks", "career_summaries.fgp",
            "career_summaries.ftp", "career_summaries.tpp", "career_summaries.gamesplayed",
            "career_summaries.gamesstarted", "career_summaries.turnovers", "career_summaries.plusminus",
            "heightmeters", "weightkilograms", "jersey", "nbadebutyear", "yearspro"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df, None

    except Exception as err:
        return None, f"Supabase 資料庫查詢異常：{err}"


def to_excel_bytes(dataframe: pd.DataFrame, sheet_name: str = "球員資料") -> bytes:
    """將 DataFrame 轉換為 .xlsx (Excel) 格式的二進位字節流。"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


# ==========================================
# 載入資料
# ==========================================
df, error_msg = load_all_players_full_data()

# ==========================================
# 自訂美化樣式 (CSS)
# ==========================================
st.markdown(
    """
    <style>
    .dl-header-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0288D1 0%, #00796B 50%, #388E3C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .dl-subtitle {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 1.2rem;
    }
    .info-card {
        background: linear-gradient(145deg, #f0f7ff 0%, #f4fbf7 100%);
        border: 1px solid #cce5ff;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .stat-badge {
        display: inline-block;
        background-color: #00796B;
        color: white;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .highlight-val {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0288D1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 頁面標題與簡介
# ==========================================
st.markdown('<div class="dl-header-title">📥 NBA 球員資料查詢與 Excel 下載</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dl-subtitle">整合 Supabase <code>players</code> (球員)、<code>career_summaries</code> (生涯數據) 與 <code>teams</code> (球隊) 3 表關聯查詢，支援單一球員與全體資料即時匯出 <b>.xlsx</b> 檔案。</div>',
    unsafe_allow_html=True,
)

# 錯誤處理與提示
if error_msg is not None:
    st.error(f"❌ {error_msg}")
    st.info("💡 請確認 `.env` 中的 `SUPABASE_URL` 與 `SUPABASE_PUBLISHABLE_KEY` 是否已設定，且資料庫連線正常。")
    st.stop()

if df is None or df.empty:
    st.warning("⚠️ 資料庫中查無任何球員資料。")
    st.stop()

# ==========================================
# 頂部概覽指標 (KPI Cards)
# ==========================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_players = len(df)
total_teams = df["teams.fullname"].nunique() if "teams.fullname" in df.columns else 30
active_seasons = f"{int(df['nbadebutyear'].min())} ~ {int(df['nbadebutyear'].max())}" if "nbadebutyear" in df.columns else "N/A"
total_cols = len(df.columns)

with kpi1:
    st.metric(label="🏀 關聯球員總數", value=f"{total_players} 位")
with kpi2:
    st.metric(label="🏟️ 涵蓋球隊數", value=f"{total_teams} 支")
with kpi3:
    st.metric(label="📅 選秀/出道年份跨度", value=active_seasons)
with kpi4:
    st.metric(label="📑 完整整合欄位數", value=f"{total_cols} 個欄位")

st.divider()

# ==========================================
# 下拉選單：球員選擇器 (firstname + lastname)
# ==========================================
st.subheader("🎯 選擇目標球員")

# 建立排序好的球員清單 (firstname + lastname)
player_names = sorted(df["player_name"].dropna().unique().tolist())

# 增加「全部球員資料」選項，方便使用者進行批次匯出
ALL_OPTION = f"📋 【全部球員資料】 (共 {len(player_names)} 位球員)"
select_options = [ALL_OPTION] + player_names

# 預設選取著名球員（例如 LeBron James，若無則選第 1 位球員）
default_index = 0
if "LeBron James" in player_names:
    default_index = select_options.index("LeBron James")

sel_col1, sel_col2 = st.columns([3, 2])

with sel_col1:
    selected_option = st.selectbox(
        "🔍 請選擇球員（支援鍵盤直接輸入名稱快速搜尋）：",
        options=select_options,
        index=default_index,
        help="選項由 players 資料表中的 firstname + lastname 組成。"
    )

is_all_selected = (selected_option == ALL_OPTION)

# 依選取過濾資料
if is_all_selected:
    target_df = df.copy()
    current_player_name = "All_NBA_Players"
    display_title = f"全部 NBA 球員資料（共 {len(target_df)} 筆）"
else:
    target_df = df[df["player_name"] == selected_option].copy()
    current_player_name = selected_option
    display_title = f"🏀 球員【{selected_option}】詳細資料"

with sel_col2:
    # 產生 Excel 二進位資料
    excel_file_bytes = to_excel_bytes(
        target_df,
        sheet_name=selected_option[:30] if not is_all_selected else "全體球員資料"
    )
    
    # 檔名清理
    clean_filename = selected_option.replace(" ", "_").replace("【", "").replace("】", "")
    excel_filename = f"NBA_{clean_filename}_Data.xlsx"

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.download_button(
        label=f"📥 下載【{selected_option}】為 .xlsx",
        data=excel_file_bytes,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        type="primary",
        help="點擊立即下載包含 players, career_summaries, teams 3 表所有欄位的 Excel 試算表檔案。"
    )

st.divider()

# ==========================================
# 球員詳細卡片 (當選擇單一球員時呈現精美資訊卡)
# ==========================================
if not is_all_selected and not target_df.empty:
    player_row = target_df.iloc[0]
    
    st.subheader(f"👤 {display_title}")

    card_c1, card_c2, card_c3 = st.columns(3)

    # 1. 基本身家背景
    with card_c1:
        st.markdown("""
        <div class="info-card">
            <h4>📋 基本背景資訊</h4>
        """, unsafe_allow_html=True)
        jersey = player_row.get('jersey')
        jersey_str = f"#{int(jersey)}" if pd.notnull(jersey) else "未提供"
        pos = player_row.get('pos', '未提供')
        height_m = player_row.get('heightmeters', '未提供')
        weight_kg = player_row.get('weightkilograms', '未提供')
        dob = player_row.get('dateofbirthutc', '未提供')
        college = player_row.get('collegename', '無大學經歷 / 直升')
        country = player_row.get('country', 'USA')
        debut = player_row.get('nbadebutyear', '未提供')
        exp = player_row.get('yearspro', '未提供')

        st.markdown(f"""
        - **背號 / 位置**：`{jersey_str}` / `{pos}`
        - **身高 / 體重**：`{height_m} m` / `{weight_kg} kg`
        - **出生日期**：`{dob}`
        - **國籍 / 大學**：`{country}` / `{college}`
        - **NBA 出道年份**：`{debut}` (球齡: `{exp}` 年)
        </div>
        """, unsafe_allow_html=True)

    # 2. 所屬球隊資訊 (來自 teams 表)
    with card_c2:
        st.markdown("""
        <div class="info-card">
            <h4>🏟️ 所屬球隊 (Teams)</h4>
        """, unsafe_allow_html=True)
        team_fullname = player_row.get('teams.fullname', '未提供')
        team_tricode = player_row.get('teams.tricode', '')
        team_conf = player_row.get('teams.confname', '未提供')
        team_div = player_row.get('teams.divname', '未提供')
        team_city = player_row.get('teams.city', '未提供')
        team_nickname = player_row.get('teams.nickname', '未提供')

        st.markdown(f"""
        - **球隊全稱**：**{team_fullname}** (`{team_tricode}`)
        - **所屬分區**：`{team_conf} Conference`
        - **分組賽區**：`{team_div} Division`
        - **所在城市**：`{team_city}`
        - **球隊暱稱**：`{team_nickname}`
        </div>
        """, unsafe_allow_html=True)

    # 3. 生涯關鍵數據 (來自 career_summaries 表)
    with card_c3:
        st.markdown("""
        <div class="info-card">
            <h4>📊 生涯核心數據 (Career)</h4>
        """, unsafe_allow_html=True)
        ppg = player_row.get('career_summaries.ppg', 0.0)
        rpg = player_row.get('career_summaries.rpg', 0.0)
        apg = player_row.get('career_summaries.apg', 0.0)
        bpg = player_row.get('career_summaries.bpg', 0.0)
        mpg = player_row.get('career_summaries.mpg', 0.0)
        fgp = player_row.get('career_summaries.fgp', 0.0)
        tpp = player_row.get('career_summaries.tpp', 0.0)
        ftp = player_row.get('career_summaries.ftp', 0.0)
        pts = player_row.get('career_summaries.points', 0)
        gp = player_row.get('career_summaries.gamesplayed', 0)

        st.markdown(f"""
        - **場均得分 (PPG)**：<span class="highlight-val">{ppg:.1f}</span>
        - **場均籃板 / 助攻**：`{rpg:.1f}` RPG / `{apg:.1f}` APG
        - **場均阻攻 / 時間**：`{bpg:.1f}` BPG / `{mpg:.1f}` MPG
        - **三項命中率**：FG `{fgp:.1f}%` / 3P `{tpp:.1f}%` / FT `{ftp:.1f}%`
        - **生涯總得分 / 出賽**：`{int(pts):,}` 分 / `{int(gp)}` 場
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 完整欄位資料預覽與表格展示
# ==========================================
st.subheader("📑 完整欄位資料預覽 (Data Preview)")

st.caption(f"以下展示將寫入 `.xlsx` 檔案的完整欄位資料（共 {len(target_df)} 筆資料，{len(target_df.columns)} 個欄位）：")

# 格式化欄位呈現
st.dataframe(
    target_df,
    use_container_width=True,
    hide_index=False
)

# ==========================================
# 3 表結構關聯與欄位說明
# ==========================================
with st.expander("🔍 點此檢視 Supabase 3 表 Inner Join 關聯架構說明", expanded=False):
    st.markdown("""
    #### 關聯架構 (Inner Join Architecture)
    1. **`players` 表**：儲存球員主體資料（`personid`, `firstname`, `lastname`, `jersey`, `heightmeters`, `weightkilograms`, `teamid` 等）。
    2. **`career_summaries` 表**：儲存球員生涯統計（`ppg`, `rpg`, `apg`, `bpg`, `points`, `gamesplayed`, `fgp`, `ftp`, `tpp` 等），透過 `personid` 與 `players` 關聯。
    3. **`teams` 表**：儲存球隊資訊（`teamid`, `fullname`, `tricode`, `city`, `confname`, `divname` 等），透過 `teamid` 與 `players` 關聯。

    ```sql
    -- 等效 SQL 查詢語法
    SELECT *
    FROM nba.players p
    INNER JOIN nba.career_summaries cs ON p.personid = cs.personid
    INNER JOIN nba.teams t ON p.teamid = t.teamid;
    ```
    """)
