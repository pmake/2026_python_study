from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=False)
    page = browser.new_page()
    page.goto("https://tw.yahoo.com/", wait_until="domcontentloaded")
    
    # 選取你要的元素（使用文字定位）
    # Playwright 可以直接點擊，不需要 ActionChains
    web_element = page.get_by_role("link", name="拍賣")
    print(web_element)
    web_element.click()
   
    
    # 如果需要保持瀏覽器開啟以便觀察，可以加入等待
    input('按一下 ENTER 關閉 browser')
    browser.close()