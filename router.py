from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mlask import MLAsk

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse(
        name="index.html", context=context
    )


@router.get("/review")
async def review():
    message = "お前なんて大嫌いだ!!!"
    emotion_analyzer = MLAsk()
    return emotion_analyzer.analyze(message)
    