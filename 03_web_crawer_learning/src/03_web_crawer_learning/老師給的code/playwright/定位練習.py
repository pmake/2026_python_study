"""
https://playwright.dev/python/docs/locators
"""

from pathlib import Path  # 匯入 pathlib 模組中的 Path 類別，用於處理檔案與目錄路徑
from typing import Callable, List  # 匯入 typing 模組的 Callable 與 List，用於型別標註 (Type Hints)
import re  # 匯入標準庫 re 模組，提供正則表達式功能
from playwright.sync_api import Page, expect, sync_playwright  # 從 Playwright 同步 API 匯入 Page 頁面物件、expect 斷言模組與 sync_playwright 啟動入口


def locate_by_role(page: Page) -> None:  # 定義依據 ARIA 角色 (Role) 定位頁面元素的練習函式
    """最佳首選：ARIA 角色搭配名稱，互動元素最穩定。"""  # 函式說明文件字串 (Docstring)
    signin_btn = page.get_by_role("button", name="Sign in")  # 取得角色為 "button" 且可見名稱為 "Sign in" 的按鈕 Locator
    signin_btn.hover()  # 將滑鼠游標懸停 (hover) 到該按鈕元素上方
    signin_btn.click()  # 點擊該 Sign in 按鈕


def locate_by_text(page: Page) -> None:  # 定義依據可見文字內容 (Text) 定位元素的練習函式
    """以元素可見文字尋找內容或按鈕。"""  # 函式說明文件字串 (Docstring)
    page.get_by_text("前往 momo 購物網").click()  # 尋找包含文字 "前往 momo 購物網" 的元素並執行點擊
    page.bring_to_front()  # 將當前分頁視窗帶到最前端焦點, 如果上一個點擊有開新tab，此指令就會將原tab拉回焦點
    


def locate_by_label(page: Page) -> None:  # 定義依據標籤文字 (Label) 定位輸入框的練習函式
    """表單欄位首選：依 label 對應 input。"""  # 函式說明文件字串 (Docstring)
    page.get_by_label("User Name").fill("Jeff")  # 尋找對應 Label 文字為 "User Name" 的輸入框並輸入 "Jeff"
    page.get_by_label("Email").fill("abc@gmail.com")  # 尋找對應 Label 文字為 "Email" 的輸入框並輸入 "abc@gmail.com"

def locate_by_placeholder(page: Page) -> None:  # 定義依據預設占位文字 (Placeholder) 定位輸入框的練習函式
    """沒有 label 時，用 placeholder 辨識輸入框。"""  # 函式說明文件字串 (Docstring)
    page.get_by_placeholder("輸入安全代碼").fill("123456789")  # 尋找占位文字為 "輸入安全代碼" 的輸入框並填入 "123456789"
    page.get_by_role("button", name="Subscribe").click()  # 點擊角色為 button 且名稱為 "Subscribe" 的訂閱按鈕


def locate_by_alt_text(page: Page) -> None:  # 定義依據圖片替代文字 (Alt Text) 定位圖像元素的練習函式
    """依圖片說明文字（alt）定位圖像。"""  # 函式說明文件字串 (Docstring)
    page.get_by_alt_text("gotoYahoo").click()  # 點擊 alt 屬性為 "gotoYahoo" 的圖片元素
    page.bring_to_front()  # 將當前分頁視窗帶到最前端焦點
    


def locate_by_title(page: Page) -> None:  # 定義依據 HTML title 屬性定位元素的練習函式
    """利用 title 屬性（較少用，但可當備案）。"""  # 函式說明文件字串 (Docstring)
    page.get_by_title("Issues count").click()  # 點擊 title 屬性內容為 "Issues count" 的 HTML 元素
    # page.get_by_role("button", name="顯示 Issue 數量").click()  # 註解備註：替代方案，可使用 get_by_role 定位按鈕


def locate_by_test_id(page: Page) -> None:  # 定義依據測試識別碼 (data-testid) 定位元素的練習函式
    """若頁面提供 data-testid，這是最穩定的測試專用定位。"""  # 函式說明文件字串 (Docstring)
    page.get_by_test_id("buy").click()  # 點擊 data-testid 屬性等於 "buy" 的元素


def locate_by_css(page: Page) -> None:  # 定義依據 CSS 選擇器 (CSS Selector) 定位元素的練習函式
    """CSS 選擇器，語意化定位失敗時再使用。"""  # 函式說明文件字串 (Docstring)
    page.locator("#id .class > span").first.click()  # 使用 CSS 選擇器尋找符合條件的第一個 (first) span 元素並點擊


def locate_by_xpath(page: Page) -> None:  # 定義依據 XPath 路徑語法定位元素的練習函式
    """XPath 為最後備援，冗長且容易壞。"""  # 函式說明文件字串 (Docstring)
    page.locator("//div[@id='abc']").click()  # 使用 XPath 路徑找到 id 為 'abc' 的 div 元素並執行點擊



def filter_locators(page: Page) -> None:  # 定義利用 filter 鏈式過濾進行精準定位的練習函式
    """filter() 透過文字或子元素縮小範圍。"""  # 函式說明文件字串 (Docstring)
    
    # get_by_role("button", name="Add to cart") 
    # 會優先匹配按鈕的 aria-label，而不是可見文字。
    # 按鈕的 aria-label 是 "Add Product 2 to cart"，不是 "Add to cart"，因此定位不到。

    # 方案 1：使用完整的 aria-label
    page.get_by_role("listitem") \
        .filter(has_text="Product 2") \
        .get_by_role("button", name="Add Product 2 to cart") \
        .click()  # 點擊該按鈕
    
    # 方案 2：使用正則表達式匹配（已註解，可選用）
    # page.get_by_role("listitem") \
    #     .filter(has_text="Product 2") \
    #     .get_by_role("button", name=re.compile("Add.*cart")) \
    #     .click()
    
    # 方案 3：使用文字定位（已註解，可選用）
    # page.get_by_role("listitem") \
    #     .filter(has_text="Product 2") \
    #     .get_by_text("Add to cart") \
    #     .click()
    
    # 方案 4：因為已經 filter 縮小範圍，可以直接用 button 角色（已註解，可選用）
    # page.get_by_role("listitem") \
    #     .filter(has_text="Product 2") \
    #     .get_by_role("button") \
    #     .click()


    

def nth_first_last(page: Page) -> None:  # 定義使用索引與位置 (nth/first/last) 取得指定元素的練習函式
    """nth()/first()/last() 取得指定順位元素。"""  # 函式說明文件字串 (Docstring)
    page.get_by_role("listitem").nth(1).click()  # 取得所有 listitem 匹配結果中索引為 1 (即第 2 個) 的項目並執行點擊


def combine_and(page: Page) -> None:  # 定義使用 and_() 組合多重條件 (交集) 定位的練習函式
    """and_() 同時滿足多個條件。"""  # 函式說明文件字串 (Docstring)
    page.get_by_role("button").and_(page.get_by_title("Subscribe")).click()  # 找到既是 button 角色且 title 為 "Subscribe" 的元素並執行點擊


def combine_or(page: Page) -> None:  # 定義處理條件分支與動態對話框互動的練習函式
    """or_() 任一 locator 成功即可。"""  # 函式說明文件字串 (Docstring)
    new_btn = page.get_by_role("button", name="New")  # 取得名稱為 "New" 的按鈕 Locator
    dialog = page.get_by_text("Confirm security settings")  # 取得包含 "Confirm security settings" 文字的 Locator
    
    if new_btn.is_visible():  # 檢查 "New" 按鈕目前是否在頁面上可見
        new_btn.click()  # 若 "New" 按鈕可見，則執行點擊
    elif dialog.is_visible():  # 若 "New" 按鈕不可見，再檢查對話框文字是否可見
        dialog.click()  # 若對話框可見，則執行點擊
    
    page.wait_for_timeout(5000)  # 讓頁面強制停頓等待 5000 毫秒 (5 秒)
    dialog_close_btn = page.get_by_role("button", name="確定")  # 取得名稱為 "確定" 的對話框關閉按鈕 Locator

    if dialog_close_btn.is_visible():  # 檢查 "確定" 按鈕是否在頁面上可見
        dialog_close_btn.click()  # 若可見則點擊 "確定" 按鈕以關閉對話框
    


def count_and_text(page: Page) -> None:  # 定義驗證元素數量與進行斷言 (Expect Assertion) 的練習函式
    """count()/to_have_text() 驗證清單數量與內容。"""  # 函式說明文件字串 (Docstring)
    listitems = page.get_by_role("listitem")  # 取得所有角色為 listitem 的元素集合 Locator
    expect(listitems).to_have_count(6)  # 使用 expect 斷言工具驗證 listitem 的數量精確等於 6 個
    input()  # 暫停 Python 程式執行，等待使用者在命令列介面 (Terminal) 按下 Enter 鍵繼續



def strict_mode_example(page: Page) -> None:  # 定義展示 Playwright 嚴格模式 (Strict Mode) 機制的練習函式
    """Strict Mode：定位太寬鬆會報錯，提醒要加條件。"""  # 函式說明文件字串 (Docstring)
    page.get_by_role("button", name="Sign in").click()  # 點擊名稱為 "Sign in" 的按鈕 (若有多個匹配將觸發 Strict Mode 錯誤)


def main() -> None:  # 定義主程式流程進入點函式
    """開啟本地 placeholder.html，逐一執行練習函式。"""  # 函式說明文件字串 (Docstring)
    html_path = Path(__file__).parent / "html" / "placeholder.html"  # 使用 Path 計算相對於目前指令碼位置的本地 HTML 檔案路徑
    if not html_path.exists():  # 檢查目標 HTML 檔案是否存在於指定路徑
        raise FileNotFoundError(f"找不到練習檔案：{html_path}")  # 若檔案不存在則拋出 FileNotFoundError 例外

    exercises: List[Callable[[Page], None]] = [  # 宣告包含所有定位練習函式的列表，型別標註為 Callable[[Page], None] 的列表
        locate_by_role,  # 練習 1：依據 Role 角色定位
        locate_by_text,  # 練習 2：依據 Text 可見文字定位
        locate_by_label,  # 練習 3：依據 Label 標籤定位
        locate_by_placeholder,  # 練習 4：依據 Placeholder 預設文字定位
        locate_by_alt_text,  # 練習 5：依據 Alt Text 圖片說明定位
        locate_by_title,  # 練習 6：依據 Title 屬性定位
        locate_by_test_id,  # 練習 7：依據 Test ID 測試識別碼定位
        locate_by_css,  # 練習 8：依據 CSS Selector 定位
        locate_by_xpath,  # 練習 9：依據 XPath 定位
        filter_locators,  # 練習 10：鏈式過濾器定位
        nth_first_last,  # 練習 11：依據順序位置定位
        combine_and,  # 練習 12：AND 複合條件定位
        combine_or,  # 練習 13：OR 分支條件定位
        count_and_text,  # 練習 14：數量驗證與斷言
    ]

    with sync_playwright() as p:  # 建立與啟動 Playwright 同步物件實例 p 的上下文管理器
        browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=200)  # 啟動 Chrome 瀏覽器 (顯示視窗且每步操作延遲 200 毫秒)
        context = browser.new_context(locale="zh-TW")  # 建立獨立的瀏覽器上下文 (Context)，設定預設語系為繁體中文 (zh-TW)
        page = context.new_page()  # 在當前內容上下文中新建一個分頁 (Page)
        # page.goto(html_path.resolve().as_uri())  # 註解備註：使用 resolved URI 開啟本地 HTML 檔
        page.goto("https://jumbofun.neocities.org/placeholder")  # 控制瀏覽器導航至指定範例網址
        for func in exercises:  # 使用 for 迴圈順序歷遍 exercises 列表中的每個練習函式
            print(f"執行：{func.__name__}")  # 在主控台印出目前正在執行的函式名稱
            func(page)  # 呼叫並執行該練習函式，將 page 頁面實例作為參數傳入

        print("全部定位練習已完成，請確認視窗狀態。")  # 執行完所有練習後印出完成提示文字
        browser.close()  # 關閉瀏覽器實例並釋放相關資源


if __name__ == "__main__":  # 判斷當前模組是否作為主程式直接執行 (而非被 import)
    main()  # 執行 main() 主進入點函式


