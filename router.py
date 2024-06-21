from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ml.models import Model
import os
from dotenv import load_dotenv
import time
import requests
from bs4 import BeautifulSoup


load_dotenv('.env')

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse(
        name="index.html", context=context
    )


@router.get("/review")
async def review(model = Depends(Model)):
    return model.predict("よろしくお願いいたします!!!!")

@router.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        for i in range(100):
            await websocket.send_text(f"Message text was: {i}")
            time.sleep(1)


@router.get("/test")
async def teset():
    url="https://search.rakuten.co.jp/search/mall/雛人形/"
    html=requests.get(url)
    soup=BeautifulSoup(html.text,'html.parser')
    items=soup.select('.searchresultitem')
 
    n=1

    results = []
 
    for item in items:
        title=item.select_one('.title')
        price=item.select_one('.price')
        n+=1
        results.append(item)
    
    return results