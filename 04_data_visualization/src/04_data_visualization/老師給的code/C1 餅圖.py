import pandas as pd
import plotly.express as px

# 創造樣板數據：各產品類別的銷售額占比（用於比例展示、組成結構分析）
df = pd.DataFrame({
    '產品類別': ['電子產品', '服飾', '食品', '書籍', '家居用品'],
    '銷售額': [350000, 280000, 220000, 150000, 100000]
})

# 圓餅圖
fig = px.pie(
    df,
    values='銷售額',      # 數值（決定扇形大小）
    names='產品類別',      # 類別（決定扇形標籤）
    title='各產品類別銷售額占比（圓餅圖）',
    hole=0.3,              # 圓環圖（0-1之間，0為實心圓餅，0.3為30%空心）
    color_discrete_sequence=px.colors.qualitative.Set3  # 配色方案
)

fig.update_traces(
    textposition='inside',      # 標籤位置：'inside', 'outside', 'auto'
    textinfo='percent+label'    # 顯示百分比和標籤（可選：'label', 'percent', 'value', 'label+percent'等）
)

fig.update_layout(
    template='plotly_white'
)

fig.show()

