import plotly.express as px
import pandas as pd

# 模擬多層級預算資料
df = pd.DataFrame({
    '部門': ['行銷', '行銷', '行銷', '研發', '研發', '業務', '業務', '管理', '管理'],
    '子部門': ['廣告', '活動', '品牌', '產品開發', '測試', '北區', '南區', '人資', '財務'],
    '專案': ['社群行銷', '線下活動', '品牌重塑', 'App開發', 'QA自動化', '新客拓展', 'VIP維護', '招募計畫', '預算管理'],
    '預算金額': [300, 150, 200, 400, 180, 250, 200, 100, 120]
})

# 建立冰柱圖
fig = px.icicle(
    df,
    path=['部門', '子部門', '專案'],  # 定義階層結構
    values='預算金額',
    color='部門',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='公司年度預算分配冰柱圖（階層矩形分析）'
)

fig.show()