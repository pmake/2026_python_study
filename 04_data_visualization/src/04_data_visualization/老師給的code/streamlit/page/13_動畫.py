import streamlit as st
import plotly.express as px


df = px.data.gapminder()
fig = px.bar(df, x="continent", y="pop", color="continent",
             animation_frame="year",
             animation_group="country", 
             range_y=[0,4000000000]
             )

st.plotly_chart(fig, use_container_width=True)