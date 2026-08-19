import plotly.express as px

# 使用內建 Gapminder 資料集
df = px.data.gapminder().query("year == 2007")

fig = px.choropleth(
    df,
    locations="iso_alpha",           # 國家 ISO 代碼
    color="gdpPercap",               # 顏色依 GDP 人均值
    hover_name="country",            # 滑鼠提示國名
    color_continuous_scale="Viridis",# 顏色漸層
    title="🌍 2007 年全球各國人均 GDP 分布圖"
)

fig.show()