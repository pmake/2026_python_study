import streamlit as st
import mysql.connector
import pandas as pd

st.title("MySQL 資料")

try:
    # ① 直接使用 mysql-connector-python 建立連線
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["username"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

    # ② 建立 Cursor
    cursor = conn.cursor(dictionary=True)

    # ③ 執行 SQL
    cursor.execute("SELECT * FROM players LIMIT 100")

    # ④ 取得資料
    rows = cursor.fetchall()

    # ⑤ 轉成 DataFrame
    df = pd.DataFrame(rows)

    st.success("資料庫連線成功")
    st.dataframe(df, use_container_width=True)

    # ⑥ 關閉
    cursor.close()
    conn.close()

except Exception as error:
    st.error(f"資料庫連線失敗：{error}")