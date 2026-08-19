import pandas as pd
import plotly.express as px
import numpy as np


np.random.seed(42)


data = []
regions = ['北部', '中部', '南部', '東部']

for region in regions:
    # 為每個地區生成不同分佈特徵的數據
    if region == '北部':
        scores = np.random.normal(85, 10, 200)  # 平均85，標準差10
    elif region == '中部':
        scores = np.random.normal(80, 12, 200)   # 平均80，標準差12
    elif region == '南部':
        scores = np.random.normal(75, 15, 200)   # 平均75，標準差15（分佈較廣）
    else:  # 東部
        scores = np.random.normal(82, 11, 200)   # 平均82，標準差11

    # 確保分數在合理範圍內（0-100）並四捨五入取整
    scores = np.clip(scores, 0, 100)
    scores = np.round(scores).astype(int)

    for score in scores:
        data.append({'地區': region, '滿意度分數': score})

df = pd.DataFrame(data)

# 經驗累積分佈函數圖（ECDF）
fig = px.ecdf(
    df,
    x='滿意度分數',     # 數值變數
    color='地區',       # 依地區分組並上色
    title='各地區客戶滿意度分數累積分佈函數（ECDF）',
    labels={'滿意度分數': '滿意度分數', 'ecdf': '累積概率'},
    ecdfnorm='probability'  # 顯示概率（0-1），可選：'percent'（0-100%）
)

fig.update_layout(
    template='plotly_white',
    xaxis_title='滿意度分數',
    yaxis_title='累積概率',
    legend_title='地區'
)

fig.show()

df.to_excel('test copy 3.xlsx')