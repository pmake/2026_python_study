import pandas as pd
import plotly.express as px
import numpy as np


np.random.seed(42)


data = []
courses = ['數學', '語文', '英文', '科學']

for course in courses:
    # 為每個課程生成不同分佈特徵的數據
    if course == '數學':
        scores = np.random.normal(75, 12, 80)  # 平均75，標準差12
    elif course == '語文':
        scores = np.random.normal(82, 10, 80)   # 平均82，標準差10
    elif course == '英文':
        scores = np.random.normal(78, 14, 80)   # 平均78，標準差14（分佈較廣）
    else:  # 科學
        scores = np.random.normal(80, 11, 80)   # 平均80，標準差11
    
    # 確保分數在合理範圍內（0-100）
    scores = np.clip(scores, 0, 100)
    scores = np.round(scores).astype(int)
    
    for score in scores:
        data.append({'課程': course, '成績': score})

df = pd.DataFrame(data)

# 條帶圖（一維散點圖）
fig = px.strip(
    df,
    x='課程',           # 類別變數
    y='成績',           # 數值變數
    color='課程',       # 依課程上色
    stripmode='overlay',  # 重疊模式（可選：'group' 分組顯示）
    title='各課程學生成績分佈比較（條帶圖）',
    labels={'成績': '成績', '課程': '課程'}
)

fig.update_layout(
    template='plotly_white',
    showlegend=False
)

fig.show()

