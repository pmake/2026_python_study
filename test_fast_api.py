from fastapi import FastAPI
import uvicorn  # 記得要匯入

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Helloaa!"}


@app.get('/hello/{name}')
async def hello(name: str):
    return {"message": name}

@app.get('/item/')
async def get_item(limit: int = 3):
    return {}
    items = ['book1', 'book2', 'book3']
    return {'items': items[:limit]}



# 讓檔案可以直接被 python 指令執行
if __name__ == "__main__":
    uvicorn.run("test_fast_api:app", host="127.0.0.1", port=8000, reload=True)