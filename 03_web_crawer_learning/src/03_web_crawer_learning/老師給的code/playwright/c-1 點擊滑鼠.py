# 從 playwright 的同步 API 模組中匯入 sync_playwright 進入點函式
from playwright.sync_api import sync_playwright

# 使用上下文管理器 (with 語句) 啟動 Playwright 環境，執行結束後會自動釋放相關資源
with sync_playwright() as p:
    # 啟動 Chromium 瀏覽器（指定 channel="chrome" 使用本機 Chrome，headless=False 關閉無頭模式以顯示瀏覽器視窗）
    browser = p.chromium.launch(channel="chrome", headless=False)
    # 開啟一個全新的瀏覽器分頁 (Page)
    page = browser.new_page()
    # 讓瀏覽器前往指定網址 (Yahoo 台灣首頁)，並等待 DOM 結構載入完成 (domcontentloaded)
    page.goto("https://tw.yahoo.com/", wait_until="domcontentloaded")
    
    # 選取你要的元素（使用文字定位）
    # Playwright 可以直接點擊，不需要 ActionChains
    # 使用 get_by_role 定位角色為 "link" (超連結) 且顯示名稱為 "拍賣" 的網頁元素
    web_element = page.get_by_role("link", name="拍賣")
    # 印出定位到的 Locator 物件資訊
    print(web_element)
    # 對定位到的元素執行滑鼠左鍵點擊操作
    web_element.click()

    # 接著點擊html中另一個指定元素
    # 【Playwright 自動等待機制說明】：
    # 1. 宣告階段 (page.get_by_role)：屬於「懶載入 (Lazy Evaluation)」，僅建立 Locator 物件，此時「不會」發送請求或等待 DOM 元素出現。
    # 2. 動作階段 (web_element.click())：會自動觸發「自動等待 (Auto-waiting)」，預設最長等待 30 秒。
    #    點擊前會自動進行可操作性檢查 (Actionability Checks)：確認元素 Attached(掛載)、Visible(可見)、Stable(穩定無動畫)、Receives Events(無遮罩) 且 Enabled(可用)。
    web_element = page.get_by_role("link", name="超人氣賣家")
    print(web_element)
    # 執行點擊（此時會自動等待元素載入並達到可操作狀態）
    web_element.click()
   
    # 如果需要保持瀏覽器開啟以便觀察，可以加入等待
    # 暫停程式並等待使用者在終端機按下 ENTER 鍵，防止瀏覽器立即關閉
    input('按一下 ENTER 關閉 browser')
    # 關閉瀏覽器實例
    browser.close()