import streamlit as st
import pandas as pd

st.write("使用資料來建立表格。")

#  write會幫你找最適合的表達方式，所以這個具有互動性
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# 單純的靜態table
st.table(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))





