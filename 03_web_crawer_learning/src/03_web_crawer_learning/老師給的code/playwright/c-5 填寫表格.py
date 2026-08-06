from playwright.sync_api import sync_playwright

url = 'http://www.webscrapingfordatascience.com/postform2/'

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=False)
    page = browser.new_page()
    page.goto(url)
    
    # 填寫姓名欄位
    page.locator('input[name="name"]').fill('Jeff')
    
    # 選擇性別（單選按鈕）
    # attribution的選擇，一個property一個[]
    page.locator('input[name="gender"][value="M"]').click()
    
    # 勾選複選框
    page.locator('input[name="pizza"]').click()
    page.locator('input[name="salad"]').click()
    
    # 選擇下拉選單
    # Playwright 中可以直接使用 select_option() 方法
    page.locator('select[name="haircolor"]').select_option(value='brown')
    
    # 填寫多行文字（comments）
    # Playwright 中可以使用 \n 來表示換行
    page.locator('textarea[name="comments"]').fill('Jeff is good.\nJeff is perfect.')
    
    input('按一下 ENTER 送出表格')
    # Playwright 中提交表單可以使用 evaluate() 方法
    # 或者直接點擊 submit 按鈕
    page.locator('form').evaluate('form => form.submit()')
    
    # 或者: page.locator('input[type="submit"]').click()
    
    input('按一下 ENTER 關閉 browser')
    browser.close()