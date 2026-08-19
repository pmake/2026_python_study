import pandas as pd
import plotly.express as px

# 創造樣板數據：一週各天的銷售額（週期性數據）
df = pd.DataFrame({
    '星期': ['週一', '週二', '週三', '週四', '週五', '週六', '週日'],
    '銷售額': [12000, 15000, 18000, 16000, 22000, 28000, 25000],
    '類別': ['平日', '平日', '平日', '平日', '平日', '週末', '週末']
})

# 極座標長條圖（圓形長條圖）
fig = px.bar_polar(
    df,
    r='銷售額',           # 半徑（數值）
    theta='星期',         # 角度（類別）
    color='銷售額',       # 顏色映射到數值
    template='plotly_white',
    color_continuous_scale='Viridis',
    title='一週各天銷售額極座標長條圖'
)

fig.show()

