import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    '部門': ['行銷', '研發', '業務', '客服', '管理'],
    '績效分數': [80, 90, 75, 70, 85]
})

fig = px.scatter_polar(
    df,
    r='績效分數',
    theta='部門',
    color='部門',     # 可選：依分類上色
    size='績效分數',  # 可選：以大小代表強度
    title='各部門績效雷達圖'
)
fig.show()
