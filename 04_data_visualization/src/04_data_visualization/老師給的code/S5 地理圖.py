import plotly.express as px
import pandas as pd

# 建立範例資料
df = pd.DataFrame({
    '城市': ['台北', '台中', '高雄'],
    '經度': [121.5654, 120.684, 120.301],
    '緯度': [25.0330, 24.1477, 22.6273],
    '銷售額': [500, 300, 700]
})

# 建立地圖散點圖
fig = px.scatter_map(
    data_frame=df,
    lat='緯度',
    lon='經度',
    color='銷售額',
    size='銷售額',
    hover_name='城市',
    zoom=6,
    map_style='basic',   # 直接使用 OSM，不需要 Mapbox Token
    title='全台銷售據點分佈圖',
    subtitle='依銷售額大小與顏色區分'
)

fig.show()





# https://plotly.com/python-api-reference/generated/plotly.express.scatter_map.html

# map style. Allowed values are 
# 'basic', 'carto-darkmatter', 'carto-darkmatter-nolabels', 
# 'carto-positron', 'carto-positron-nolabels', 'carto-voyager', 
# 'carto-voyager-nolabels', 'dark', 'light', 'open-street-map', 
# 'outdoors', 'satellite', 'satellite-streets', 'streets', 
# 'white-bg'.