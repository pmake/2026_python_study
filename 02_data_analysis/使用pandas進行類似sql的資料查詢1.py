import pandas as pd
from pathlib import Path

target_dir = Path('02_data_analysis/outputs')
target_player_file_path = target_dir / 'nba_players.csv'
target_career_file_path = target_dir / 'nba_career_summaries.csv'
target_team_file_path = target_dir / 'nba_teams.csv'


players_df = pd.read_csv(target_player_file_path)
career_df = pd.read_csv(target_career_file_path)
teams_df = pd.read_csv(target_team_file_path)

# 找出每場平均得分最高的10名球員
players_top10_ppg = (
    players_df
    .merge(career_df, on='personid', how='inner')
    .nlargest(10, 'ppg', keep='all')
    .sort_values(by='ppg',ascending=False) 
    .reset_index(drop=True)
)

print("ppg排名前10球員清單：")
print(players_top10_ppg.loc[:, ['firstname', 'lastname', 'ppg']])

# 多重條件
players_multi_conditions = (
    players_df
    .merge(career_df, on='personid', how='inner')
    .query("ppg >= 20 and rpg >= 5 and apg >= 3")
    .sort_values(by='ppg',ascending=False) 
    .reset_index(drop=True)
)

print("多重條件過濾：")
print(players_multi_conditions.loc[:, ['firstname', 'lastname', 'ppg', 'apg', 'rpg']])

# 分群處理
result_grouped_processed = (
    players_df
    .merge(career_df, on='personid', how='inner') # inner, 兩邊都要有才是有效資料
    .merge(teams_df, on='teamid', how='left') # left, 左表有就有效，比對不到會回傳NaN補上空資料
    .groupby(['teamid', 'fullname'],dropna=False) # 加入fullname易於識別, dropna=False設定當分組中包含NaN數據時不會把整組過濾
    .agg(
        count_ppg_over_20=('ppg', lambda x: (x >= 20).sum()), # 對每個分組做處理，指定欄位和處理方式
        count_rpg_over_5=('rpg', lambda x: (x >= 5).sum()),
        count_apg_over_3=('apg', lambda x: (x > 3).sum())
    )
    .sort_values(by=['fullname', 'teamid'])
    .reset_index()
)

print("分群處理：")
print(result_grouped_processed.loc[:])
