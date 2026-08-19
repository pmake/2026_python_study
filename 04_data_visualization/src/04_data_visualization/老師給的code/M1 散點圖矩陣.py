import plotly.express as px
import pandas as pd

# 模擬車輛性能資料
df = pd.DataFrame({
    '馬力': [120, 150, 180, 200, 220, 250, 300],
    '油耗(km/L)': [15, 14, 12, 11, 10, 9, 8],
    '價格(萬)': [80, 100, 120, 140, 160, 180, 200],
    '加速(0-100km/s)': [12, 10, 8.5, 7.8, 7.0, 6.5, 5.8],
    '品牌': ['A', 'A', 'B', 'B', 'C', 'C', 'C']
})

# 建立散點圖矩陣
fig = px.scatter_matrix(
    df,
    dimensions=['馬力', '油耗(km/L)', '價格(萬)', '加速(0-100km/s)'],
    color='品牌',
    title='車輛性能指標散點圖矩陣',
    
)

fig.update_traces(diagonal_visible=True)  # 顯示對角線分佈
fig.show()