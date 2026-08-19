import streamlit as st


st.set_page_config(
    page_title="Streamlit 互動資料教學",
    page_icon="🎉",
    layout="wide",
)


def home():
    """顯示應用首頁。"""
    st.title("🎉 我的第一個 Streamlit App123456")
    st.write("這是用 Python 和 Streamlit 做出來的互動網頁應用！")
    st.write("開啟美妙人生！")


pages = {
    "首頁": [
        st.Page(home, title="首頁", icon="🏠", default=True),
    ],
    "DataFrame 與資料": [
        st.Page("page/1_顯示DataFrame.py", title="顯示 DataFrame", icon="📋"),
        st.Page(
            "page/2_DataFrame添加樣式.py",
            title="DataFrame 添加樣式",
            icon="🎨",
        ),
        st.Page(
            "page/3_DataFrame添加樣式2.py",
            title="DataFrame 樣式進階",
            icon="✨",
        ),
        st.Page("page/4_導入資料.py", title="導入資料", icon="📥"),
        st.Page("page/5_業務資料標注.py", title="業務資料標注", icon="📌"),
        st.Page("page/db_cloud.py", title="Cloud MySQL 資料", icon="🗄️"),
    ],
    "圖表": [
        st.Page("page/6_lineChart.py", title="Line Chart", icon="📈"),
        st.Page("page/7_Matplotlib.py", title="Matplotlib", icon="📊"),
        st.Page("page/7_plotly.py", title="Plotly", icon="💠"),
    ],
    "互動分析": [
        st.Page("page/8_業務產品分析.py", title="業務產品分析", icon="💼"),
        st.Page("page/9_互動資料選單.py", title="互動資料選單", icon="🎛️"),
        st.Page("page/11_頁面分割.py", title="多圖表分析", icon="🧩"),
        st.Page("page/12_月份選擇.py", title="月份區間選擇", icon="📅"),
    ],
    "佈局與頁面": [
        st.Page("page/10_頁面分欄.py", title="頁面分欄", icon="↔️"),
        st.Page("page/15_頁面.py", title="Tabs 頁面", icon="🗂️"),
    ],
    "動畫與即時資料": [
        st.Page("page/13_動畫.py", title="Plotly 動畫", icon="🎬"),
        st.Page("page/14_即時變動.py", title="即時變動", icon="⏱️"),
    ],
}

current_page = st.navigation(pages)
current_page.run()
