import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)



# 優點：一行就畫好，支援互動。
# 缺點：無法客製顏色、加標題、調整樣式。

st.line_chart(df)