from pathlib import Path
import plotly.express as px
import pandas as pd

# 讀取銷售資料 (以目前檔案所在路徑為基準)
data_path = Path(__file__).parent / 'data'
file_path = data_path / 'nba_career.csv'
df = pd.read_csv(file_path)

# 建立散點圖
fig = px.scatter(
    df,
    x='ppg',
    y='rpg',
    # color='產品類別',
    # size='銷售額',
    title='ppg與rpg關係圖',
    labels={'ppg': 'ppg', 'rpg': 'rpg'}
)

fig.show()

