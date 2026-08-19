import pandas as pd
import plotly.express as px
import numpy as np

# 創造樣板數據：店鋪A的每日營業額（用於數據頻率分佈、數據分組統計）
np.random.seed(42)

# 生成每日營業額數據點
revenue = np.random.normal(50000, 8000, 150)  # 平均50000，標準差8000
# 確保營業額為正數
revenue = np.clip(revenue, 0, None)

df = pd.DataFrame({'營業額': revenue})

# 直方圖
fig = px.histogram(
    df,
    x='營業額',         # 數值變數
    nbins=30,           # 分組數量（可選，預設會自動計算）
    title='店鋪A每日營業額分佈直方圖',
    labels={'營業額': '營業額（元）', 'count': '頻率'}
)

fig.update_layout(
    template='plotly_white',
    xaxis_title='營業額（元）',
    yaxis_title='頻率'
)

fig.show()

