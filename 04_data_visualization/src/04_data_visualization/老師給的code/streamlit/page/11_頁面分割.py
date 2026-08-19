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

        # 取得所有業務單位
        all_units = filtered_sales['業務單位'].unique().tolist()

        # 分成兩行兩欄（四格）
        rows = [st.columns(2), st.columns(2)]  # 共兩列，每列兩欄

        for idx, unit in enumerate(all_units):
            # 取得該單位的資料
            unit_sales = filtered_sales[filtered_sales['業務單位'] == unit]

            # 彙總
            grouped = unit_sales.groupby('銷售產品')['銷售金額'].sum().reset_index()

            # 畫圖
            fig = px.bar(
                grouped,
                x='銷售產品',
                y='銷售金額',
                title=f'業務單位：{unit}',
                text='銷售金額'
            )

            # fig.update_layout(showlegend=False)

            # 選擇要放在哪一列哪一欄
            if unit == '業務1':
                row, col = 0, 0
            elif unit == '業務3':
                row, col = 1, 0
            elif unit == '業務2':
                row, col = 0, 1
            elif unit == '業務4':
                row, col = 1, 1
     

            with rows[row][col]:
                st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("請至少選擇一個產品！")