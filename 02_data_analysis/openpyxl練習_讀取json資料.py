import json
from pathlib import Path
import pandas as pd

# 使用 pathlib 讀取檔案內容並解析 JSON
BASE_DIR = Path.cwd()
work_dir = BASE_DIR / '02_data_analysis' / 'outputs'
print(work_dir)
file_path = work_dir / '路外停車資訊.json'

# 直接將 JSON 檔載入成 Dataframe 格式
df = pd.read_json(file_path)
print(df.head())

# 快速篩選出區域為「八德區」且有剩餘車位的停車場
bade_parks = df[df['areaName'] == '八德區'][['parkName', 'totalSpace', 'surplusSpace']]
print(bade_parks.loc[0:4])