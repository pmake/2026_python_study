from pathlib import Path
from cloakbrowser import launch

# 取得目前 .py 檔案所在的同層目錄絕對路徑
BASE_DIR = Path(__file__).parent
DEFAULT_COOKIE_PATH = BASE_DIR / "google_auth_state.json"
# 定義專案根目錄
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
print("專案根目錄", DATA_DIR)


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


def outline_single_file(page):
    print("目標頁面標題：", page.title())
    # 定位包含"upload files"文字的元素，然後hover至其上，把滑鼠移過去
    page.get_by_text("upload files").hover()
    # 宣告input type=file name=Filedata的元素
    file_input = page.locator('input[name="Filedata"]')
    # 等待元素掛載到 DOM
    file_input.wait_for(state="attached")
    # 寫一個迴圈遍歷 DATA_DIR 資料夾，取得裡面的3個檔案完整檔名
    for filename in DATA_DIR.glob("*.pdf"):
        print(filename.name)
        # 鎖定 input (name=Filedata) 元素，設定並上傳檔案
        file_input.set_input_files(f"{DATA_DIR}/{filename.name}")
        page.get_by_text("upload files").hover()
        page.wait_for_timeout(10000)  

        # 接下來定位賽文為"Chat" 的span元素並執行點擊，等右邊選單出现
        page.get_by_text("Chat").click()
        # 定位placeholder為"Ask a question or create something" 的textarea元素
        print(123)
        page.get_by_placeholder("Ask a question or create something").fill("請幫我生成這份報告的大綱")
        print("成功輸入問題")
        # 等待頁面載入完成
        page.wait_for_timeout(10000) 
        print("取得AI生成的大綱")
        
        
        # 點擊確定

    input("請檢視頁面，完成後在終端機按下 Enter 鍵結束...")



if not DEFAULT_COOKIE_PATH.exists():
    get_google_auth_token()

# 使用儲存的登入狀態造訪指定頁面
visit_pages_with_google_auth("https://notebook.google.com/notebook/d9609d27-f9d7-4240-85c1-8af65ceb212b", outline_single_file)

# 關閉瀏覽器實例並釋放資源
browser.close()
