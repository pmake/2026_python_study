import plotly.express as px
import pandas as pd

# 模擬購物流程資料
df = pd.DataFrame({
    '階段': ['瀏覽商品', '加入購物車', '進入結帳', '輸入付款資料', '完成訂單'],
    '人數': [1000, 600, 400, 300, 250]
})

# 建立漏斗圖
fig = px.funnel(
    df,
    x='人數',
    y='階段',
    title='顧客購物流程轉換漏斗圖',
    labels={'人數': 'Users', '階段': 'Stage'}
)

fig.show()