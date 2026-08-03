import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def main():
    # 步驟 1：設定目標網址 (URL)
    url = "https://search.books.com.tw/search/query/key/python/cat/all"

    # 步驟 2：設定請求標頭 (Headers)
    # 模仿常見瀏覽器的 User-Agent，避免被伺服器誤判為惡意爬蟲擋下
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 步驟 3：設定查詢參數 (Query Parameters)
    # 網址後方附帶的參數，例如 https://httpbin.org/get?name=Python&type=crawler
    params = {
        "name": "Python",
        "type": "crawler"
    }

    try:
        # 步驟 4：發送 GET 請求
        # 設定 timeout=10 防止請求無限等待阻塞程序
        print(f"正在發送請求至：{url} ...")
        response = requests.get(url, headers=headers, params=params, timeout=10)

        # 步驟 5：檢查 HTTP 回應狀態碼
        # 若狀態碼為 4xx 或 5xx，raise_for_status() 會主動引發 HTTPError 異常
        response.raise_for_status()
        print(f"請求成功！HTTP 狀態碼：{response.status_code}\n")

        # 步驟 6：設定或確認編碼機制
        # requests 會根據 Header 自動推斷編碼，亦可手動調整為 utf-8
        response.encoding = "utf-8"

        # 步驟 7：取得並處理回應資料
        # 7a. 取得文字格式的回應內容 (response.text)
        print("=== 回應文字內容 ===")
        print(response.text[:200])  # 印出前 200 個字元

        # 7b. 使用 BeautifulSoup4 與 lxml 解析 HTML
        print("\n=== 使用 BeautifulSoup4 + lxml 解析 HTML ===")
        soup = BeautifulSoup(response.text, "lxml")

        # CSS 定位選擇器（移除原本限定單一項目的 :nth-child(4)，改為匹配所有 li 下的 div.item-info）
        css_selector = "div.table-searchbox div.mod2.table-container > div:first-child.table-tr div.table-td"
        
        # 使用 select() 進行多元素搜尋，回傳所有符合條件的元素列表
        target_elements = soup.select(css_selector)
        if target_elements:
            print(f"共找到 {len(target_elements)} 個目標元素：\n")
            books_data = []
            for idx, elem in enumerate(target_elements, 1):
                # 1. 取得商品名稱 (.prod-name)
                prod_name_node = elem.select_one("h4")
                prod_name = prod_name_node.get_text(strip=True) if prod_name_node else "無商品名稱"

                # 2. 取得折扣 (.prod-price)
                prod_discount_node = elem.select_one("li b:nth-child(1)")
                prod_discount = prod_discount_node.get_text(strip=True) if prod_discount_node else "無折扣資訊"

                # 3. 取得商品價格 (.prod-price)
                prod_price_node = elem.select_one("li b:nth-child(2)")
                prod_price = prod_price_node.get_text(strip=True) if prod_price_node else "無價格資訊"


                print(f"[{idx}] 品名: {prod_name} | 折扣: {prod_discount} | 折扣後價格: {prod_price}")
                
                # 收集資料
                books_data.append({
                    "商品名稱": prod_name,
                    "商品折扣": prod_discount,
                    "商品折扣後價格": prod_price
                })

            # 步驟 8：將資料儲存為 Excel 檔案 ('books_with_prices.xlsx')
            excel_path = Path("./03_web_crawer_learning/src/03_web_crawer_learning/data/books_with_prices.xlsx")
            # 若資料夾不存在則自動建立 (包含所有父層目錄)
            excel_path.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(books_data)
            df.to_excel(excel_path, index=False)
            print(f"\n成功將 {len(books_data)} 筆書籍資料儲存至 '{excel_path}'！")
        else:
            print("未找到目標元素 (請確認 HTML 結構或選擇器是否符合回應內容)")

        # 7c. 若回應內容為 JSON 格式，可解析為 Python dict (response.json())
        if "application/json" in response.headers.get("Content-Type", ""):
            print("\n=== 解析 JSON 資料 ===")
            json_data = response.json()
            print(f"發送者 IP (origin): {json_data.get('origin')}")
            print(f"傳入參數 (args): {json_data.get('args')}")
            print(f"使用的 User-Agent: {json_data.get('headers', {}).get('User-Agent')}")

    # 步驟 8：異常處理 (Exception Handling)
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
