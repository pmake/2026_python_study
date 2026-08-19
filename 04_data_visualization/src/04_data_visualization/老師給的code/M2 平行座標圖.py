import plotly.express as px
import pandas as pd

# 建立車輛性能資料
df = pd.DataFrame({
    '車款': ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
    '品牌': ['Audi', 'Audi', 'BMW', 'BMW', 'Toyota', 'Toyota'],
    '馬力': [150, 180, 200, 220, 130, 140],
    '油耗(km/L)': [14, 13, 12, 11, 17, 16],
    '價格(萬)': [120, 140, 160, 180, 100, 110],
    '加速(0-100km/s)': [9.0, 8.0, 7.5, 7.0, 10.5, 9.8]
})

# 建立平行座標圖
fig = px.parallel_coordinates(
    df,
    dimensions=['馬力', '油耗(km/L)', '價格(萬)', '加速(0-100km/s)'],
    color='價格(萬)',
    color_continuous_scale=px.colors.sequential.Viridis,
    title='車輛性能平行座標圖'
)

fig.show()