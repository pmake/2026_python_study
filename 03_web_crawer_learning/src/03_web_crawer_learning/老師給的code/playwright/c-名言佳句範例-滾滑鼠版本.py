from playwright.sync_api import sync_playwright, TimeoutError

url = 'http://www.webscrapingfordatascience.com/complexjavascript/'

with sync_playwright() as p:
        # 用 Chromium，也可以改成 firefox / webkit
        browser = p.chromium.launch(channel="chrome",headless=False)
        page = browser.new_page()
        page.goto(url)

        # 無限捲動的 div
        div_element = page.locator(".infinite-scroll")
        # 所有 quote 元素
        quotes = page.locator(".quote")

        nr_quotes = 0
        index=0
        while True:
            # 點一下 div，確保焦點在它上面
            div_element.click()

            # 按 PageDown 5 次（模擬往下捲）
            for _ in range(5):
                page.locator(".quote").hover
                index=index+100
                page.mouse.wheel(0, index)
     

            # 等「第 nr_quotes 個 quote」出現
            # 例如原本有 0 個，就等 index 0 出現；原本有 10 個，就等 index 10 出現
            try:
                quotes.nth(nr_quotes).wait_for(state="attached", timeout=3000)
            except TimeoutError:
                # 3 秒內沒有新 quote 出現 → 代表真的沒東西了
                print("... done!")
                break

            # 更新 quote 數量
            nr_quotes = quotes.count()
            print("... 現在一共看到", nr_quotes, "quotes")

        # 最終拿到全部 quotes
        total = quotes.count()
        print(total, "quotes 被發現\n")
        for i in range(total):
            text = quotes.nth(i).text_content()
            print(text)

        input("按一下 ENTER 關閉 browser")
        browser.close()