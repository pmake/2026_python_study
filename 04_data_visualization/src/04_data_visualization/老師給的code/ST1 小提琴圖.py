import pandas as pd
import plotly.express as px
import numpy as np


np.random.seed(42)

# 為每個部門生成多個績效分數數據點，模擬真實分佈
data = []
departments = ['行銷部', '研發部', '業務部', '客服部', '管理部']

for dept in departments:
    # 為每個部門生成不同分佈特徵的數據
    if dept == '行銷部':
        scores = np.random.normal(75, 10, 50)  # 平均75，標準差10
    elif dept == '研發部':
        scores = np.random.normal(85, 8, 50)   # 平均85，標準差8
    elif dept == '業務部':
        scores = np.random.normal(70, 15, 50)  # 平均70，標準差15（分佈較廣）
    elif dept == '客服部':
        scores = np.random.normal(65, 12, 50)   # 平均65，標準差12
    else:  # 管理部
        scores = np.random.normal(80, 9, 50)   # 平均80，標準差9
    
    # 確保分數在合理範圍內（0-100）
    scores = np.clip(scores, 0, 100)
    
    for score in scores:
        data.append({'部門': dept, '績效分數': score})

df = pd.DataFrame(data)

# 小提琴圖（結合箱線圖和密度圖）
fig = px.violin(
    df,
    x='部門',           # 類別變數
    y='績效分數',       # 數值變數
    color='部門',       # 依部門上色
    box=True,           # 顯示箱線圖
    points='all',       # 顯示所有數據點（可選：'outliers', 'suspectedoutliers', False）
    title='各部門績效分數分佈比較（小提琴圖）',
    labels={'績效分數': '績效分數', '部門': '部門'}
)

fig.update_layout(
    template='plotly_white',
    showlegend=False
)

fig.show()

