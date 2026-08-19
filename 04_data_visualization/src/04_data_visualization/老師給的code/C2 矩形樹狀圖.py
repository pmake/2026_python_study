import pandas as pd
import plotly.express as px


df = pd.DataFrame({
    '部門': ['行銷部', '行銷部', '行銷部', '研發部', '研發部', '研發部', '業務部', '業務部', '業務部'],
    '產品類別': ['數位廣告', '社群媒體', '傳統媒體', '軟體開發', '硬體研發', '測試', 'B2B銷售', 'B2C銷售', '線上銷售'],
    '預算': [500000, 300000, 200000, 800000, 600000, 200000, 700000, 500000, 400000]
})

# 樹狀圖（矩形樹狀圖）
fig = px.treemap(
    df,
    path=[px.Constant('全部部門'), '部門', '產品類別'],  # 階層路徑：根節點 -> 第一層 -> 第二層
    values='預算',      # 數值（決定矩形大小）
    color='預算',        # 顏色映射到數值
    color_continuous_scale='Blues',  # 連續色階
    title='各部門產品類別預算分配樹狀圖',
    labels={'預算': '預算（元）'}
)

fig.update_layout(
    template='plotly_white'
)

fig.show()

