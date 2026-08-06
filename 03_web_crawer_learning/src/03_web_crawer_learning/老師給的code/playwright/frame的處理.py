from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=False)
    
    # 第一種寫法
    # context = browser.new_context(
    #         viewport={'width': 1920, 'height': 1080},
    #     )
    # page = context.new_page()

    # 第二種寫法
    # 使用 page.set_viewport_size() 設定視窗大小
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

   
    page.goto("https://jumbofun.neocities.org/iframe")
    
    # 切換到 iframe（索引 1，即第二個 iframe）
    # Playwright 中可以使用 frame_locator 或獲取 frame 物件
    # 方法1: 使用 frame_locator（推薦，更簡潔）
    frame = page.frame_locator('iframe').nth(1)
    
    # 方法2: 或使用 page.frames 獲取所有 frame，然後選擇索引 1
    # frames = page.frames
    # if len(frames) > 1:
    #     frame = frames[1]
    
   
    
    
    # 等待「關於起士」連結出現並可見
    target_menu = frame.get_by_text("關於起士").nth(0) 
    target_menu.wait_for(state="visible", timeout=10000)
    # 將滑鼠移動到「關於起士」元素上（hover）
    target_menu.hover()
    
    # 等待「銷售據點」連結出現並可見
    sub_menu = frame.get_by_text("銷售據點").nth(0)
    sub_menu.wait_for(state="visible", timeout=10000)
    
    # 點擊「銷售據點」連結
    sub_menu.click()
    
    # 如果需要保持瀏覽器開啟以便觀察，可以加入等待
    input('按一下 ENTER 關閉 browser')
    browser.close()