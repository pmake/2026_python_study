import plotly.express as px
import pandas as pd

# 建立行銷漏斗資料
df = pd.DataFrame({
    '階段': ['廣告曝光', '點擊進站', '註冊帳號', '加入購物車', '完成購買'],
    '人數': [5000, 3200, 1800, 900, 400]
})

# 建立面積漏斗圖
fig = px.funnel_area(
    df,
    names='階段',
    values='人數',
    title='行銷轉換流程面積漏斗圖',
    color_discrete_sequence=px.colors.sequential.Bluered
)

fig.show()