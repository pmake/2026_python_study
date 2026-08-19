from pathlib import Path
import pandas as pd
import plotly.express as px

# 讀取銷售資料 (以目前檔案所在路徑為基準)
data_path = Path(__file__).parent / 'data'
file_path = data_path / 'sales.csv'
df = pd.read_csv(file_path)

# 按業務單位分組，計算總業績金額
sales_by_unit = df.groupby('業務單位')['銷售金額'].sum().reset_index()
sales_by_unit = sales_by_unit.sort_values('銷售金額', ascending=False)

sales_by_unit.to_csv(data_path / '業務整理結果.csv', index=False, encoding='utf-8-sig')

# 使用 plotly.express 建立柱狀圖
fig = px.bar(
    sales_by_unit,
    x='業務單位',
    y='銷售金額',
    text=sales_by_unit['銷售金額'].apply(lambda x: f'{x:,.0f}'),
    title='各業務單位業績金額柱狀圖',
    labels={'業務單位': '業務單位', '銷售金額': '業績金額'},
    #https://www.w3schools.com/colors/colors_names.asp
    color_discrete_sequence=['DeepPink']
)


# 設定文字標籤位置
# textposition 參數常用選項如下:
# 'inside'：文字顯示於 bar 內部
# 'outside'：文字顯示於 bar 外部
# 'auto'：自動選擇顯示位置
# 'none'：不顯示文字
fig.update_traces(textposition='outside')

# 設定圖表高度
fig.update_layout(height=600)

# 顯示圖表
fig.show()

