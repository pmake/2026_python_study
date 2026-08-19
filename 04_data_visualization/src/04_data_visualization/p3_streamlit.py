import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 頁面基本設定
# ==========================================
st.set_page_config(
    page_title="Streamlit 的功能介紹",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 自訂美化樣式 (CSS)
# ==========================================
st.markdown(
    """
    <style>
    /* 全局字體與平滑滾動 */
    html {
        scroll-behavior: smooth;
    }
    
    /* 漸層標題裝飾 */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F00, #1E88E5, #9C27B0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }

    /* 亮點卡片樣式 */
    .feature-card {
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* 標籤 Badge 樣式 */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 0.85em;
        font-weight: 700;
        border-radius: 6px;
        margin-right: 0.5rem;
    }
    .badge-red { background-color: #ffebee; color: #c62828; }
    .badge-blue { background-color: #e3f2fd; color: #1565c0; }
    .badge-green { background-color: #e8f5e9; color: #2e7d32; }
    .badge-purple { background-color: #f3e5f5; color: #6a1b9a; }
    .badge-orange { background-color: #fff3e0; color: #ef6c00; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 側邊欄 (Sidebar)
# ==========================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&auto=format&fit=crop&q=80",
        caption="📊 Streamlit 數據魔法師",
        use_container_width=True,
    )
    
    st.markdown("### 🧭 快速導覽目錄")
    st.markdown("""
    - [1. 純 Python 開發](#1-python-pure-python-no-frontend)
    - [2. 即時熱重載與響應式](#2-instant-hot-reload-reactivity)
    - [3. 豐富多元的互動元件](#3-rich-interactive-widgets)
    - [4. 無縫整合各大圖表庫](#4-seamless-data-visualization)
    - [5. 智慧快取加速機制](#5-smart-caching-performance)
    - [6. 彈性靈活的排版與容器](#6-flexible-layouts-containers)
    - [7. 原生 AI 與對話介面](#7-ai-native-chat-ai-ui)
    - [8. 跨步驟狀態管理](#8-session-state-state-management)
    - [9. 多頁面架構與導航](#9-multi-page-navigation)
    - [10. 一鍵雲端免費部署](#10-one-click-cloud-deployment)
    """)
    
    st.divider()
    st.markdown("### 🎈 互動特效小工具")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        if st.button("🎉 放氣球", use_container_width=True):
            st.balloons()
    with col_sb2:
        if st.button("❄️ 下雪囉", use_container_width=True):
            st.snow()
            
    st.info("💡 **小撇步**：Streamlit 讓資料科學家在數小時內就能把 Python 腳本變成精美 Web App！")


# ==========================================
# 首頁頂部 Banner 與標題
# ==========================================
st.markdown('<div class="hero-title">🚀 Streamlit 的功能介紹</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">為機器學習、資料分析與 Python 開發者量身打造的極速 Web 應用框架 ✨</div>',
    unsafe_allow_html=True,
)

# 頂部形象圖與簡介
hero_col1, hero_col2 = st.columns([3, 2])

with hero_col1:
    st.markdown(
        """
        > 🌟 **什麼是 Streamlit？**  
        > Streamlit 是一個開源的 Python 框架，旨在讓資料科學家和 AI 工程師**完全不需要具備前端經驗（免 HTML、CSS、JS）**，
        > 就能以最直覺的 Python 程式碼，把資料分析模型、機器學習 Prototype 快速轉化為優雅強大的互動式 Web 應用程式！
        """
    )
    
    # 快速數據展示指標
    m1, m2, m3 = st.columns(3)
    m1.metric(label="⚡ 開發速度", value="10x 更快", delta="免前端技術")
    m2.metric(label="🐍 學習門檻", value="純 Python", delta="即寫即用")
    m3.metric(label="🌐 部署難度", value="0 摩擦力", delta="一鍵上雲")

with hero_col2:
    st.image(
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=700&auto=format&fit=crop&q=80",
        caption="💻 寫 Python，享全端互動網頁！",
        use_container_width=True,
    )

st.divider()

# ==========================================
# 🌟 10 大核心強調重點介紹
# ==========================================
st.subheader("🔥 Streamlit 10 大核心功能亮點", anchor="features-overview")
st.write("以下為您詳細拆解 Streamlit 最令人驚豔的 10 大功能特色與實踐技巧：")

# ------------------------------------------
# 重點 1
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 1. 🐍 純 Python 開發 (Pure Python, No Frontend)")
        st.markdown(
            "`:badge[免前端]` `:badge[超低門檻]` `:rainbow[開發體驗極佳]`"
        )
        st.markdown(
            """
            - **告別複雜前端語法**：完全無需學習 HTML、CSS、JavaScript、React 或 Vue。
            - **像寫 Script 一樣自然**：只需從上到下呼叫 `st.write()`、`st.title()`，程式執行邏輯與一般 Python 腳本無異。
            - **超強相容性**：只要是 Python 原生資料型態（dict, list, DataFrame, 物件），Streamlit 都能聰明自動渲染！
            """
        )
        st.code("import streamlit as st\n\nst.title('Hello Streamlit!')\nst.write('純 Python 打造的第一個網頁應用 🎉')", language="python")
    with col_demo:
        st.image(
            "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&auto=format&fit=crop&q=80",
            caption="純粹的 Python，無限的可能",
            use_container_width=True,
        )

# ------------------------------------------
# 重點 2
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 2. ⚡ 即時熱重載與響應式 (Instant Hot-Reload & Reactivity)")
        st.markdown(
            "`:badge[即時預覽]` `:badge[自動重繪]` `:green[開發效率倍增]`"
        )
        st.markdown(
            """
            - **存檔立即更新 (Hot-Reloading)**：只要在編輯器中按 `Ctrl + S`，瀏覽器畫面會即刻自動刷新，所見即所得。
            - **資料響應模型 (Reactivity)**：只要使用者在網頁上移動滑桿或按下按鈕，Streamlit 會自動重新從頭執行腳本並動態計算最新數值。
            - **所改即所見**：大幅縮減「修改程式 ➡️ 重啟伺服器 ➡️ 重新整理」的漫長除錯迴圈。
            """
        )
        st.info("💡 試試看右邊的互動滑桿，感受即時響應的魅力！")
    with col_demo:
        slider_val = st.slider("🎚️ 調整數值以體驗即時響應：", min_value=1, max_value=100, value=66)
        st.success(f"目前滑桿數值：**{slider_val}** (計算平方值：**{slider_val ** 2}**)")

# ------------------------------------------
# 重點 3
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 3. 🎛️ 豐富多元的互動元件 (Rich Interactive Widgets)")
        st.markdown(
            "`:badge[開箱即用]` `:badge[雙向綁定]` `:orange[元件豐富]`"
        )
        st.markdown(
            """
            - **元件種類繁多**：按鈕、滑桿、多選下拉清單、單選框、文字輸入框、檔案上傳器、顏色挑選器、日期時間挑選器。
            - **一行程式碼搞定**：只需 `user_input = st.text_input('請輸入')` 即可把使用者的輸入直接存進 Python 變數！
            - **即時回傳值**：每個元件都有返回值，直接與下游的演算法或資料管線對接。
            """
        )
        st.code("user_name = st.text_input('您的暱稱', 'Python 好手')\ncolor = st.color_picker('喜愛的代表色', '#FF4B4B')", language="python")
    with col_demo:
        demo_name = st.text_input("👤 輸入你的名字：", value="Python 大師")
        demo_color = st.color_picker("🎨 選擇你的幸運色：", "#FF4B4B")
        st.markdown(f"哈囉 <span style='color:{demo_color}; font-weight:bold; font-size:1.2rem;'>{demo_name}</span>！歡迎體驗 Streamlit！", unsafe_allow_html=True)

# ------------------------------------------
# 重點 4
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 4. 📊 無縫整合各大圖表庫 (Seamless Data Visualization)")
        st.markdown(
            "`:badge[視覺化神兵]` `:badge[全圖表支援]` `:blue[互動圖表]`"
        )
        st.markdown(
            """
            - **全方位支援熱門套件**：完美整合 **Plotly, Matplotlib, Seaborn, Altair, Bokeh, PyDeck, ECharts** 等。
            - **原生互動式圖表**：內建 `st.line_chart()`, `st.bar_chart()`, `st.area_chart()`, `st.map()`，傳入 Pandas DataFrame 即可自動繪圖。
            - **縮放與懸浮檢視**：圖表支援游標懸停 (Tooltip)、放大縮小、動態篩選，給使用者頂級的資料探索體驗！
            """
        )
    with col_demo:
        chart_data = pd.DataFrame(
            np.random.randn(20, 3) + [10, 15, 20],
            columns=["📈 產品 A", "📊 產品 B", "🚀 產品 C"]
        )
        st.line_chart(chart_data, height=220)

# ------------------------------------------
# 重點 5
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 5. 🚀 智慧快取加速機制 (Smart Caching & Performance)")
        st.markdown(
            "`:badge[@st.cache_data]` `:badge[@st.cache_resource]` `:violet[極速效能]`"
        )
        st.markdown(
            """
            - **解決重複運算瓶頸**：針對耗時的模型載入、SQL 查詢、大型 CSV 讀取，使用裝飾器智慧快取結果。
            - `@st.cache_data`：專為可序列化資料（如 DataFrame、字典、陣列、計算結果）設計。
            - `@st.cache_resource`：專門快取不可序列化的全域資源（如資料庫連線池、大型 ML/深度學習模型權重）。
            - **智慧失效偵測**：當函式程式碼或輸入參數改變時，自動重新計算並更新快取。
            """
        )
        st.code("@st.cache_data\ndef load_huge_dataset(url):\n    return pd.read_csv(url)\n\n# 只有第一次會讀取，之後秒開！", language="python")
    with col_demo:
        st.image(
            "https://images.unsplash.com/photo-1517976487504-59a1a08420e7?w=600&auto=format&fit=crop&q=80",
            caption="🚀 善用快取，讓 App 像火箭般極速奔馳",
            use_container_width=True,
        )

# ------------------------------------------
# 重點 6
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 6. 🧱 彈性靈活的排版與容器 (Flexible Layouts & Containers)")
        st.markdown(
            "`:badge[分欄佈局]` `:badge[分頁籤 Tabs]` `:red[儀表板架構]`"
        )
        st.markdown(
            """
            - **多樣排版容器**：
              - `st.columns()`：輕鬆切分多欄，製作如專業商業儀表板的並排版面。
              - `st.tabs()`：分頁籤切換不同維度的分析內容，保持頁面乾淨整潔。
              - `st.expander()`：可收折的詳細資訊區塊，節省螢幕空間。
              - `st.sidebar`：側邊欄放置全域控制選單。
              - `st.container(border=True)`：精緻的卡片式容器。
            """
        )
    with col_demo:
        tab1, tab2, tab3 = st.tabs(["🌟 特色 A", "📊 特色 B", "💡 特色 C"])
        with tab1:
            st.write("這是 **分頁籤 1** 的內容：整齊劃一的排版！")
        with tab2:
            st.write("這是 **分頁籤 2** 的內容：支援在各分頁放置不同的圖表。")
        with tab3:
            st.write("這是 **分頁籤 3** 的內容：點擊即時無縫切換！")

# ------------------------------------------
# 重點 7
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 7. 🤖 原生 AI 與對話介面 (Native Chat & AI UI)")
        st.markdown(
            "`:badge[LLM 必備]` `:badge[st.chat_message]` `:green[對話式 UI]`"
        )
        st.markdown(
            """
            - **一秒打造 ChatGPT 介面**：內建 `st.chat_message()` 與 `st.chat_input()`，是目前打造 LLM / GenAI 最受歡迎的框架。
            - **串流打字機效果 (Streaming)**：支援 `st.write_stream()`，讓大型語言模型生成的文字像打字機一樣逐字流暢輸出！
            - **多代理人與多角色對話**：可自訂頭像 (Avatar) 與角色名稱 (user, assistant, tool)。
            """
        )
        st.code('with st.chat_message("assistant"):\n    st.write("哈囉！我是您的 Streamlit 智慧助手 🤖")', language="python")
    with col_demo:
        with st.chat_message("user"):
            st.write("如何用 Streamlit 打造 AI 應用？")
        with st.chat_message("assistant", avatar="🤖"):
            st.write("只需要 `st.chat_message` 與 `st.chat_input`，3 分鐘搞定！🎉")

# ------------------------------------------
# 重點 8
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 8. 💾 跨步驟狀態管理 (`st.session_state`)")
        st.markdown(
            "`:badge[狀態保存]` `:badge[多步驟表單]` `:blue[資料持久化]`"
        )
        st.markdown(
            """
            - **記憶使用者操作歷程**：在每次頁面重繪時，透過 `st.session_state` 保留購物車清單、登入狀態或計數器。
            - **字典式直覺存取**：支援 `st.session_state['key'] = value` 或屬性式 `st.session_state.key`。
            - **支援回呼函式 (Callbacks)**：可在按鈕點擊或輸入變更時，觸發特定的 Python 函式處理商業邏輯。
            """
        )
    with col_demo:
        if "counter" not in st.session_state:
            st.session_state.counter = 0
            
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            if st.button("➕ 點擊計數 +1", use_container_width=True):
                st.session_state.counter += 1
        with c_col2:
            if st.button("🔄 重設歸零", use_container_width=True):
                st.session_state.counter = 0
                
        st.metric(label="🎯 跨重繪計數器", value=st.session_state.counter)

# ------------------------------------------
# 重點 9
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 9. 📑 多頁面架構與導航 (Multi-Page & `st.navigation`)")
        st.markdown(
            "`:badge[企業級架構]` `:badge[st.navigation]` `:violet[模組化管理]`"
        )
        st.markdown(
            """
            - **靈活的多頁面組織**：透過 `pages/` 資料夾或新一代 `st.navigation()` / `st.Page()`，輕鬆構建大型多功能應用。
            - **自動生成導航選單**：側邊欄自動產生漂亮的階層式導航列，支援分類分組、自訂圖示與權限控管。
            - **程式碼模組化**：不同業務頁面各自獨立檔案，方便團隊協同開發與維護。
            """
        )
        st.code('pages = {\n    "分析": [st.Page("p1.py", title="銷售總覽", icon="📊")],\n    "設定": [st.Page("p2.py", title="系統設定", icon="⚙️")]\n}\nst.navigation(pages).run()', language="python")
    with col_demo:
        st.image(
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=80",
            caption="模組化結構，建構強大的企業級應用",
            use_container_width=True,
        )

# ------------------------------------------
# 重點 10
# ------------------------------------------
with st.container(border=True):
    col_text, col_demo = st.columns([3, 2])
    with col_text:
        st.markdown("### 10. 🌐 一鍵雲端免費部署 (One-Click Cloud Deployment)")
        st.markdown(
            "`:badge[Streamlit Cloud]` `:badge[GitHub 整合]` `:orange[秒速上線]`"
        )
        st.markdown(
            """
            - **零設定雲端上線**：將程式碼推送到 GitHub，連接 **Streamlit Community Cloud**，按一下按鈕即可獲得公開網址！
            - **自動持續整合 (CI/CD)**：GitHub 程式碼一旦更新 `git push`，雲端應用會自動重新佈署。
            - **支援密鑰與環境變數管理**：提供 `st.secrets` 安全存放 API Key、資料庫連線密碼，安全無虞。
            - **多平台相容**：除了 Streamlit Cloud，也支援 Docker、AWS、GCP、Azure、HuggingFace Spaces 輕鬆容器化部屬。
            """
        )
    with col_demo:
        st.image(
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80",
            caption="🌍 讓你的 App 隨時隨地向全世界展示",
            use_container_width=True,
        )

st.divider()

# ==========================================
# 趣味互動區與結語
# ==========================================
st.subheader("🎉 立即開始你的 Streamlit 之旅！")

cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white; margin: 1rem 0;">
            <h3 style="color: white; margin-bottom: 0.5rem;">🌟 Turn Python Scripts into Beautiful Web Apps</h3>
            <p style="font-size: 1rem; opacity: 0.95;">從今天開始，用 Streamlit 釋放你的數據與 AI 潛能！</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 探索完畢！點我慶祝 🎉", use_container_width=True, type="primary"):
            st.balloons()
            st.toast("恭喜掌握 Streamlit 10 大核心技能！🥳", icon="🚀")
    with col_btn2:
        if st.button("❄️ 感受冰涼靈感 ☃️", use_container_width=True):
            st.snow()
            st.toast("保持冷靜，持續寫 Python！🐍", icon="✨")

st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.9rem; margin-top: 2rem;">
        Made with ❤️ using Streamlit & Python | 2026 Python Study
    </div>
    """,
    unsafe_allow_html=True,
)
