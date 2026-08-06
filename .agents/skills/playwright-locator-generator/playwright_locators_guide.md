# Playwright 元素定位器最佳實作與常見陷阱指南

本指南匯整 Playwright 動態爬蟲與自動化測試中，關於**元素定位器（Locators）**的優先順序、常見誤區、隱藏元素處理及實戰經驗法則。

---

## 1. 🏆 定位器優先順序與最佳實作 (Locators Priority)

Playwright 官方建議**優先使用「使用者可感知（User-facing）」的特徵**來定位元素。這樣當網頁的內部 CSS 或 HTML 結構重構時，自動化指令最不易失效。

| 優先順序 | 定位器方法 | 適用場景與優勢 | 範例 |
| :--- | :--- | :--- | :--- |
| **🥇 第 1 順位** | `get_by_role()` | **官方首選**。同時驗證元件角色與名稱，最符合網頁語意與無障礙標準，抗改版能力最強。 | `page.get_by_role("button", name="送出")`<br>`page.get_by_role("checkbox", name="華南投顧.pdf")` |
| **🥈 第 2 順位** | `get_by_text(..., exact=True)` | 使用者直接看到的純文字。建議加上 `exact=True` 避免模糊比對造成衝突。 | `page.get_by_text("Chat", exact=True)` |
| **🥉 第 3 順位** | `get_by_placeholder()` / `get_by_label()` | 輸入框或表單元件的首選。直接對應輸入框內的提示文字或 `aria-label`。 | `page.get_by_placeholder("Ask a question...")`<br>`page.get_by_label("使用者帳號")` |
| **備用選擇** | `locator('css_or_xpath')` | 用於定位無語意文字、無 Role 的特殊屬性或隱藏元件（如 `<input type="file">`）。 | `page.locator('input[name="Filedata"]')` |
| **⚠️ 避免使用** | `.first` / `.nth(0)` | **Anti-pattern（反模式）**。盲目取第一個匹配項，版面稍有微調極易點錯。 | `page.get_by_text("Chat").first` （不推薦） |

---

## 2. 💡 觀念澄清：`get_by_role` 中的 `name` 參數

在執行 `page.get_by_role("checkbox", name="檔名.pdf")` 時，許多初學者會發現 HTML 標籤內根本沒有 `name="..."` 屬性。

### 核心觀念：此 `name` 非彼 `name`
* **HTML `name="..."` 屬性**：後端表單提交的欄位 key（例如 `<input name="Filedata">`）。
* **Playwright `name="..."` 參數**：指 W3C ARIA 規範中的 **「Accessible Name（無障礙名稱）」**。

### 瀏覽器如何計算 Accessible Name？
瀏覽器會依序檢查以下來源作為元件的名稱：
1. **`aria-label` 屬性（優先度最高！）** 👈 例：`<input type="checkbox" aria-label="華南投顧.pdf">`
2. **`<label>` 標籤文字**
3. **元件內部的純文字**（例如 `<button>點我</button>`）
4. **`aria-labelledby` 所引用的元素**

---

## 3. 📁 隱藏元素與檔案上傳 (`<input type="file">`) 處理

網頁中的檔案上傳框通常會被設置 `display: none` 或 `aria-hidden="true"` 並用自訂按鈕遮蓋。

### 處理原則
```html
<input type="file" name="Filedata" aria-hidden="true" style="display: none;">
```

1. **不能使用 `get_by_role()`**：因為 `aria-hidden="true"` 的元素預設會被無障礙樹忽略。
2. **定位方式**：使用固定且具備唯一性的屬性定位器：
   ```python
   file_input = page.locator('input[name="Filedata"]')
   ```
3. **等待機制**：使用 `state="attached"`，**切勿使用 `state="visible"`**（隱藏元件永遠不會 visible）：
   ```python
   file_input.wait_for(state="attached")
   ```
4. **上傳檔案**：直接呼叫 `.set_input_files()`，**不需要先對畫面按鈕執行 `hover()` 或 `click()`**：
   ```python
   file_input.set_input_files("path/to/file.pdf")
   ```

---

## 4. 🖱️ DOM 事件冒泡與嵌套元素點擊

### 問題：點擊被 `<button>` 包裹的 `<span>` 會觸發按鈕嗎？
```html
<button id="submit">
  <span>送出資料</span>
</button>
```

**答案：絕對會！**

1. **DOM 事件冒泡（Event Bubbling）**：點擊 `<span>` 的事件會自動向上層層傳遞至 `<button>` 並觸發其 `onclick` 事件。
2. **Playwright 物理點擊**：Playwright 的 `.click()` 會計算元素的視覺中心座標發送真實點擊。
3. **最佳寫法**：Playwright 的 `get_by_role("button", name="送出資料")` 會自動將 `<span>` 內部的文字當作按鈕的名稱，因此直接定位按鈕即可：
   ```python
   page.get_by_role("button", name="送出資料").click()
   ```

---

## 5. 🚫 嚴格模式衝突（Strict Mode Violation）與除錯

### 錯誤現象
```text
playwright._impl._errors.Error: Locator.click: Error: strict mode violation:
get_by_text("Chat") resolved to 3 elements:
  1) <div>...</div>
  2) <h2>Chat</h2>
  3) <div role="tooltip">...</div>
```

### 發生原因
Playwright 預設啟用 Strict Mode，要求定位器必須精確找到**唯一一個**元素。如果使用 `get_by_text("Chat")`，預設為模糊包含比對，會匹配到所有包含 "Chat" 字樣的子元素。

### 解決方案
* **方案 A（推薦）**：開啟精確比對
  ```python
  page.get_by_text("Chat", exact=True).click()
  ```
* **方案 B（推薦）**：結合元件角色
  ```python
  page.get_by_role("heading", name="Chat").click()
  ```

---

## 6. 🔍 需前置動作才會出現的元素處理機制 (Hover 前置需求判斷)

### 問題：浮動或前置動作出現的元素，是否一定要先寫 `.hover()`？

**解答：不一定！完全取決於元素是「早已存在 DOM 裡被隱藏」還是「Hover 後才由 JS 動態生成」。**

### 兩種網頁機制對比

| 機制 | 特徵與說明 | 是否需要 Hover？ | Playwright 處理方式 |
| :--- | :--- | :--- | :--- |
| **情況 A：元素本就在 DOM 中** | 元素早已載入 HTML 樹，僅透過 CSS (`display: none` 或 `opacity: 0`) 隱藏。常見於檔案上傳框或隱藏表單。 | ❌ **不需要 Hover** | 直接透過 DOM 選擇器操作即可：<br>`page.locator('input[name="Filedata"]').wait_for(state="attached")`<br>`page.locator('input[name="Filedata"]').set_input_files("file.pdf")` |
| **情況 B：JS 動態生成** | 滑鼠移過去時，JavaScript 才執行 `appendChild` 將 HTML 渲染出來。常見於浮動下拉選單。 | ⭕ **必須先 Hover** | 必須先觸發 Hover，讓 DOM 產生該元素後才能定位：<br>`page.get_by_text("選單").hover()`<br>`page.get_by_text("下載").click()` |

### 🛠️ 實務上如何判斷是否需要 Hover？
1. **F12 元素搜尋法**：在未懸停滑鼠前，於開發者工具 Elements 頁籤按 `Ctrl+F` (或 `Cmd+F`) 搜尋元素特徵。
   * 搜尋得到 $\rightarrow$ **免 Hover**，直接操作 DOM。
   * 搜尋不到 $\rightarrow$ **需 Hover** 觸發生成。
2. **Playwright Codegen 錄製**：執行 `playwright codegen <網址>` 自動錄製操作流程，若自動生成了 `.hover()` 則代表需要該前置動作。

---

## 7. 🎬 Playwright Codegen (自動錄製工具) 實戰全攻略

### 常用指令技巧 (使用 `uv` 與本機 Chrome)

* **使用本機 Chrome 瀏覽器（免安裝特製版 Chromium）**：
  ```bash
  uv run playwright codegen --channel=chrome <網址>
  ```
* **帶入已儲存的登入狀態 (Cookies / Session)**：
  ```bash
  uv run playwright codegen --channel=chrome --load-storage="path/to/auth_state.json" <網址>
  ```

### 工具欄介面圖示說明

當開啟 Codegen 錄製時，瀏覽器畫面上會出現一個浮動工具欄：

| 圖示 | 功能名稱 | 作用 |
| :---: | :--- | :--- |
| 🔴 | **Record (錄製)** | 點擊可暫停 / 恢復錄製 |
| ↖️ | **Pick Locator** | 用滑鼠點擊網頁元素，抓取該元素的 Locator 定位器 |
| 👁️ | **Assert Visibility** | 點擊元素加入「驗證元素是否可見」的斷言程式碼 |
| <u>ab</u> | **Assert Text** | 點擊元素加入「驗證文字內容」的斷言程式碼 |
| **`</>`** | **Code View (程式碼視窗)** | **👈 點擊開啟 Inspector 視窗以檢視與複製錄製好的程式碼** |

### 程式碼複製與結束流程

1. **查看與複製程式碼**：
   * 點擊懸浮工具欄最右側的 **`</>`** 圖示，開啟 Inspector 程式碼視窗。
   * 點擊 Inspector 右上角的 **📋 `Copy`** 按鈕（或使用鍵盤快捷鍵 `Cmd+A` $\rightarrow$ `Cmd+C`）複製內容。
2. **結束錄製**：
   * 關閉 Inspector 視窗或 Chrome 瀏覽器視窗。
   * 或在 Terminal 終端機按下 `Ctrl+C` 中斷程序。
