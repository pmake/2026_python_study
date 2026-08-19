import plotly.express as px
import streamlit as st

df = px.data.iris()
fig = px.scatter(df, 
                 x="sepal_width", 
                 y="sepal_length", 
                 color="species", 
                 marginal_y="violin",
                 marginal_x="box", 
                 template="simple_white")

st.plotly_chart(fig, use_container_width=True)