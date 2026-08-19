import plotly.express as px
import pandas as pd

# 建立車輛性能評比資料
df = pd.DataFrame({
    '項目': ['加速', '操控', '舒適度', '安全性', '油耗', '科技配備', '外觀', '加速'],  # 收尾連接
    'Model A': [9, 8, 7, 8, 6, 7, 8, 9],
    'Model B': [7, 9, 8, 9, 7, 9, 7, 7],
    'Model C': [8, 7, 9, 7, 9, 8, 8, 8]
})

# 將資料轉為長表格式
df_melt = df.melt(id_vars='項目', var_name='車款', value_name='評分')

# 建立極座標折線圖
fig = px.line_polar(
    df_melt,
    r='評分',
    theta='項目',
    color='車款',
    line_close=True,
    markers=True,
    title='車輛能力評比雷達圖',
    labels={'項目': '性能項目', '評分': '分數 (1~10)'}
)

fig.update_traces(fill='toself', opacity=0.6)  # 讓每條線區域填滿，增加可讀性
fig.show()