以 @p5_查詢介面_post.py 檔案為基礎，修改為:
尋找頁面中"select#author"元素，底下會有多個"option"元素，代表作者(author)。
頁面中還有一個"select#tag"元素，底下會有多個"option"元素，對應所選作者的tag標籤。每次選擇不同作者選項時，頁面就會更新，同時底下的""select#tag"內容會依據所選作者變化。
選擇"select#tag"中的不同tag時，頁面不會更新，但點擊"input.btn.btn-default"按鈕時，頁面就會更新並新增對應的"div.quote"元素，"div.quote"元素可能有1個以上。
"div.quote"底下會有3個"span"，依序是"quote", "author", "tag"。

現在我需要遍歷所有author select選項，以及對應的每個select tag，並抓取每個配對其下的所有"div.quote"內容。

主網址為"https://quotes.toscrape.com/search.aspx"
只要有選擇任一"select#author"底下的選擇，頁面就會更新並變更為"https://quotes.toscrape.com/filter.aspx"，並且會重置"select#tag"元素的selected選項為預設選項(空白)。
只有在"select#author"和"select#tag"都有有效選項時點擊"input.btn.btn-default"按鈕才會取得包含"div.quote"的頁面

請開始修改。