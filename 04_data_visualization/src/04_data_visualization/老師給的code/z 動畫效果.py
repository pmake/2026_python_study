import plotly.express as px

# 內建資料集：各國 GDP、壽命、人口隨年份變化
df = px.data.gapminder()

fig = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    animation_frame="year",  # 動畫控制的時間軸
    animation_group="country",  # 每個國家是一個持續的群組
    size="pop",  # 氣泡大小
    color="continent",  # 顏色依洲別區分
    hover_name="country",
    log_x=True,  # GDP 改用對數軸更清楚
    size_max=60,
    range_x=[100, 100000],
    range_y=[25, 90],
    title="🌍 各國 GDP 與壽命變化（1952–2007）"
)

fig.show()