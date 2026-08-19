import plotly.express as px
import pandas as pd

# 範例資料：模擬三個維度的數據
df = pd.DataFrame({
    '銷售額': [100, 150, 200, 250, 300, 350, 400],
    '客戶滿意度': [70, 75, 80, 82, 88, 90, 95],
    '回購率': [20, 30, 40, 50, 60, 70, 80],
    '業務員': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
})

# 建立 3D 散點圖
fig = px.scatter_3d(
    df,
    x='銷售額',
    y='客戶滿意度',
    z='回購率',
    color='業務員',
    size='回購率',
    title='業務員三維績效分析',
)

fig.show()
