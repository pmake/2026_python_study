# 從 playwright.sync_api 模組匯入同步模式的 sync_playwright 函式
from playwright.sync_api import sync_playwright

# 使用 with 上下文管理器啟動 Playwright 物件 p，確保離開區塊時會自動清理與釋放資源
with sync_playwright() as p:
    # 啟動 Chromium 瀏覽器（指定使用系統安裝的 Chrome 瀏覽器頻道，並設定 headless=False 以顯示視窗）
    browser = p.chromium.launch(channel="chrome", headless=False)
    
    # 在瀏覽器中建立並開啟一個新的分頁 (Page 物件)
    page = browser.new_page()
    
    # 導覽/前往指定的測試網址 (拖放示範網頁)
    page.goto('http://sahitest.com/demo/dragDropMooTools.htm')
    
    # 使用 CSS ID 選擇器 (#dragger) 定位要被拖拽的來源元素
    dragger = page.locator('#dragger')
    
    # 使用包含文字的選擇器 (div:has-text("Item 1")) 定位目標放置區塊元素
    item1 = page.locator('div:has-text("Item 1")')
    
    # 使用 Playwright 的 drag_to() 方法將來源元素 (dragger) 拖拽並釋放至目標元素 (item1) 上
    # (此方法會自動完成按住、移動、釋放一連串的滑鼠拖放動作)
    dragger.drag_to(item1)
    
    # 呼叫 Python 內建 input() 函式暫停程式，等待使用者按下 Enter 鍵以保留瀏覽器畫面供觀察
    input('按一下 ENTER 關閉 browser')
    
    # 關閉瀏覽器實例
    browser.close()