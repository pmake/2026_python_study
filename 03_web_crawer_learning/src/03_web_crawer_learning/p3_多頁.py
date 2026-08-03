import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from urllib.parse import urljoin

def main():
    # 步驟 1：設定起始目標網址 (URL) 與標頭
    base_url = "https://quotes.toscrape.com/"
    current_url = base_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_quotes_data = []
    page_num = 1

    try:
        # 步驟 2：利用 while 迴圈進行多頁爬取，直到沒有下一頁按鈕
        while current_url:
            print(f"==================================================")
            print(f"正在發送請求至第 {page_num} 頁：{current_url} ...")
            response = requests.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"

            # 使用 BeautifulSoup 解析頁面 HTML
            soup = BeautifulSoup(response.text, "lxml")

            # 步驟 3：抓取每個頁面的 "div.quote" 元素
            quote_elements = soup.select("div.quote")
            print(f"第 {page_num} 頁共找到 {len(quote_elements)} 個格言區塊：\n")

            for idx, quote in enumerate(quote_elements, 1):
                # 取得所有的 span 元素
                spans = quote.select("span")
                
                # 1. 第一個 span 內的文字內容是 "格言 (quote)"
                quote_text = spans[0].get_text(strip=True) if len(spans) > 0 else ""

                # 2. 第二個 span 內的文字是 "作者 (author)"，如果span內含small.author標籤則優先取其姓名，否則取完整文字
                author = ""
                if len(spans) > 1:
                    author_node = spans[1].select_one("small.author")
                    author = author_node.get_text(strip=True) if author_node else spans[1].get_text(strip=True)

                # "div.tags" 底下的 "a" 元素為 "標籤 (tag)"，可能有 1 到多個 tag
                tags_div = quote.select_one("div.tags")
                tags = [a.get_text(strip=True) for a in tags_div.select("a")] if tags_div else []
                tags_str = ", ".join(tags)

                print(f"[{idx}] 格言: {quote_text}")
                print(f"    作者: {author}")
                print(f"    標籤: {tags_str}\n")

                all_quotes_data.append({
                    "頁碼": page_num,
                    "格言(quote)": quote_text,
                    "作者(author)": author,
                    "標籤(tag)": tags_str
                })

            # 步驟 4：檢查是否有換頁按鈕 "li.next a"
            next_btn = soup.select_one("li.next a")
            if next_btn and "href" in next_btn.attrs:
                next_href = next_btn["href"]
                # 使用 urljoin 組合完整的下一頁網址
                current_url = urljoin(current_url, next_href)
                page_num += 1
            else:
                print("未找到 'li.next a' 按鈕，代表已爬取完畢所有頁面！")
                current_url = None

        # 步驟 5：將所有收集到的資料儲存為 Excel 檔案
        if all_quotes_data:
            # 使用 Path(__file__).parent 取得當前腳本所在的目錄，並建立底下的 data 資料夾
            excel_path = Path(__file__).parent / "data" / "quotes_data.xlsx"
            excel_path.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(all_quotes_data)
            df.to_excel(excel_path, index=False)
            print(f"\n任務完成！共爬取 {page_num} 頁、{len(all_quotes_data)} 筆資料，已儲存至 '{excel_path}'")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 錯誤發生：{http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"網路連線錯誤：{conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"請求超時：{timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"發送請求時發生其他錯誤：{req_err}")

if __name__ == "__main__":
    main()

