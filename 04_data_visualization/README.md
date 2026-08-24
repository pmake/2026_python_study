# 04 Data Visualization
## 執行Streamlit指令
- 需在終端輸入以下指令:
    - ".venv\Scripts\python -m streamlit run 04_data_visualization\src\04_data_visualization\p4_streamlit.py"
## Deploy 到 Streamlit.io
- 點擊本地執行的 Streamlit 網址右上角的「Deploy」->「Deploy to Streamlit Community Cloud」
- 接著依程序走
    - 注意預設只能讀取Public的Github repo，可以透過設定權限使其可讀取Private的 repo, 但不建議
- 本地使用.env管理的敏感資訊，在deploy時需要新增到Streamlit.io 對應app的設定中
    - Secrets 會被加密儲存，詳見Streamlit Secrets運作方式說明
        - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
        - 展示用項目才deploy，雖然有加密，但仍有風險。
    - 設定路徑
        - app 清單 -> Settings -> Secrets -> 將.env內容改為TOML格式寫入並儲存即可，不需修改程式碼
            - 寫入後會需要幾分鐘才會生效
        