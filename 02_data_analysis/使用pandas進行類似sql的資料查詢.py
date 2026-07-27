import pandas as pd
from pathlib import Path

# 1. 使用 pathlib 設定路徑（最佳實作：跨平台且直覺）
target_dir = Path('02_data_analysis/outputs')
target_team_file_path = target_dir / 'nba_teams.csv'
target_player_file_path = target_dir / 'nba_players.csv'

# 2. 直接使用 pd.read_csv 讀取（自動進行 CSV 解析與檔案關閉）
teams_df = pd.read_csv(target_team_file_path)
players_df = pd.read_csv(target_player_file_path)

# 3. 💡 真正的 Pandas 鏈式查詢（Method Chaining）
# 將 合併 -> 條件過濾 -> 排序 -> 重設索引 一氣呵成
laker_players = (
    players_df
    .merge(teams_df, on='teamid', how='inner')
    .query("fullname == 'Los Angeles Lakers'")
    .sort_values(by='lastname')  # 依球員姓氏排序
    .reset_index(drop=True)      # 重置索引，讓號碼從 0 開始
)

# 4. 檢視結果
print(f"湖人隊共有 {len(laker_players)} 位球員：")
# 篩選前5筆資料檢視，並指定要取得的欄位，並列印出來
print(laker_players.loc[0:4, ['firstname', 'lastname', 'fullname']])

# 找出每場平均得分最高的10名球員