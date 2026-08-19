import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


months = np.arange(1, 13)
sales = np.random.randint(1000, 5000, size=12)

fig, ax = plt.subplots()
ax.plot(months, sales, label='Monthly Sales', color='blue', linestyle='-')
ax.set_title("Performance Over 12 Months")
ax.set_xlabel("Month")
ax.set_ylabel("Performance (Unit: Thousand)")
ax.set_xticks(months)
ax.legend()

st.pyplot(fig)