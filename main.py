from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import router

app = FastAPI()

# 静的フォルダの設定
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)