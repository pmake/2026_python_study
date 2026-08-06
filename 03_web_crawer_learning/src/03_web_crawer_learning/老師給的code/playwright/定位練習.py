"""
https://playwright.dev/python/docs/locators
"""

from pathlib import Path
from typing import Callable, List
import re
from playwright.sync_api import Page, expect, sync_playwright


def locate_by_role(page: Page) -> None:
    """最佳首選：ARIA 角色搭配名稱，互動元素最穩定。"""
    signin_btn = page.get_by_role("button", name="Sign in")
    signin_btn.hover()
    signin_btn.click()


def locate_by_text(page: Page) -> None:
    """以元素可見文字尋找內容或按鈕。"""
    page.get_by_text("前往 momo 購物網").click()
    page.bring_to_front()
    


def locate_by_label(page: Page) -> None:
    """表單欄位首選：依 label 對應 input。"""
    page.get_by_label("User Name").fill("Jeff")
    page.get_by_label("Email").fill("abc@gmail.com")

def locate_by_placeholder(page: Page) -> None:
    """沒有 label 時，用 placeholder 辨識輸入框。"""
    page.get_by_placeholder("輸入安全代碼").fill("123456789")
    page.get_by_role("button", name="Subscribe").click()


def locate_by_alt_text(page: Page) -> None:
    """依圖片說明文字（alt）定位圖像。"""
    page.get_by_alt_text("gotoYahoo").click()
    page.bring_to_front()
    


def locate_by_title(page: Page) -> None:
    """利用 title 屬性（較少用，但可當備案）。"""
    page.get_by_title("Issues count").click()
    # page.get_by_role("button", name="顯示 Issue 數量").click()


def locate_by_test_id(page: Page) -> None:
    """若頁面提供 data-testid，這是最穩定的測試專用定位。"""
    page.get_by_test_id("buy").click()


def locate_by_css(page: Page) -> None:
    """CSS 選擇器，語意化定位失敗時再使用。"""
    page.locator("#id .class > span").first.click()


def locate_by_xpath(page: Page) -> None:
    """XPath 為最後備援，冗長且容易壞。"""
    page.locator("//div[@id='abc']").click()



def filter_locators(page: Page) -> None:
    """filter() 透過文字或子元素縮小範圍。"""
    
    # get_by_role("button", name="Add to cart") 
    # 會優先匹配按鈕的 aria-label，而不是可見文字。
    # 按鈕的 aria-label 是 "Add Product 2 to cart"，不是 "Add to cart"，因此定位不到。

    # 方案 1：使用完整的 aria-label
    page.get_by_role("listitem") \
        .filter(has_text="Product 2") \
        .get_by_role("button", name="Add Product 2 to cart") \
        .click()
    
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


    

def nth_first_last(page: Page) -> None:
    """nth()/first()/last() 取得指定順位元素。"""
    page.get_by_role("listitem").nth(1).click()


def combine_and(page: Page) -> None:
    """and_() 同時滿足多個條件。"""
    page.get_by_role("button").and_(page.get_by_title("Subscribe")).click()


def combine_or(page: Page) -> None:
    """or_() 任一 locator 成功即可。"""
    new_btn = page.get_by_role("button", name="New")
    dialog = page.get_by_text("Confirm security settings")
    
    if new_btn.is_visible():
        new_btn.click()
    elif dialog.is_visible():
        dialog.click()
    
    page.wait_for_timeout(5000)
    dialog_close_btn = page.get_by_role("button", name="確定")

    if dialog_close_btn.is_visible():
        dialog_close_btn.click()
    


def count_and_text(page: Page) -> None:
    """count()/to_have_text() 驗證清單數量與內容。"""
    listitems = page.get_by_role("listitem")
    expect(listitems).to_have_count(6)
    input()


def strict_mode_example(page: Page) -> None:
    """Strict Mode：定位太寬鬆會報錯，提醒要加條件。"""
    page.get_by_role("button", name="Sign in").click()


def main() -> None:
    """開啟本地 placeholder.html，逐一執行練習函式。"""
    html_path = Path(__file__).parent / "html" / "placeholder.html"
    if not html_path.exists():
        raise FileNotFoundError(f"找不到練習檔案：{html_path}")

    exercises: List[Callable[[Page], None]] = [
        locate_by_role,
        locate_by_text,
        locate_by_label,
        locate_by_placeholder,
        locate_by_alt_text,
        locate_by_title,
        locate_by_test_id,
        locate_by_css,
        locate_by_xpath,
        filter_locators,
        nth_first_last,
        combine_and,
        combine_or,
        count_and_text,
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome",headless=False, slow_mo=200)
        context = browser.new_context(locale="zh-TW")
        page = context.new_page()
        # page.goto(html_path.resolve().as_uri())
        page.goto("https://jumbofun.neocities.org/placeholder")
        for func in exercises:
            print(f"執行：{func.__name__}")
            func(page)

        print("全部定位練習已完成，請確認視窗狀態。")
        browser.close()


if __name__ == "__main__":
    main()

