import streamlit as st
import pandas as pd

sales = pd.read_csv('./data/sales.csv')

st.dataframe(sales)