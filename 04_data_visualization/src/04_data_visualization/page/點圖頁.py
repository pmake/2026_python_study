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
st.title("📊 Iris 鳶尾花 Plotly 互動點圖")
st.caption("利用 Plotly Express 強大的多維度散佈圖（Scatter Plot）進行資料探索與視覺化")

st.markdown("""
點圖（散佈圖，Scatter Plot）是資料分析中最常用的圖表之一，能夠直觀呈現**兩組或多組連續變數之間的相關性、分群聚集與離群值分佈**。
""")

st.divider()

# ==========================================
# 互動控制面板
# ==========================================
st.subheader("🎛️ 散佈圖參數設定面板")

# 特徵中文名稱映射字典
feature_map = {
    "sepal_length": "花萼長度 (sepal_length)",
    "sepal_width": "花萼寬度 (sepal_width)",
    "petal_length": "花瓣長度 (petal_length)",
    "petal_width": "花瓣寬度 (petal_width)"
}
feature_keys = list(feature_map.keys())

ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)

with ctrl_col1:
    x_axis = st.selectbox(
        "📌 選擇 X 軸特徵：",
        options=feature_keys,
        index=0,
        format_func=lambda k: feature_map[k]
    )

with ctrl_col2:
    y_axis = st.selectbox(
        "📌 選擇 Y 軸特徵：",
        options=feature_keys,
        index=1,
        format_func=lambda k: feature_map[k]
    )

with ctrl_col3:
    size_choice = st.selectbox(
        "🔵 點大小維度 (Size)：",
        options=["無 (固定大小)"] + feature_keys,
        index=3, # 預設 petal_length
        format_func=lambda k: "固定大小" if k == "無 (固定大小)" else feature_map[k]
    )

with ctrl_col4:
    marginal_choice = st.selectbox(
        "📐 邊緣分佈圖 (Marginal)：",
        options=["violin", "box", "histogram", "rug", "無 (none)"],
        index=0
    )

adv_col1, adv_col2, adv_col3 = st.columns(3)

with adv_col1:
    trendline_option = st.selectbox(
        "📈 趨勢擬合線 (Trendline)：",
        options=["無 (None)", "ols (線性回歸)", "lowess (局部加權回歸)"],
        index=0
    )

with adv_col2:
    template_choice = st.selectbox(
        "🎨 圖表主題風格 (Template)：",
        options=["plotly_white", "plotly_dark", "simple_white", "ggplot2", "seaborn"],
        index=0
    )

with adv_col3:
    selected_species = st.multiselect(
        "🌺 品種篩選 (Species)：",
        options=df['species'].unique().tolist(),
        default=df['species'].unique().tolist()
    )

# 篩選資料
chart_df = df[df['species'].isin(selected_species)].copy()

st.divider()

# ==========================================
# 多頁籤圖表展示 (Tabs)
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📈 2D 互動散佈圖 (主要)",
    "🧩 散佈圖矩陣 (Scatter Matrix)",
    "🌐 3D 立體散點圖 (3D Scatter)"
])

# ------------------------------------------
# Tab 1: 2D 互動散佈圖
# ------------------------------------------
with tab1:
    if chart_df.empty:
        st.warning("⚠️ 請至少選擇一個品種以顯示圖表！")
    else:
        # 設定 scatter 參數
        scatter_kwargs = {
            "data_frame": chart_df,
            "x": x_axis,
            "y": y_axis,
            "color": "species",
            "color_discrete_map": {
                "setosa": "#636EFA",
                "versicolor": "#EF553B",
                "virginica": "#00CC96"
            },
            "hover_data": ["species_id", "petal_length", "petal_width", "sepal_length", "sepal_width"],
            "title": f"🌸 Iris 鳶尾花特徵關係點圖：{feature_map[x_axis]} vs {feature_map[y_axis]}",
            "template": template_choice,
            "labels": {k: v.split(" ")[0] for k, v in feature_map.items()}
        }

        if size_choice != "無 (固定大小)":
            scatter_kwargs["size"] = size_choice

        if marginal_choice != "無 (none)":
            scatter_kwargs["marginal_x"] = marginal_choice
            scatter_kwargs["marginal_y"] = marginal_choice

        if trendline_option.startswith("ols"):
            scatter_kwargs["trendline"] = "ols"
        elif trendline_option.startswith("lowess"):
            scatter_kwargs["trendline"] = "lowess"

        fig_scatter = px.scatter(**scatter_kwargs)
        fig_scatter.update_layout(
            height=620,
            legend_title_text="品種 (Species)",
            hoverlabel=dict(bgcolor="white", font_size=12)
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("""
        > **💡 圖表觀察要點**：
        > 1. **山鳶尾 (Setosa)** 在花瓣長度與寬度上具有非常明顯的獨立聚類特徵，與另外兩種完全線性可分。
        > 2. **變色鳶尾 (Versicolor)** 與 **維吉尼亞鳶尾 (Virginica)** 在花萼尺寸上有一定重疊，但在花瓣尺寸上能呈現出清晰的分界梯度。
        """)

# ------------------------------------------
# Tab 2: 散佈圖矩陣
# ------------------------------------------
with tab2:
    st.markdown("#### 🔍 全特徵散佈圖矩陣 (Pairplot / Scatter Matrix)")
    st.caption("同時觀察花萼長度、花萼寬度、花瓣長度、花瓣寬度兩兩組合的散佈關係與對角線分佈")
    
    if not chart_df.empty:
        fig_matrix = px.scatter_matrix(
            chart_df,
            dimensions=feature_keys,
            color="species",
            color_discrete_map={
                "setosa": "#636EFA",
                "versicolor": "#EF553B",
                "virginica": "#00CC96"
            },
            title="Iris 鳶尾花全特徵散佈圖矩陣",
            template=template_choice,
            labels={k: v.split(" ")[0] for k, v in feature_map.items()}
        )
        fig_matrix.update_layout(height=750)
        st.plotly_chart(fig_matrix, use_container_width=True)

# ------------------------------------------
# Tab 3: 3D 立體散點圖
# ------------------------------------------
with tab3:
    st.markdown("#### 🌐 3D 空間特徵散點圖")
    st.caption("在三維空間中自由旋轉視角，直觀感受三品種的立體聚類形態")
    
    if not chart_df.empty:
        fig_3d = px.scatter_3d(
            chart_df,
            x="sepal_length",
            y="sepal_width",
            z="petal_length",
            size="petal_width",
            color="species",
            color_discrete_map={
                "setosa": "#636EFA",
                "versicolor": "#EF553B",
                "virginica": "#00CC96"
            },
            title="Iris 3D 特徵分佈圖 (X:花萼長, Y:花萼寬, Z:花瓣長, Size:花瓣寬)",
            template=template_choice,
            labels={k: v.split(" ")[0] for k, v in feature_map.items()}
        )
        fig_3d.update_layout(height=650)
        st.plotly_chart(fig_3d, use_container_width=True)
