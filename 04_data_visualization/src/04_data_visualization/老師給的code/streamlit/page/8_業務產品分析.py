import streamlit as st
import pandas as pd
import plotly.express as px

# 讀取 CSV 檔
sales = pd.read_csv('./data/sales.csv')

# 分組彙總：以「業務單位」和「銷售產品」分組，計算銷售金額總和
grouped = sales.groupby(['業務單位', '銷售產品'])['銷售金額'].sum().reset_index()

# 使用 Plotly 畫出分組柱狀圖
fig = px.bar(
    grouped,
    x='業務單位',
    y='銷售金額',
    color='銷售產品',
    barmode='group',  # 分組柱狀圖（不是堆疊）
    title='各業務單位各產品銷售金額'
)

# 顯示圖表
st.plotly_chart(fig)