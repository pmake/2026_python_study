from pathlib import Path
from cloakbrowser import launch

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
    """
    # 建立帶有 Google Auth 登入狀態資訊的 Context 與分頁
    context = browser.new_context(storage_state=cookie_path)
    auth_page = context.new_page()

    auth_page.goto(url)
    action(auth_page)

    context.close()

# 要對網頁執行的動作
def outline_single_file(page):
    print("目標頁面標題：", page.title())
    # 先上傳所有pdf檔案
    # 寫一個迴圈遍歷 DATA_DIR 資料夾，取得裡面的3個檔案完整檔名
    for filename in DATA_DIR.glob("*.pdf"):
        print(filename.name)
        # 檢查上傳介面是否出現在畫面上，若沒有就點擊上傳介面
        if not page.get_by_role("button", name="Upload files").is_visible():
            page.get_by_role("button", name="Add source").click()
        else:
            print("上傳介面已出現在畫面上")
            # 定位包含"upload files"文字的元素，然後hover至其上，把滑鼠移過去，以產生file input
            page.get_by_text("upload files").hover()
            # 宣告input type=file name=Filedata的元素
            file_input = page.locator('input[name="Filedata"]')
            # 等待元素掛載到 DOM
            file_input.wait_for(state="attached")
            # 定位 input (name=Filedata) 元素，並上傳檔案
            file_input.set_input_files(f"{DATA_DIR}/{filename.name}")
        
        
        # 定位placeholder為"Ask a question or create something" 的textarea元素
        textrea = page.get_by_placeholder("Ask a question or create something")
        textrea.fill("請幫我生成這份報告的大綱")
        # 等待已上傳文件的元素出現
        page.get_by_role("checkbox", name=filename.name).wait_for(state="attached")
        # 送出enter鍵點擊
        textrea.press("Enter")
        # 等待頁面載入完成
        print("取得AI生成的大綱")
        # 點擊確定

    input("請檢視頁面，完成後在終端機按下 Enter 鍵結束...")
    
    
    try:
        
    
    
    



if not DEFAULT_COOKIE_PATH.exists():
    get_google_auth_token()

# 使用儲存的登入狀態造訪指定頁面
visit_pages_with_google_auth("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b", outline_single_file)

# 關閉瀏覽器實例並釋放資源
browser.close()


# 錄制內容
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context(storage_state="03_web_crawer_learning/src/03_web_crawer_learning/老師給的code/playwright/google_auth_state.json")
    page = context.new_page()
    page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
    page.get_by_role("button", name="More").click()
    page.get_by_role("menuitem", name="Remove source").click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Chat options").click()
    page.get_by_role("menuitem", name="Delete chat history Chat").click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Add source").click()
    page.get_by_role("button", name="Upload files").click()
    page.locator("input[name=\"Filedata\"]").set_input_files("華南投顧-8215-明基材-1150805.pdf")
    page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
    page.get_by_role("textbox", name="Query box").click()
    page.get_by_role("textbox", name="Query box").fill("")
    page.get_by_role("textbox", name="Query box").press("CapsLock")
    page.get_by_role("textbox", name="Query box").fill("幫我摘要10個重點")
    page.get_by_role("button", name="Copy model response to").click()
    page.get_by_role("button", name="Chat options").click()
    page.get_by_role("menuitem", name="Delete chat history Chat").click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Chat options").click()
    page.locator(".cdk-overlay-backdrop").click()
    page.get_by_role("button", name="More").click()
    page.get_by_role("menuitem", name="Remove source").click()
    page.get_by_role("button", name="Cancel").click()
    page.get_by_role("checkbox", name="華南投顧-8215-明基材-1150805.pdf").uncheck()
    page.get_by_role("checkbox", name="華南投顧-8215-明基材-1150805.pdf").check()
    page.get_by_role("button", name="More").click()
    page.get_by_role("menuitem", name="Remove source").click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Add source").click()
    page.get_by_role("button", name="Upload files").click()
    page.locator("input[name=\"Filedata\"]").set_input_files("華南投顧-6805-富世達-1150805.pdf")
    page.goto("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b?pli=1")
    page.get_by_role("textbox", name="Query box").click()
    page.get_by_role("textbox", name="Query box").fill("幫i")
    page.get_by_role("textbox", name="Query box").press("ArrowUp")
    page.get_by_role("textbox", name="Query box").press("ArrowLeft")
    page.get_by_role("textbox", name="Query box").fill("幫i")
    page.get_by_role("textbox", name="Query box").press("ArrowRight")
    page.get_by_role("textbox", name="Query box").fill("幫i")
    page.get_by_role("textbox", name="Query box").press("ArrowRight")
    page.get_by_role("textbox", name="Query box").fill("幫我產生10個重點摘要")
    page.get_by_role("textbox", name="Query box").click()
    page.get_by_role("textbox", name="Query box").fill("123")
    page.get_by_role("button", name="Stop generating").click()
    page.get_by_role("button", name="Stop").click()
    page.get_by_role("button", name="Add source").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

