from pathlib import Path
from cloakbrowser import launch
from playwright.sync_api import TimeoutError

import time
import pyperclip

# 取得目前 .py 檔案所在的同層目錄絕對路徑
BASE_DIR = Path(__file__).parent
DEFAULT_COOKIE_PATH = BASE_DIR / "google_auth_state.json"
# 定義pdf所在的資料夾路徑
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
print("pdf所在的資料夾", DATA_DIR)


# 啟動 CloakBrowser 防偵測 Chromium 瀏覽器實例
browser = launch(
    headless=False  # 設定為非無頭模式（True 代表背景執行不顯示視窗，False 會顯示瀏覽器 GUI）
)


def get_google_auth_token(cookie_path=DEFAULT_COOKIE_PATH):
    """
    開啟 Google 首頁，由使用者手動完成登入後，將登入狀態（Cookies/Storage）儲存至檔案。
    """
    context = browser.new_context()
    page = context.new_page()

    # 讓分頁前往（導覽至）指定的網址
    page.goto("https://google.com")
    print("當前頁面標題：", page.title())

    # 定位 Google 登入按鈕並點擊
    login_btn = page.locator('a[href*="accounts.google.com"]').first
    if login_btn.is_visible():
        login_btn.click()

    # 暫停程式執行，等待使用者在終端機手動完成登入
    print("請於開啟的瀏覽器視窗中手動完成 Google 帳號登入...")
    input("手動完成登入後，請在終端機按下 Enter 鍵以儲存登入狀態...")

    # 把目前已登入的狀態存成指定名稱的 JSON 檔案
    context.storage_state(path=cookie_path)
    print(f"登入狀態已成功儲存至：{cookie_path}")
    
    context.close()


def visit_pages_with_google_auth(url, action, cookie_path=DEFAULT_COOKIE_PATH):
    """
    載入指定路徑的登入狀態 JSON 檔，建立帶有驗證資訊的 Context 並造訪目標網頁。
    若偵測到未登入或 Cookie 已過期，會自動清除舊狀態並重新要求登入。
    """
    # 確保存在登入狀態檔，若無則先建立
    if not cookie_path.exists():
        get_google_auth_token(cookie_path)

    # 建立帶有 Google Auth 登入狀態資訊的 Context 與分頁
    context = browser.new_context(storage_state=cookie_path)
    auth_page = context.new_page()

    auth_page.goto(url)

    # 檢查是否被重新導向至 Google 登入頁面（代表 Cookie 已過期）
    if "accounts.google.com" in auth_page.url:
        print("⚠️ 偵測到登入狀態已過期，正在重新手動登入...")
        context.close()
        cookie_path.unlink(missing_ok=True)
        get_google_auth_token(cookie_path)

        # 重新建立帶有新 Token 的 Context
        context = browser.new_context(storage_state=cookie_path)
        auth_page = context.new_page()
        auth_page.goto(url)

    action(auth_page)

    context.close()

# 要對網頁執行的動作
def outline_single_file(page):
    print("目標頁面標題：", page.title())
    # 先將視窗放到最大，否則RWD可能會將相關介面藏起來
    page.set_viewport_size({"width": 1920, "height": 1080})

    # 取得 DATA_DIR 資料夾，裡面的所有檔案完整含檔名路徑
    files_inside_given_folder = []
    for filename in DATA_DIR.glob("*.pdf"):
        files_inside_given_folder.append(filename)
    print("檔案列表：", files_inside_given_folder)
    

    # 依檔案數量，執行對應次數的處理
    for f in files_inside_given_folder:
        print(f'目前處理檔案：{f}')
        # 判斷是否存在既有來源
        try:
            page.get_by_role("checkbox", name="Select all sources").wait_for(state="attached", timeout=3000)
            print("有既存來源")

            # 先移除既存來源
            page.get_by_role("checkbox", name="Select all sources").wait_for(state="visible", timeout=3000)
            page.get_by_role("button", name="More").first.click()
            page.get_by_role("menuitem", name="Remove source").click()
            page.get_by_role("button", name="Delete").click()
            print("已移除所有來源")

            
        except TimeoutError:
            print("沒有來源")
            pass

        # 移除對話紀錄。放在移除來源的外面，避免只移除了來源卻有舊對話紀錄存在的情況
        page.get_by_role("button", name="Chat options").click()
        delete_chat_btn =  page.get_by_role("menuitem", name="Delete chat history Chat")
        if delete_chat_btn.is_disabled():
            print("沒有對話紀錄")
        else:
            page.get_by_role("menuitem", name="Delete chat history Chat").click()
            page.get_by_role("button", name="Delete").click()
            print("已移除對話紀錄")

        # 上傳新檔案
        # 檢查上傳介面是否出現在畫面上，若沒有就點擊上傳介面
        try:
            page.get_by_role("button", name="Upload files").wait_for(state="attached", timeout=3000)
            print("上傳介面已出現在畫面上")
        except Exception:
            print("沒有上傳介面")
            # 有抖動bug導致新增source無法被定位，先滑鼠點擊一下才會正常
            page.mouse.click(10, 10)
            page.get_by_role("button", name="Add source").click()
            print("點擊Add sources")

        # 定位包含"upload files"文字的元素，然後hover至其上，把滑鼠移過去，以產生file input元素
        page.get_by_text("upload files").hover()
        # 宣告input type=file name=Filedata的元素
        file_input = page.locator('input[name="Filedata"]')
        # 等待元素掛載到 DOM
        file_input.wait_for(state="attached")
        # 定位 input (name=Filedata) 元素，並上傳檔案
        file_input.set_input_files(f)
        
        # 等待上傳完成，以「動態讀取中」的 SVG (indeterminate-circle) 消失為判斷依據
        # 避免誤抓到常駐在頁面上的 determinate-circle 導致逾時
        loading_locator = page.locator("circle.mdc-circular-progress__indeterminate-circle, [role='progressbar']")
        try:
            loading_locator.first.wait_for(state="attached", timeout=3000)
        except Exception:
            print("未找到動態載入圈")
            pass

        # 等待所有動態載入圈隱藏/消失
        try:
            print("正在等待檔案上傳完成...")
            for loader in loading_locator.all():
                loader.wait_for(state="hidden")
            print("檔案已上傳完成")
        except Exception:
            print("檔案已上傳，但有動態載入圈未消失")

        
        # 點擊對話框輸入問題
        textarea = page.get_by_role("textbox", name="Query box")
        textarea.click()
        textarea.fill("幫我摘要10個重點")
        textarea.press("Enter")

        # 等待結果產生
        try:
            print("摘要產生中...")
            page.get_by_role("button", name="Stop generating").wait_for(state="hidden", timeout=60000)
            print("摘要已產生")
        except TimeoutError:
            print("摘要未在60秒內產生")
            pass


        # 複製摘要另存
        # 1. 等待最後一個copy按鈕出現
        time.sleep(3)
        # 2. 點擊複製按鈕
        page.get_by_role("button", name="Copy model response to").last.click()
        # 3. 稍等 0.5 秒確保瀏覽器已將內容寫入系統剪貼簿
        time.sleep(0.5)
        # 4. 取得剪貼簿內容
        summary_content = pyperclip.paste()
        # 5. 以原 PDF 檔名產生 .md 檔（例如 "報告.pdf" 轉為 "報告.md"）
        output_md_path = f.with_suffix(".md")
        output_md_path.write_text(summary_content, encoding="utf-8")
        print(f"✅ 已成功將摘要存至：{output_md_path.name}")


    input("請檢視頁面，完成後在終端機按下 Enter 鍵結束...")
    return
    

    
    

# 使用儲存的登入狀態造訪指定頁面（若未登入或過期會自動觸發登入流程）
visit_pages_with_google_auth("https://notebook.google.com/notebook/c908d939-45fe-4812-a29b-a392ab25e575", outline_single_file)

# 關閉瀏覽器實例並釋放資源
browser.close()


# 錄制內容
# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(channel="chrome", headless=False)
#     context = browser.new_context(storage_state="03_web_crawer_learning/src/03_web_crawer_learning/老師給的code/playwright/google_auth_state.json")
#     page = context.new_page()
#     page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
#     page.get_by_role("button", name="More").click()
#     page.get_by_role("menuitem", name="Remove source").click()
#     page.get_by_role("button", name="Delete").click()
#     page.get_by_role("button", name="Chat options").click()
#     page.get_by_role("menuitem", name="Delete chat history Chat").click()
#     page.get_by_role("button", name="Delete").click()
#     page.get_by_role("button", name="Add source").click()
#     page.get_by_role("button", name="Upload files").click()
#     page.locator("input[name=\"Filedata\"]").set_input_files("華南投顧-8215-明基材-1150805.pdf")
#     page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
#     page.get_by_role("textbox", name="Query box").click()
#     page.get_by_role("textbox", name="Query box").fill("")
#     page.get_by_role("textbox", name="Query box").press("CapsLock")
#     page.get_by_role("textbox", name="Query box").fill("幫我摘要10個重點")
#     page.get_by_role("button", name="Copy model response to").click()
#     page.get_by_role("button", name="Chat options").click()
#     page.get_by_role("menuitem", name="Delete chat history Chat").click()
#     page.get_by_role("button", name="Delete").click()
#     page.get_by_role("button", name="Chat options").click()
#     page.locator(".cdk-overlay-backdrop").click()
#     page.get_by_role("button", name="More").click()
#     page.get_by_role("menuitem", name="Remove source").click()
#     page.get_by_role("button", name="Cancel").click()
#     page.get_by_role("checkbox", name="華南投顧-8215-明基材-1150805.pdf").uncheck()
#     page.get_by_role("checkbox", name="華南投顧-8215-明基材-1150805.pdf").check()
#     page.get_by_role("button", name="More").click()
#     page.get_by_role("menuitem", name="Remove source").click()
#     page.get_by_role("button", name="Delete").click()
#     page.get_by_role("button", name="Add source").click()
#     page.get_by_role("button", name="Upload files").click()
#     page.locator("input[name=\"Filedata\"]").set_input_files("華南投顧-6805-富世達-1150805.pdf")
#     page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
#     page.get_by_role("textbox", name="Query box").click()
#     page.get_by_role("textbox", name="Query box").fill("幫i")
#     page.get_by_role("textbox", name="Query box").press("ArrowUp")
#     page.get_by_role("textbox", name="Query box").press("ArrowLeft")
#     page.get_by_role("textbox", name="Query box").fill("幫i")
#     page.get_by_role("textbox", name="Query box").press("ArrowRight")
#     page.get_by_role("textbox", name="Query box").fill("幫i")
#     page.get_by_role("textbox", name="Query box").press("ArrowRight")
#     page.get_by_role("textbox", name="Query box").fill("幫我產生10個重點摘要")
#     page.get_by_role("textbox", name="Query box").click()
#     page.get_by_role("textbox", name="Query box").fill("123")
#     page.get_by_role("button", name="Stop generating").click()
#     page.get_by_role("button", name="Stop").click()
#     page.get_by_role("button", name="Add source").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)

