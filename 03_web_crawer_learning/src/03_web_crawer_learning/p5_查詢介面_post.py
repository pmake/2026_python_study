import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def main():
    # 設定標準輸出編碼為 UTF-8，避免 Windows Console (CP950) 無法印出特殊字元 (例如 'André Gide') 導致崩潰
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # 步驟 1：設定起始目標網址 (URL) 與請求標頭
    base_url = "https://quotes.toscrape.com/search.aspx"
    filter_url = "https://quotes.toscrape.com/filter.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 建立 requests Session 以保持連線狀態
    session = requests.Session()
    session.headers.update(headers)

    all_quotes_data = []

    try:
        # 步驟 2：發送 GET 請求取得初始頁面 (search.aspx)
        print(f"正在存取初始頁面：{base_url} ...")
        res_initial = session.get(base_url, timeout=10)
        res_initial.raise_for_status()
        res_initial.encoding = "utf-8"

        soup_initial = BeautifulSoup(res_initial.text, "lxml")

        # 取得 ASP.NET 的 __VIEWSTATE 隱藏欄位值
        viewstate_node = soup_initial.select_one("#__VIEWSTATE")
        if not viewstate_node:
            print("找不到 __VIEWSTATE 欄位，無法進行 PostBack 操作！")
            return
        initial_viewstate = viewstate_node.get("value", "")

        # 抓取 select#author 元素底下的所有作者 option (過濾掉預設空白選項 '----------')
        author_options = [
            op.get_text(strip=True)
            for op in soup_initial.select("select#author option")
            if op.get_text(strip=True) and op.get_text(strip=True) != "----------"
        ]

        print(f"成功取得作者清單，共找到 {len(author_options)} 位作者。\n")

        # 步驟 3：遍歷所有作者 (author)
        for author_idx, author_name in enumerate(author_options, 1):
            print(f"--------------------------------------------------")
            print(f"[{author_idx}/{len(author_options)}] 選擇作者：{author_name}")

            # 模擬選擇作者觸發 onchange="javascript:__doPostBack()"
            # 發送 POST 請求至 filter.aspx 更新 select#tag 內容
            author_post_data = {
                "author": author_name,
                "__VIEWSTATE": initial_viewstate
            }

            res_author = session.post(filter_url, data=author_post_data, timeout=10)
            res_author.raise_for_status()
            res_author.encoding = "utf-8"

            soup_author = BeautifulSoup(res_author.text, "lxml")

            # 取得更新後的 __VIEWSTATE
            author_viewstate_node = soup_author.select_one("#__VIEWSTATE")
            author_viewstate = author_viewstate_node.get("value", "") if author_viewstate_node else initial_viewstate

            # 抓取更新後的 select#tag 元素底下的所有 tag option (過濾掉預設空白選項 '----------')
            tag_options = [
                op.get_text(strip=True)
                for op in soup_author.select("select#tag option")
                if op.get_text(strip=True) and op.get_text(strip=True) != "----------"
            ]

            print(f"    作者 '{author_name}' 共有 {len(tag_options)} 個對應標籤 (Tag): {tag_options}")

            # 步驟 4：遍歷該作者對應的所有標籤 (tag)
            for tag_name in tag_options:
                # 模擬選擇 author + tag 並點擊 "Search" 按鈕 (input.btn.btn-default)
                search_post_data = {
                    "author": author_name,
                    "tag": tag_name,
                    "submit_button": "Search",
                    "__VIEWSTATE": author_viewstate
                }

                res_search = session.post(filter_url, data=search_post_data, timeout=10)
                res_search.raise_for_status()
                res_search.encoding = "utf-8"

                soup_search = BeautifulSoup(res_search.text, "lxml")

                # 抓取頁面中新增對應的 "div.quote" 元素
                quote_elements = soup_search.select("div.quote")

                for quote_item in quote_elements:
                    # "div.quote" 底下有 3 個 span，依序是 quote, author, tag
                    spans = quote_item.select("span")

                    quote_text = spans[0].get_text(strip=True) if len(spans) > 0 else ""
                    quote_author = spans[1].get_text(strip=True) if len(spans) > 1 else ""
                    quote_tag = spans[2].get_text(strip=True) if len(spans) > 2 else ""

                    print(f"        -> [格言]: {quote_text}")
                    print(f"           [作者]: {quote_author}")
                    print(f"           [標籤]: {quote_tag}")

                    all_quotes_data.append({
                        "作者(author)": quote_author,
                        "標籤(tag)": quote_tag,
                        "格言(quote)": quote_text
                    })

        # 步驟 5：將所有收集到的資料儲存為 Excel 檔案
        if all_quotes_data:
            excel_path = Path(__file__).parent / "data" / "quotes_search_data.xlsx"
            excel_path.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(all_quotes_data)
            df.to_excel(excel_path, index=False)
            print(f"\n==================================================")
            print(f"任務完成！共抓取 {len(all_quotes_data)} 筆格言資料，已儲存至 '{excel_path}'")

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
