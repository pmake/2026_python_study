from playwright.sync_api import sync_playwright

with sync_playwright() as p:
   
    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )
    context = browser.new_context()

    # 建立新分頁
    page = context.new_page()

    # 導航至指定網址
    page.goto("https://tw.news.yahoo.com/",wait_until="domcontentloaded")

    # 等待 2 秒（2000 毫秒）
    page.wait_for_timeout(5000)

    # 重新載入頁面
    page.reload(wait_until="domcontentloaded")

    # 再等待 1 秒
    page.wait_for_timeout(4000)

    # 關閉當前分頁
    page.close()

    print('目前進入暫停位置，如要關閉點擊Enter後離開')
    input()    

    browser.close()