import streamlit as st

st.sidebar.title("App 說明")
st.sidebar.write("這是一個產品推薦應用")

tab1, tab2, tab3 = st.tabs(["介紹", "推薦", "熱門"])

with tab1:
    st.write("這裡介紹 App 目的")

with tab2:
    st.write("依照你的選項推薦產品")

with tab3:
    st.write("這裡顯示熱門商品排行")