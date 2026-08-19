import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    '蘋果汁': [60, 30, 10, 50, 20],
    '柳橙汁': [30, 50, 70, 20, 60],
    '葡萄汁': [10, 20, 20, 30, 20],
    '飲料名稱': ['清爽蘋果', '熱帶橙香', '葡萄能量', '蜜香特調', '晨光綜合']
})

fig = px.scatter_ternary(
    df,
    a='蘋果汁',
    b='柳橙汁',
    c='葡萄汁',
    color='飲料名稱',
    size='蘋果汁',
    title='果汁飲品配方比例分析'
)

fig.show()