import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# Load data
mixed_data = pd.read_csv("data/mixed_data.csv")

# 欄位設定
numeric_cols = ["Age", "Salary", "Experience"]
categorical_cols = ["Department", "Position"]

# 數值欄位 Pipeline
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

# 類別欄位 Pipeline
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ],
    remainder="passthrough"
)



X_train_transformed = preprocessor.fit_transform(mixed_data)

# 取得轉換後的欄位名稱
feature_names = preprocessor.get_feature_names_out()

# 轉成 DataFrame
X_train_transformed_df = pd.DataFrame(
    X_train_transformed,
    columns=feature_names,
    index=mixed_data.index
)

X_train_transformed_df
