import pandas as pd
import plotly.express as px
import numpy as np


np.random.seed(42)

# 為每個產品生成多個銷售額數據點，包含一些異常值
data = []
products = ['產品A', '產品B', '產品C', '產品D']

for product in products:
    # 為每個產品生成不同分佈特徵的數據
    if product == '產品A':
        sales = np.random.normal(50000, 8000, 100)  # 平均50000，標準差8000
        # 添加一些異常值
        sales = np.append(sales, [120000, 15000])
    elif product == '產品B':
        sales = np.random.normal(60000, 10000, 100)  # 平均60000，標準差10000
        sales = np.append(sales, [20000])
    elif product == '產品C':
        sales = np.random.normal(45000, 12000, 100)  # 平均45000，標準差12000（分佈較廣）
        sales = np.append(sales, [100000, 8000])
    else:  # 產品D
        sales = np.random.normal(55000, 9000, 100)   # 平均55000，標準差9000
        sales = np.append(sales, [130000])
    
    # 確保銷售額為正數
    sales = np.clip(sales, 0, None)
    
    for sale in sales:
        data.append({'產品': product, '銷售額': sale})

df = pd.DataFrame(data)

# 箱線圖（盒鬚圖）
fig = px.box(
    df,
    x='產品',           # 類別變數
    y='銷售額',         # 數值變數
    color='產品',       # 依產品上色
    points='outliers',  # 只顯示異常值（可選：'all', 'suspectedoutliers', False）
    title='各產品銷售額分佈比較（箱線圖）',
    labels={'銷售額': '銷售額（元）', '產品': '產品'}
)

fig.update_layout(
    template='plotly_white',
    showlegend=False
)

fig.show()

