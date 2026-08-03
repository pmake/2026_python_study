以 "p6_查詢介面_post2.py" 檔案為基礎，進行以下需求修改:
我要遍歷查詢選項，取得全部的作者(author)、標籤(tag)、格言(quote)內容，這些內容包含在頁面的div.quote中，"<div class="quote">
            <span class="content">“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”</span> - 
            <span class="author">Albert Einstein</span> (<span class="tag">life</span>)
        </div>"內容，其中span.content和span.author和span.tag內容依序為格言(quote)、作者(author)和標籤(tag)。


特別提醒，初始頁面為"view-source:https://quotes.toscrape.com/filter.aspx"，選擇過作者(author)後，網址會變更為"https://quotes.toscrape.com/filter.aspx"。

以下是網頁原始碼，請分析其內容運作方式，自行完成修改需求。