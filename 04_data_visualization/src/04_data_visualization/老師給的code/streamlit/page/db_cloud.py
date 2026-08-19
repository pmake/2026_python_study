import json
import os

import mysql.connector
import pandas as pd
import streamlit as st


REQUIRED_CONFIG_KEYS = {"host", "port", "database", "user", "password"}


def get_mysql_config():
    """從 Cloud Run 的 MYSQL_CONFIG Secret 讀取 MySQL 連線設定。"""
    raw_config = os.getenv("MYSQL_CONFIG")
    if not raw_config:
        raise RuntimeError(
            "找不到 MYSQL_CONFIG，請在 Cloud Run 將 Secret 綁定到同名環境變數。"
        )

    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError as error:
        raise RuntimeError("MYSQL_CONFIG 不是有效的 JSON 格式。") from error

    missing_keys = REQUIRED_CONFIG_KEYS - config.keys()
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise RuntimeError(f"MYSQL_CONFIG 缺少必要欄位：{missing}")

    return config


@st.cache_data(ttl=60)
def load_players():
    """從 MySQL 讀取 players 資料，並快取 60 秒。"""
    config = get_mysql_config()
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=int(config["port"]),
            user=config["user"],
            password=config["password"],
            database=config["database"],
            charset="utf8mb4",
            connection_timeout=10,
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM players LIMIT 100")
        return pd.DataFrame(cursor.fetchall())
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


st.title("☁️ Cloud MySQL 資料")

try:
    df = load_players()
    st.success("資料庫連線成功")
    st.dataframe(df, use_container_width=True)
except Exception as error:
    st.error(f"資料庫連線失敗：{error}")
