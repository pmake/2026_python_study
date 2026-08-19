- 繪圖要點： 
    - 圖表會有主要內容，例如x,y，如果有次要資料可能需要用到，可以設置為hover data，遊標掃過即會顯示
    - 雷達圖主要用途是比較在各種指標的表現，如果指標數值差距過大，可以考慮標準化或做有意義的數值轉換

- Streamlit要點
    - 簡單說Streamlit提供構建網頁的基礎框架以及各種部件，你可以利用這些部件來構建你的網頁，用疊床架屋的方式堆疊網頁內容。然後和Pandas, Plotly等套件密切整合，可以簡單的將處理好的資料或圖表置入網頁中。
        - streamlit 有很多的部件，比如radio, markdown, 讓你可以簡單快速的佈建網頁格局。
        - 和plotly, bokeh, matplotlib, seaborn等圖表庫可以完美結合，你可以利用這些圖表庫製作圖表，然後利用streamlit的部件將圖表佈建在網頁上。
    - 架構
        - page 和 navigation
            - 一個page一個.py檔
                - page中使用部件拼裝內容
            - 在首頁上設定navigation
                - 在navigation中import其他page
        