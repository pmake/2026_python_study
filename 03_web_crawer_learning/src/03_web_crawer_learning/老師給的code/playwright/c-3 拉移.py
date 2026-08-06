from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=False)
    page = browser.new_page()
    page.goto('http://sahitest.com/demo/dragDropMooTools.htm')
    
    # 被拖拽元素
    dragger = page.locator('#dragger')
    # 目標元素1
    item1 = page.locator('div:has-text("Item 1")')
    
    # Playwright 中拖放操作可以直接使用 drag_to() 方法
    # 這相當於 Selenium 的 click_and_hold -> move_to_element -> release
    dragger.drag_to(item1)
    
    # 如果需要保持瀏覽器開啟以便觀察，可以加入等待
    input('按一下 ENTER 關閉 browser')
    browser.close()