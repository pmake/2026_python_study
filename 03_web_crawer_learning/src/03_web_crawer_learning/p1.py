import re
import requests
from bs4 import BeautifulSoup

def main():
    # 步驟 1：設定目標網址 (URL)
    url = "https://www.ruten.com.tw/item/22013381765312/"

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

        # 使用文字搜尋（使用正則表達式進行文字比對，不使用 CSS Selector）
        target_keyword = "RT.context"
        
        # 搜尋 HTML 中所有包含關鍵字的文字節點
        # re.compile(target_keyword): 將字串編譯為正則表達式物件，使 string 參數能進行包含比對（模糊比對）
        matched_nodes = soup.find_all(string=re.compile(target_keyword))
        
        # 方法 2：使用 map(str.strip, ...) 對每個節點只執行 1 次去除前後空白/換行，再由 if s 過濾掉無效空字串
        target_texts = [s for s in map(str.strip, matched_nodes) if s]
        if target_texts:
            print(f"找到 {len(target_texts)} 個包含 '{target_keyword}' 的文字內容：{target_texts}")
        else:
            print(f"未找到包含 '{target_keyword}' 的文字內容")

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
