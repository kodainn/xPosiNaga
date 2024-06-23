from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ml.models import Model
from dotenv import load_dotenv
from json import loads
from helper import send_rakuten_review_comment_posinaga



load_dotenv('.env')

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse(
        name="index.html", context=context
    )

@router.websocket("/posinaga")
async def ws(websocket: WebSocket, model = Depends(Model)):
    await websocket.accept()
    while True:
        client_message = await websocket.receive_text()
        start_server_message = {"action": "start", "message": ""}
        await websocket.send_json(start_server_message)
        client_message_decode = loads(client_message)
        if client_message_decode["action"] == "start":
            await send_rakuten_review_comment_posinaga(client_message_decode["search_text"], model, websocket)
        
        end_server_message = {"action": "end", "message": ""}
        await websocket.send_json(end_server_message)
        
                