from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=False)
    page = browser.new_page()
    page.goto("https://www.momoshop.com.tw/")

    page.get_by_text("手機/相機").click()
    
    # 時間火候是個關鍵
    # 等待「攝相機」連結出現並可見
    main_menu = page.locator("#C10")
    # 等10秒
    main_menu.wait_for(state="visible", timeout=10000)
    
    # 將滑鼠移動到「攝相機」元素上（hover）
    main_menu.hover()
    
    # 等「安卓手機」出現
    # 等待「安卓手機」連結出現並可見

    # 第一種定位方法
    sub_menu = page.locator("a[btid='1500100008']").all()
    first_item = sub_menu[0]
    first_item.wait_for(state="visible", timeout=10000)
    first_item.click()
    
    # 第二種定位方法
    # sub_menu = page.locator("xpath=/html/body/div[1]/div[2]/div/div/div[1]/div[1]/table/tbody/tr/td[4]/ul/li[2]/a")
    # sub_menu.wait_for(state="visible", timeout=10000)
    # sub_menu.click()
    
 
    
    # 如果需要保持瀏覽器開啟以便觀察，可以加入等待
    input('按一下 ENTER 關閉 browser')
    browser.close()