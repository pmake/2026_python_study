# [FIRST OCCURRENCE: pathlib.Path] 匯入標準函式庫的物件導向路徑處理模組 Path。
from pathlib import Path

# [FIRST OCCURRENCE: pandas] 匯入資料處理與分析的核心函式庫，慣用別名為 pd。
import pandas as pd

# [FIRST OCCURRENCE: ColumnTransformer] 欄位轉換器，允許對 DataFrame 中不同型態的欄位（如數值與類別）分別套用不同的預處理管道，最後水平拼裝（hstack）成單一特徵矩陣。
from sklearn.compose import ColumnTransformer
# [FIRST OCCURRENCE: Pipeline] 循序執行一系列轉換器（Transformers）與最終估計器（Estimator）的管道物件，能避免資料外洩（Data Leakage）並簡化流程。
from sklearn.pipeline import Pipeline
# [FIRST OCCURRENCE: SimpleImputer] 缺失值填補工具，提供單變量（單一欄位統計量）的缺失值補值策略（如平均數、中位數、眾數或常數）。
from sklearn.impute import SimpleImputer
# [FIRST OCCURRENCE: StandardScaler, OneHotEncoder]
# - StandardScaler: 數值特徵標準化（Z-score: (x - μ) / σ），將資料轉換為平均值 0、標準差 1 的分佈。
# - OneHotEncoder: 獨熱編碼器，將離散類別特徵轉換為二元（0/1）虛擬變數向量。
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# [FIRST OCCURRENCE: train_test_split] 資料集切分工具，用於將特徵與目標變數依指定比例隨機拆分為訓練集與測試集。
from sklearn.model_selection import train_test_split

# [FIRST OCCURRENCE: pd.read_csv] 從指定路徑讀取 CSV 檔案並載入為 DataFrame 物件。
# [FIRST OCCURRENCE: Path(__file__).parent] 取得當前檔案所在目錄，確保無論從何處執行都能正確定位同目錄下的 data 資料夾。
# Load data
data_path = Path(__file__).resolve().parent / "data" / "mixed_data.csv"
mixed_data = pd.read_csv(data_path)

# 欄位設定：將特徵依資料型態分群，以便後續指派不同的預處理步驟
numeric_cols = ["Age", "Salary", "Experience"]
categorical_cols = ["Department", "Position"]

# 數值欄位 Pipeline
# [FIRST OCCURRENCE: Pipeline 實例化] 接收由 (名稱, 轉換器物件) 構成的 tuple 清單，資料會依序流入轉換器。
numeric_pipeline = Pipeline([
    # [FIRST OCCURRENCE: SimpleImputer(strategy="mean")] 計算各欄位平均值（Mean）來填補缺失值，僅適用於連續型數值資料。
    ("imputer", SimpleImputer(strategy="mean")),
    # [FIRST OCCURRENCE: StandardScaler()] 計算各數值欄位的平均值與標準差，消除不同特徵間量綱/尺度差異對模型的影響。
    ("scaler", StandardScaler())
])

# 類別欄位 Pipeline
# [RECURRING: Pipeline] 針對類別型欄位定義專屬的處理流水線。
categorical_pipeline = Pipeline([
    # [RECURRING: SimpleImputer] 此處使用 strategy="most_frequent"（眾數填補），以出現頻率最高的類別值填補缺失，適用於離散/文字欄位。
    ("imputer", SimpleImputer(strategy="most_frequent")),
    # [FIRST OCCURRENCE: OneHotEncoder 參數解析]
    # - handle_unknown="ignore": 若預測/測試階段遇到未曾看過的全新類別，直接編碼為全 0 向量，避免拋出 ValueError。
    # - sparse_output=False: 直接輸出稠密矩陣（Dense NumPy Array）而非稀疏矩陣（scipy.sparse），方便後續檢視與轉為 DataFrame。
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# ColumnTransformer 整合
# [FIRST OCCURRENCE: ColumnTransformer 實例化]
# - transformers: 接收由 (步驟名稱, 轉換器/Pipeline, 作用欄位清單) 構成的 tuple 列表。
# - remainder="passthrough": 未在 transformers 中被指定的其他欄位將原樣保留（預設為 "drop" 會被丟棄）。
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ],
    remainder="passthrough"
)

# [FIRST OCCURRENCE: fit_transform]
# 1. fit: 在 mixed_data 上學習統計參數（各數值欄位的均值與標準差、各類別欄位的唯一值字典）。
# 2. transform: 套用學習到的參數執行補值、標準化與獨熱編碼，回傳合併後的二維 NumPy 陣列。
X_train_transformed = preprocessor.fit_transform(mixed_data)

# 取得轉換後的欄位名稱
# [FIRST OCCURRENCE: get_feature_names_out] 自動生成轉換後的特徵欄位名稱清單（如 "num__Age", "cat__Department_HR" 等），保留特徵可解釋性。
feature_names = preprocessor.get_feature_names_out()

# 轉成 DataFrame
# [FIRST OCCURRENCE: pd.DataFrame 重組]
# 將轉換後的純數值陣列（NumPy ndarray）重新封裝回 DataFrame，並綁定對應的欄位名稱（columns）與原始索引（index）。
X_train_transformed_df = pd.DataFrame(
    X_train_transformed,
    columns=feature_names,
    index=mixed_data.index
)

# 輸出檢視最終轉換完成的 DataFrame 物件
X_train_transformed_df
print(X_train_transformed_df)