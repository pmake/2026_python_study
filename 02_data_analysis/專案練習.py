import pandas as pd
from pathlib import Path

# 使用 pathlib 建立路徑
BASE_DIR = Path.cwd()
work_dir = BASE_DIR / '02_data_analysis' / 'outputs'
print(work_dir)

