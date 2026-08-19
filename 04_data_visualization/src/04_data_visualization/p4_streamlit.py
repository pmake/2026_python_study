import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 頁面基本設定 (全域配置)
# ==========================================
st.set_page_config(
    page_title="Streamlit × Plotly × Pandas 數據視覺化",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 首頁內容定義函數
# ==========================================
def home():
    """顯示應用首頁，詳細說明 Streamlit、Plotly 與 Pandas 的結合與協同應用。"""
    
    # 自訂美化樣式 (CSS)
    st.markdown(
        """
        <style>
        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(120deg, #FF4B4B 0%, #FF8F00 40%, #1E88E5 80%, #9C27B0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        .hero-desc {
            font-size: 1.15rem;
            color: #555;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        .tech-card {
            border-radius: 12px;
            padding: 1.25rem;
            background: rgba(240, 244, 248, 0.5);
            border: 1px solid rgba(0, 0, 0, 0.08);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .tech-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        }
        .step-box {
            background-color: #f8f9fa;
            border-left: 4px solid #1E88E5;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="hero-title">🌺 Streamlit × Plotly × Pandas 現代數據視覺化</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-desc">探索 Python 現代資料科學生態系的「黃金三角」：數據處理、互動圖表與網頁儀表板的一站式極速整合。</div>',
        unsafe_allow_html=True
    )
    
    st.divider()

    # ------------------------------------------
    # 三大核心工具的黃金三角介紹
    # ------------------------------------------
    st.subheader("💡 核心架構：現代 Python 數據應用的黃金三角")
    st.markdown("當代資料科學家與軟體工程師不再需要複雜的前後端分離架構，透過以下三大核心庫即可高效構建全功能互動應用：")

    t_col1, t_col2, t_col3 = st.columns(3)

    with t_col1:
        st.markdown("""
        <div class="tech-card">
            <h3>🐼 1. Pandas</h3>
            <p><strong>【數據核心與清洗引擎】</strong></p>
            <ul>
                <li><strong>高效率資料操作</strong>：提供強大的 <code>DataFrame</code> 與 <code>Series</code> 資料結構。</li>
                <li><strong>靈活數據清洗</strong>：輕鬆處理缺失值、型態轉換、篩選與特徵工程。</li>
                <li><strong>聚合與統計計算</strong>：一鍵完成分組統計 (<code>groupby</code>) 與敘述性統計 (<code>describe</code>)。</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with t_col2:
        st.markdown("""
        <div class="tech-card">
            <h3>📈 2. Plotly</h3>
            <p><strong>【高互動專業圖表引擎】</strong></p>
            <ul>
                <li><strong>豐富互動體驗</strong>：原生支援縮放 (Zoom)、平移 (Pan)、框選與懸停資訊 (Hover Tooltips)。</li>
                <li><strong>Plotly Express 極簡語法</strong>：幾行 Python 程式碼即可繪製多維度點圖、箱型圖與 3D 圖。</li>
                <li><strong>高品質出版級輸出</strong>：支援自訂顏色對照 (Color Map)、邊緣分佈圖與主題風格。</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with t_col3:
        st.markdown("""
        <div class="tech-card">
            <h3>🚀 3. Streamlit</h3>
            <p><strong>【極速 Web 介面與導航】</strong></p>
            <ul>
                <li><strong>純 Python 開發</strong>：完全無需 HTML/CSS/JavaScript，快速將腳本轉化為 Web App。</li>
                <li><strong>豐富互動元件</strong>：按鈕、滑桿、多選清單、分頁 (Tabs) 與分欄 (Columns) 即時響應。</li>
                <li><strong>官方新版 Navigation API</strong>：簡潔的 <code>st.navigation</code> 與 <code>st.Page</code> 多頁面架構。</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ------------------------------------------
    # 協同運作流程展示
    # ------------------------------------------
    st.subheader("🔄 三者如何協同運作 (Workflow)")
    
    w_col1, w_col2, w_col3 = st.columns(3)

    with w_col1:
        st.markdown("""
        <div class="step-box">
            <h4>步驟 1：Pandas 載入與處理</h4>
            <p>從資料庫或內建資料集讀取數據，進行過濾與聚合計算。</p>
            <code>df = px.data.iris()</code><br>
            <code>filtered_df = df[df['species'] == 'setosa']</code>
        </div>
        """, unsafe_allow_html=True)

    with w_col2:
        st.markdown("""
        <div class="step-box">
            <h4>步驟 2：Plotly 建立互動圖表</h4>
            <p>將清洗後的 DataFrame 傳入 Plotly 函式，生成圖表物件 (Figure)。</p>
            <code>fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")</code>
        </div>
        """, unsafe_allow_html=True)

    with w_col3:
        st.markdown("""
        <div class="step-box">
            <h4>步驟 3：Streamlit 封裝呈現</h4>
            <p>透過 Streamlit 元件控制參數，並在網頁中即時渲染展示。</p>
            <code>st.dataframe(filtered_df)</code><br>
            <code>st.plotly_chart(fig, use_container_width=True)</code>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ------------------------------------------
    # 頁面快速導覽區
    # ------------------------------------------
    st.subheader("🧭 快速導航與體驗指南")
    st.info("👈 請利用左側邊欄的 **Navigation 導航選單** 切換頁面，或點擊下方卡片直接探索：")

    g_col1, g_col2 = st.columns(2)

    with g_col1:
        with st.container(border=True):
            st.markdown("### 📋 資料說明頁 (`page/資料說明頁.py`)")
            st.markdown("""
            - 展示 Plotly 內建的經典 **Fisher's Iris (鳶尾花)** 資料集
            - 包含關鍵指標統計、欄位定義對照表、互動篩選與 CSV 檔案下載
            """)
            st.caption("路徑：`page/資料說明頁.py`")

    with g_col2:
        with st.container(border=True):
            st.markdown("### 📊 點圖頁 (`page/點圖頁.py`)")
            st.markdown("""
            - 根據 Iris 鳶尾花資料集製作 Plotly 多維度互動點圖 (Scatter Plot)
            - 支援自訂 X/Y 軸、點大小、邊緣分佈圖 (Violin/Box)、趨勢線、3D 立體點圖與散佈圖矩陣
            """)
            st.caption("路徑：`page/點圖頁.py`")


# ==========================================
# 官方新版 Navigation API 設定
# ==========================================
# 依據 P4_streamlit.md 規定：
# - 首頁裡面要放入：
#   - 資料說明頁，路徑在 page/資料說明頁.py
#   - 點圖頁，路徑在 page/點圖頁.py
#   - 做出 navigation
#   - 使用 Streamlit 新版官方 Navigation API
pages = {
    "導航選單": [
        st.Page(home, title="首頁", icon="🏠", default=True),
        st.Page("page/資料說明頁.py", title="資料說明頁", icon="📋"),
        st.Page("page/點圖頁.py", title="點圖頁", icon="📊"),
    ]
}

# 建立導航並執行當前頁面
current_page = st.navigation(pages)
current_page.run()
