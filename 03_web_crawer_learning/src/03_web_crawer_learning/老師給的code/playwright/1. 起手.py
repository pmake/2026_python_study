# 從 playwright.sync_api 模組中匯入同步（sync）API 的 sync_playwright 函式
from playwright.sync_api import sync_playwright

# 啟動 Playwright 上下文管理器，並將 Playwright 實例賦值給變數 p
with sync_playwright() as p:
    # 啟動 Chromium 瀏覽器實例
    browser = p.chromium.launch(
        channel="chrome",  # 指定使用的瀏覽器管道為本機安裝的 Google Chrome
        headless=False  # 設定為無頭模式（True 代表背景執行不顯示視窗，False 會顯示瀏覽器 GUI）
    )

    # 在瀏覽器中建立並開啟一個新的分頁（Page）
    page = browser.new_page()
    
    # 讓分頁前往（導覽至）指定的網址
    page.goto("https://google.com")
    
    # 取得當前網頁的標題（Title）並印出至主控台
    print(page.title())

    # 暫停程式執行，等待使用者在終端機按下 Enter 鍵
    input("Press Enter to exit...")
    
    # 關閉瀏覽器實例並釋放資源
    browser.close()