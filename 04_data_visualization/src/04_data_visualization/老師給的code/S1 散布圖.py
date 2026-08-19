import plotly.express as px
import pandas as pd

# 建立範例資料
df = pd.DataFrame({
    '廣告費用': [100, 200, 300, 400, 500, 600, 700],
    '銷售額': [1200, 2500, 3100, 4000, 4500, 5200, 6100],
    '產品類別': ['A', 'A', 'B', 'B', 'C', 'C', 'C']
})

# 建立散點圖
fig = px.scatter(
    df,
    x='廣告費用',
    y='銷售額',
    color='產品類別',
    size='銷售額',
    title='廣告費用與銷售額關係圖',
    labels={'廣告費用': 'Advertising Cost', '銷售額': 'Sales'}
)

fig.show()

