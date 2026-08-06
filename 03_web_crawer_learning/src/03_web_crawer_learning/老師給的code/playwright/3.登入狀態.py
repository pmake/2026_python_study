"""
示範如何載入既有的 Google 登入 storage state，並在新的 Playwright
瀏覽器情境中直接沿用先前的登入狀態。

使用前請先確保已透過其他腳本或 `context.storage_state(path=...)`
產生 `google_storage_state.json`。
"""

from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

STORAGE_STATE_PATH = Path("google_storage_state.json")



def bootstrap_google_login(playwright: Playwright) -> None:
    """
    第一次登入：開啟 Gmail，請使用者手動完成 Google 驗證，
    完成後在終端機按 Enter，接著匯出 storage_state。
    """
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False, slow_mo=200,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
        ] 
    )
    
    context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-TW',
            timezone_id='Asia/Taipei',
        )
    page = context.new_page()
    page.goto("https://mail.google.com", wait_until="domcontentloaded")

    input("請在瀏覽器中完成 Google 登入，完成後回到終端機按 Enter 繼續：")

    context.storage_state(path=str(STORAGE_STATE_PATH))
    browser.close()


def open_google_with_saved_state(playwright: Playwright) -> None:
    """用既有 storage_state 啟動 context，並驗證是否仍為登入狀態。"""
    browser = playwright.chromium.launch(headless=False)
    # 載入既有 storage state 瀏覽器會關閉重開一下
    context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
    page = context.new_page()

    page.goto("https://mail.google.com", wait_until="domcontentloaded")
    print('目前進入作戰位置，如要關閉點擊Enter後離開')
    input()

    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        # 問檔案存不存在
        if not STORAGE_STATE_PATH.exists():
            print("偵測到尚未建立 storage state，將引導完成一次登入流程。")
            bootstrap_google_login(playwright)
        else:
            print("找到既有 storage state，直接載入登入狀態。")

        open_google_with_saved_state(playwright)


if __name__ == "__main__":
    main()

