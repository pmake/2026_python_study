import plotly.express as px
import pandas as pd

# 建立範例資料
df = pd.DataFrame({
    '專案階段': ['需求分析', '設計', '開發', '測試', '上線'],
    '開始日期': ['2025-01-01', '2025-01-10', '2025-02-01', '2025-03-01', '2025-03-20'],
    '結束日期': ['2025-01-09', '2025-01-31', '2025-02-28', '2025-03-19', '2025-03-31'],
    '負責人': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eric']
})

# 建立時間軸圖
fig = px.timeline(
    df,
    x_start='開始日期',
    x_end='結束日期',
    y='專案階段',
    color='負責人',
    title='專案開發時程表',
)

# 調整顯示順序與樣式
fig.update_yaxes(autorange='reversed')  # 讓最早的階段在上方
fig.update_layout(xaxis_title='日期', yaxis_title='專案階段')
fig.show()