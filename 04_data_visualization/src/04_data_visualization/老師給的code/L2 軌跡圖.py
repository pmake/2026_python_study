import plotly.express as px
import pandas as pd
import numpy as np

# 模擬飛行軌跡資料
t = np.linspace(0, 10, 100)
df = pd.DataFrame({
    '時間': t,
    'x座標': np.sin(t) * 10,
    'y座標': np.cos(t) * 10,
    '高度': t * 2
})

# 建立三維折線圖
fig = px.line_3d(
    df,
    x='x座標',
    y='y座標',
    z='高度', 
    title='無人機飛行軌跡（3D Line）',
)

fig.show()