# 第一次 FROM：引入一個裝滿強大工具（如 uv）的「建置專用」環境
FROM astral-sh/uv:python3.12.13-bookworm-slim AS builder

WORKDIR /app

# 複製設定檔並下載/安裝/編譯所有的 Python 第三方套件
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# 複製你的程式碼並在容器內的 .venv（虛擬環境）中安裝
COPY . .
RUN uv sync --frozen --no-dev

# 第二次 FROM：使用最純淨、沒有 uv、沒有雜物的官方 Python 執行環境
# 第二次 FROM 的神奇之處：一旦 Docker 執行到第二個 FROM，它會完全丟棄第一階段所產生的所有暫存層（包括 uv 執行檔本身），從頭開啟一個乾淨的新環境。

# COPY --from=builder /app /app：這是最關鍵的語法。它像是一座傳送門，只把我們在第一階段已經在 /app 內編譯好、裝好的乾淨 .venv 虛擬環境以及你的程式碼，隔空複製到這第二個新環境中。

# 結果：最終打包出來、要上傳到 Cloud Run 的 Image 裡面完全沒有 uv 軟體，也沒有編譯時的快取，只剩下精簡的 Python runtime 和安裝好的套件。
FROM python:3.12.13-slim-bookworm

WORKDIR /app

# 💡 關鍵語法：只從 builder 階段（AS builder），把「已經裝好的虛擬環境」複製過來！
COPY --from=builder /app /app

# 設定環境變數，讓系統可以直接抓到我們在第一階段裝好的套件
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


