import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
# 核心指標定義
# ==========================================
METRICS = ["ppg", "rpg", "apg", "bpg", "mpg"]
METRIC_NAMES = {
    "ppg": "場均得分 (PPG)",
    "rpg": "場均籃板 (RPG)",
    "apg": "場均助攻 (APG)",
    "bpg": "場均阻攻 (BPG)",
    "mpg": "場均時間 (MPG)"
}

# ==========================================
# 資料載入與快取函式
# ==========================================
@st.cache_data(ttl=600, show_spinner="正在從 Supabase 取得 NBA 球員生涯數據...")
def load_nba_player_data():
    """從 Supabase 讀取全體生涯數據最大值，並 inner join 查詢 LeBron 與 Carmelo 的完整資料。"""
    try:
        from database import supabase
    except Exception as err:
        return None, None, f"導入 database.py 失敗：{err}"

    try:
        # 1. 查詢所有球員生涯數據，計算各欄位在全體球員中的最大值
        all_summary_response = (
            supabase
            .schema("nba")
            .table("career_summaries")
            .select("ppg, rpg, apg, bpg, mpg")
            .execute()
        )
        all_summary_df = pd.DataFrame(all_summary_response.data)
        for col in METRICS:
            all_summary_df[col] = pd.to_numeric(all_summary_df[col], errors="coerce")

        max_metrics = all_summary_df[METRICS].max()

        # 2. 查詢目標球員：players inner join career_summaries
        # 使用 personid 做關聯，選取所有欄位，過濾 "LeBron", "Carmelo"
        player_response = (
            supabase
            .schema("nba")
            .table("players")
            .select("*, career_summaries!inner(*)")
            .in_("firstname", ["LeBron", "Carmelo", "Lebron", "carmelo"])
            .execute()
        )

        raw_data = player_response.data
        if not raw_data:
            return None, None, "未查詢到 LeBron 或 Carmelo 的球員資料。"

        # 3. 展平與整理欄位
        df = pd.json_normalize(raw_data)
        # 去除 join 產生的 career_summaries. 前綴
        df.columns = [col.replace("career_summaries.", "") for col in df.columns]
        # 去除重複欄位 (如 join 兩表皆有的 personid)
        df = df.loc[:, ~df.columns.duplicated()]

        # 轉換數值型態
        for col in METRICS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df, max_metrics, None

    except Exception as err:
        return None, None, f"Supabase 查詢異常：{err}"


# ==========================================
# 載入資料
# ==========================================
df, max_metrics, error_msg = load_nba_player_data()

# ==========================================
# 頁面標題與 Hero Banner
# ==========================================
st.markdown(
    """
    <style>
    .player-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FDB927 0%, #552583 45%, #002B5C 75%, #F58426 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="player-header">🏀 NBA 03梯絕代雙驕：LeBron James vs Carmelo Anthony</div>', unsafe_allow_html=True)
st.caption("透過 Supabase 資料庫 Join 查詢生涯數據，並以全聯盟歷史最大值標準化 5 大核心指標繪製 Plotly 雷達圖")

if error_msg:
    st.error(f"❌ {error_msg}")
    st.info("💡 請確認 `.env` 中的 `SUPABASE_URL` 與 `SUPABASE_PUBLISHABLE_KEY` 是否設定正確。")
    st.stop()

st.divider()

# ==========================================
# 數據標準化計算
# ==========================================
# 複製基礎資料並計算標準化評分 (0-10 分)
scaled_df = df[["firstname", "lastname", "temporarydisplayname"] + METRICS].copy()
for col in METRICS:
    max_val = max_metrics[col]
    if pd.notnull(max_val) and max_val > 0:
        scaled_df[f"{col}_score"] = (scaled_df[col] / max_val) * 10
    else:
        scaled_df[f"{col}_score"] = 0

# ==========================================
# 雙雄核心概覽對比卡片
# ==========================================
st.subheader("⚡ 雙雄關鍵生涯概況")

c_col1, c_col2 = st.columns(2)

lebron_match = df[df["firstname"].str.lower() == "lebron"]
carmelo_match = df[df["firstname"].str.lower() == "carmelo"]

lebron_row = lebron_match.iloc[0] if not lebron_match.empty else None
carmelo_row = carmelo_match.iloc[0] if not carmelo_match.empty else None

with c_col1:
    with st.container(border=True):
        st.markdown("### 👑 LeBron James")
        if lebron_row is not None:
            st.caption(f"身高: {lebron_row.get('heightmeters', 'N/A')} m | 體重: {lebron_row.get('weightkilograms', 'N/A')} kg | 選秀: {lebron_row.get('nbadebutyear', '2003')} 年 (狀元)")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("PPG 得分", f"{lebron_row['ppg']:.1f}")
            m2.metric("RPG 籃板", f"{lebron_row['rpg']:.1f}")
            m3.metric("APG 助攻", f"{lebron_row['apg']:.1f}")
            m4.metric("BPG 阻攻", f"{lebron_row['bpg']:.1f}")
            m5.metric("MPG 時間", f"{lebron_row['mpg']:.1f}")

with c_col2:
    with st.container(border=True):
        st.markdown("### 🎯 Carmelo Anthony")
        if carmelo_row is not None:
            st.caption(f"身高: {carmelo_row.get('heightmeters', 'N/A')} m | 體重: {carmelo_row.get('weightkilograms', 'N/A')} kg | 選秀: {carmelo_row.get('nbadebutyear', '2003')} 年 (探花)")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("PPG 得分", f"{carmelo_row['ppg']:.1f}")
            m2.metric("RPG 籃板", f"{carmelo_row['rpg']:.1f}")
            m3.metric("APG 助攻", f"{carmelo_row['apg']:.1f}")
            m4.metric("BPG 阻攻", f"{carmelo_row['bpg']:.1f}")
            m5.metric("MPG 時間", f"{carmelo_row['mpg']:.1f}")

st.divider()

# ==========================================
# 互動控制與參數設定
# ==========================================
with st.expander("⚙️ 圖表視覺與標準化設定", expanded=False):
    opt_col1, opt_col2, opt_col3 = st.columns(3)
    with opt_col1:
        scale_type = st.radio(
            "標準化刻度範圍：",
            options=["0 - 10 分制", "0 - 100 百分制"],
            index=0
        )
    with opt_col2:
        fill_opacity = st.slider("雷達圖區域透明度 (Opacity)：", min_value=0.1, max_value=0.8, value=0.4, step=0.05)
    with opt_col3:
        chart_theme = st.selectbox(
            "圖表佈景主題：",
            options=["plotly_white", "plotly_dark", "ggplot2", "seaborn"],
            index=0
        )

# 依據刻度選擇調整分數倍率
score_multiplier = 10.0 if scale_type == "0 - 10 分制" else 100.0
score_max_range = 10 if scale_type == "0 - 10 分制" else 100

for col in METRICS:
    max_val = max_metrics[col]
    scaled_df[f"{col}_display_score"] = (scaled_df[col] / max_val) * score_multiplier

# 轉換為長表格供 Plotly 繪圖
records = []
for _, row in scaled_df.iterrows():
    p_name = f"{row['firstname']} {row['lastname']}"
    for col in METRICS:
        records.append({
            "球員": p_name,
            "firstname": row["firstname"],
            "指標代碼": col,
            "指標名稱": METRIC_NAMES[col],
            "標準化評分": round(row[f"{col}_display_score"], 2),
            "生涯真實數值": row[col],
            "聯盟歷史最大值": max_metrics[col]
        })

df_melt = pd.DataFrame(records)

# ==========================================
# 頁籤分頁展示
# ==========================================
tab_radar, tab_table, tab_benchmarks, tab_raw_db = st.tabs([
    "🎯 雙雄生涯能力雷達圖",
    "📊 5 大指標詳細對照表",
    "📈 全聯盟歷史最大值基準",
    "📋 Supabase 完整關聯資料"
])

# ------------------------------------------
# Tab 1: 雷達圖
# ------------------------------------------
with tab_radar:
    # 自訂球員配色 (LeBron: 湖人紫 / Carmelo: 金橙)
    color_map = {
        "LeBron James": "#7F3FBF",
        "Carmelo Anthony": "#FF7F0E",
        "LeBron": "#7F3FBF",
        "Carmelo": "#FF7F0E"
    }

    fig = px.line_polar(
        df_melt,
        r="標準化評分",
        theta="指標名稱",
        color="球員",
        line_close=True,
        markers=True,
        color_discrete_map=color_map,
        template=chart_theme,
        title=f"LeBron James vs Carmelo Anthony 生涯 5 大維度能力雷達圖 ({scale_type})",
        hover_data={
            "標準化評分": ":.2f",
            "生涯真實數值": ":.1f",
            "聯盟歷史最大值": ":.1f",
            "球員": True,
            "指標名稱": True
        }
    )

    fig.update_traces(fill="toself", opacity=fill_opacity)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, score_max_range],
                tickfont=dict(size=11),
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        ),
        height=620,
        hoverlabel=dict(bgcolor="white", font_size=13)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > **💡 雷達圖深入解讀**：
    > 1. **全能王者 (LeBron James)**：在**助攻 (APG)**、**籃板 (RPG)** 與**上場時間 (MPG)** 上展現出極致的全能身手，且生涯場均得分高達 27.1 分。
    > 2. **進攻萬花筒 (Carmelo Anthony)**：生涯場均得分達 22.5 分，具備頂級的外圍與中距離單打終結能力，並具備優異的進攻籃板意識。
    > 3. **標準化邏輯**：各項指標是以全體 NBA 球員生涯最高紀錄（如得分、助攻、阻攻之聯盟歷史峰值）為 100% 進行相對評分縮放。
    """)

# ------------------------------------------
# Tab 2: 5大指標詳細對照表
# ------------------------------------------
with tab_table:
    st.markdown("#### 🔍 5 大維度指標深度對照")
    
    comparison_data = []
    for col in METRICS:
        lb_val = lebron_row[col] if lebron_row is not None else 0
        mel_val = carmelo_row[col] if carmelo_row is not None else 0
        max_v = max_metrics[col]
        
        lb_score = (lb_val / max_v) * 10
        mel_score = (mel_val / max_v) * 10
        diff = lb_val - mel_val
        leader = "👑 LeBron" if diff > 0 else ("🎯 Carmelo" if diff < 0 else "平手")
        
        comparison_data.append({
            "指標": METRIC_NAMES[col],
            "LeBron 生涯值": f"{lb_val:.1f}",
            "Carmelo 生涯值": f"{mel_val:.1f}",
            "聯盟歷史最大值": f"{max_v:.1f}",
            "LeBron 評分 (0-10)": f"{lb_score:.2f}",
            "Carmelo 評分 (0-10)": f"{mel_score:.2f}",
            "差異 (LeBron - Carmelo)": f"{diff:+.1f}",
            "領先者": leader
        })
        
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ------------------------------------------
# Tab 3: 全聯盟基準
# ------------------------------------------
with tab_benchmarks:
    st.markdown("#### 📏 全體球員 Career Summaries 最大值基準數據")
    st.caption("以下數值取自 Supabase `career_summaries` 資料表，作為雷達圖各指標之標準化分母")
    
    bench_records = []
    for col in METRICS:
        bench_records.append({
            "指標代碼": col,
            "指標中文名稱": METRIC_NAMES[col],
            "全體球員生涯最大值": max_metrics[col]
        })
    
    bench_df = pd.DataFrame(bench_records)
    st.table(bench_df)

# ------------------------------------------
# Tab 4: 完整資料庫欄位與匯出
# ------------------------------------------
with tab_raw_db:
    st.markdown("#### 📑 Supabase `players` INNER JOIN `career_summaries` 完整結果")
    st.caption(f"共包含 {df.shape[1]} 個欄位，涵蓋個人基本資料 (姓名、生日、身高、體重、選秀年) 與生涯累積數據")
    
    st.dataframe(df, use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 下載 LeBron & Carmelo 完整生涯數據 CSV",
        data=csv_bytes,
        file_name="lebron_carmelo_career_data.csv",
        mime="text/csv"
    )
