import streamlit as st
import pandas as pd
import plotly.express as px

# 讀取資料
sales = pd.read_csv('./data/sales.csv')
sales.columns = ['日期', '業務單位', '員工姓名', '性別', '銷售產品', '數量', '銷售金額']

# 日期轉換與欄位處理
sales['日期'] = pd.to_datetime(sales['日期'], format="%Y-%m-%d")
# dt 是 Pandas 專門用來操作 datetime 欄位的時間元件存取器
sales['年份'] = sales['日期'].dt.year
sales['月份'] = sales['日期'].dt.month

# 選擇年份
years = sorted(sales['年份'].unique())
selected_year = st.selectbox("請選擇年份", years)

# 篩選該年份的資料
sales_by_year = sales[sales['年份'] == selected_year]

# 取得該年所有月份
available_months = sorted(sales_by_year['月份'].unique())
min_month, max_month = min(available_months), max(available_months)

# 用 slider 選擇月份區間（tuple）
selected_range = st.slider("請選擇月份區間", min_value=min_month, max_value=max_month, value=(min_month, max_month))

# 篩選該區間的資料
filtered_sales = sales_by_year[
    (sales_by_year['月份'] >= selected_range[0]) &
    (sales_by_year['月份'] <= selected_range[1])
]

# 顯示資訊
st.markdown(f"###  {selected_year} 年 {selected_range[0]} 月 ~ {selected_range[1]} 月各業務單位銷售金額")

# 分組統計
grouped = filtered_sales.groupby('業務單位')['銷售金額'].sum().reset_index()

# 繪圖
fig = px.bar(
    grouped,
    x='業務單位',
    y='銷售金額',
    title=f"{selected_year} 年 {selected_range[0]}~{selected_range[1]} 月 - 各業務單位銷售金額",
    text='銷售金額'
)

st.plotly_chart(fig, use_container_width=True)