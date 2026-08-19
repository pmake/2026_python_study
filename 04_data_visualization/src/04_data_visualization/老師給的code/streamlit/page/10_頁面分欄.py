import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
with left_column:
    if st.button('Press me!'):
        st.success('按鈕已被按下！')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        '選擇顏色',
        ("紅色", "綠色", "藍色", "黃色"))
    st.write(f"你選擇了 {chosen} 顏色")