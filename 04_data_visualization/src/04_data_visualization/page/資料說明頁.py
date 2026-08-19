import streamlit as st
import plotly.express as px
import pandas as pd

# ==========================================
# 載入資料
# ==========================================
@st.cache_data
def load_iris_data():
    """載入 Plotly 內建的 Iris 資料集。"""
    return px.data.iris()

df = load_iris_data()

# ==========================================
# 頁面標題與簡介
# ==========================================
st.title("📋 Iris 鳶尾花資料集說明")
st.caption("基於 Plotly 內建的 Fisher's Iris 經典統計與機器學習資料集")

st.markdown("""
**Iris 鳶尾花資料集**（由英國統計學家兼生物學家 Ronald Fisher 於 1936 年提出）是資料科學與機器學習領域最著名的經典資料集之一。
此資料集常用於**分類演算法（Classification）**、**群聚分析（Clustering）**以及**多維度探索性資料分析（EDA）**。
""")

st.divider()

# ==========================================
# 關鍵指標概覽 (Metrics)
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📊 總樣本筆數", value=f"{len(df)} 筆")
with col2:
    st.metric(label="📏 數值特徵數", value="4 個")
with col3:
    st.metric(label="🌸 品種數量", value=f"{df['species'].nunique()} 種")
with col4:
    st.metric(label="🔍 缺失值 (NaN)", value=f"{df.isnull().sum().sum()} 筆")

st.divider()

# ==========================================
# 欄位對照說明表
# ==========================================
st.subheader("📖 欄位詳細定義與說明")

field_desc = pd.DataFrame({
    "欄位名稱 (Column)": ["sepal_length", "sepal_width", "petal_length", "petal_width", "species", "species_id"],
    "中文說明 (Description)": ["花萼長度", "花萼寬度", "花瓣長度", "花瓣寬度", "鳶尾花品種名稱", "品種編號"],
    "資料型態 (Type)": ["Float (連續數值)", "Float (連續數值)", "Float (連續數值)", "Float (連續數值)", "String (類別標籤)", "Integer (類別編號)"],
    "單位 / 類別值": ["公分 (cm)", "公分 (cm)", "公分 (cm)", "公分 (cm)", "setosa / versicolor / virginica", "1 / 2 / 3"]
})

st.table(field_desc)

st.divider()

# ==========================================
# 互動式資料檢視與過濾
# ==========================================
st.subheader("🔍 互動式 DataFrame 檢視")

with st.expander("⚙️ 點此開啟 / 收合資料過濾選項", expanded=True):
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        species_options = df['species'].unique().tolist()
        selected_species = st.multiselect(
            "選擇要檢視的品種：",
            options=species_options,
            default=species_options
        )
    with f_col2:
        petal_length_range = st.slider(
            "花瓣長度 (petal_length) 區間篩選：",
            min_value=float(df['petal_length'].min()),
            max_value=float(df['petal_length'].max()),
            value=(float(df['petal_length'].min()), float(df['petal_length'].max())),
            step=0.1
        )

# 篩選資料
filtered_df = df[
    (df['species'].isin(selected_species)) &
    (df['petal_length'] >= petal_length_range[0]) &
    (df['petal_length'] <= petal_length_range[1])
]

st.info(f"💡 目前篩選條件下共有 **{len(filtered_df)}** 筆資料（佔全部 {len(df)} 筆的 {len(filtered_df)/len(df)*100:.1f}%）。")

# 顯示 DataFrame
st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "sepal_length": st.column_config.NumberColumn("花萼長度 (cm)", format="%.2f cm"),
        "sepal_width": st.column_config.NumberColumn("花萼寬度 (cm)", format="%.2f cm"),
        "petal_length": st.column_config.NumberColumn("花瓣長度 (cm)", format="%.2f cm"),
        "petal_width": st.column_config.NumberColumn("花瓣寬度 (cm)", format="%.2f cm"),
        "species": st.column_config.TextColumn("品種名稱"),
        "species_id": st.column_config.NumberColumn("品種 ID"),
    },
    hide_index=False
)

# 下載 CSV 功能
csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 下載目前篩選的 CSV 資料",
    data=csv_data,
    file_name="iris_filtered_data.csv",
    mime="text/csv",
)

st.divider()

# ==========================================
# 統計分析與分佈摘要
# ==========================================
st.subheader("📊 特徵統計分析與分佈摘要")

stat_col1, stat_col2 = st.columns([3, 2])

with stat_col1:
    st.markdown("##### 📈 數值特徵描述性統計 (Describe)")
    st.dataframe(
        filtered_df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].describe().T,
        use_container_width=True
    )

with stat_col2:
    st.markdown("##### 🌺 各品種樣本數量分佈")
    species_counts = filtered_df['species'].value_counts().reset_index()
    species_counts.columns = ['品種', '數量']
    
    fig_pie = px.pie(
        species_counts,
        names='品種',
        values='數量',
        color='品種',
        color_discrete_map={
            'setosa': '#636EFA',
            'versicolor': '#EF553B',
            'virginica': '#00CC96'
        },
        hole=0.4,
        title="品種比例"
    )
    fig_pie.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=260)
    st.plotly_chart(fig_pie, use_container_width=True)
