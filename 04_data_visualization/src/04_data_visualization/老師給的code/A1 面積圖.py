import plotly.express as px
import pandas as pd

# 模擬資料：三項產品的月營收
df = pd.DataFrame({
    '月份': ['1月', '2月', '3月', '4月', '5月', '6月'] * 3,
    '產品': ['A'] * 6 + ['B'] * 6 + ['C'] * 6,
    '營收': [50, 60, 70, 80, 90, 100,
           40, 55, 65, 75, 85, 95,
           30, 35, 40, 45, 50, 55]
})

# 建立面積圖
fig = px.area(
    df,
    x='月份',
    y='營收',
    color='產品',
    title='各產品月營收累積變化圖',
    labels={'營收': 'Revenue', '月份': 'Month'},
)

fig.show()