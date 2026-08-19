import streamlit as st
import pandas as pd
import numpy as np

# 建立隨機數據
df = pd.DataFrame(
    np.random.randn(5, 4),
    columns=['A', 'B', 'C', 'D']
)

# 加上顏色：大於 0 綠色，小於 0 紅色
styled_df = df.style.map(
    lambda val: 'color: #0000FF' if val > 0 else 'color: #FFA500'
)

# 顯示互動表格（可捲動、可篩選）
# 跟st.write的效果一致
st.dataframe(styled_df, use_container_width=True)