from fastapi import FastAPI
import uvicorn  # 記得要匯入

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello!"}


# 讓檔案可以直接被 python 指令執行
if __name__ == "__main__":
    uvicorn.run("test_fast_api:app", host="127.0.0.1", port=8000, reload=True)