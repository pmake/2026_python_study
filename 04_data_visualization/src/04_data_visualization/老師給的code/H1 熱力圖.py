import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
years = range(2018, 2025)
months = range(1, 13)

data = []
for y in years:
    for m in months:
        base = (y - 2017) * 100000
        passengers = base + np.random.randint(100000, 900000)
        data.append([y, m, passengers])

df = pd.DataFrame(data, columns=['年份', '月份', '出境人數'])

# 年份升冪排列（2018 最小、2024 最大）
pivot_df = df.pivot(index='年份', columns='月份', values='出境人數').sort_index(ascending=True)

fig = px.imshow(
    pivot_df,
    color_continuous_scale='YlOrRd',
    title='歷年每月出境人數熱力圖（年份由下往上遞增）',
    origin='lower'  # 關鍵：把原點設在左下角
)

fig.update_xaxes(dtick=1)
fig.show()