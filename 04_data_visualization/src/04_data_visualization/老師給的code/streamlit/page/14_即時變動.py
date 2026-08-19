import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("📊 即時亂數折線圖")

# 建立一個空的位置
chart_area = st.empty()

# 儲存資料
values = []

for i in range(50):
    new_value = np.random.randint(0, 100)

    values.append(new_value)

    df = pd.DataFrame({
        "數值": values
    })

    # 每次把同一個位置的圖重新更新
    chart_area.line_chart(df)

    time.sleep(1)

st.success("✅ 模擬結束")