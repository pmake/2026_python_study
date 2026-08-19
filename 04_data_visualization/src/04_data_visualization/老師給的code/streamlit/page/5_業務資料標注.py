import streamlit as st
import pandas as pd

sales = pd.read_csv('./data/sales.csv')


st.dataframe(sales.groupby('業務單位')[['銷售數量','銷售金額']].sum().style.highlight_min())