import streamlit as st
import pandas as pd
import plotly.express as px

# 讀取 CSV
sales = pd.read_csv('./data/sales.csv')

# 取得所有產品類別
all_products = sales['銷售產品'].unique().tolist()

# 建立 multiselect 選單
selected_products = st.multiselect("請選擇要顯示的產品", options=all_products)

# 顯示圖表按鈕
if st.button("顯示圖表"):
    if selected_products:
        # 篩選所選的產品
        filtered_sales = sales[sales['銷售產品'].isin(selected_products)]

        # 分組彙總
        grouped = filtered_sales.groupby(['業務單位', '銷售產品'])['銷售金額'].sum().reset_index()

        # 畫圖
        fig = px.bar(
            grouped,
            x='業務單位',
            y='銷售金額',
            color='銷售產品',
            barmode='group',
            title='各業務單位各產品銷售金額'
        )

        st.plotly_chart(fig)
    else:
        st.warning("請至少選擇一個產品！")