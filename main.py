from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model import get_bot_response
from database import log_chat

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat": []})

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    bot_response = get_bot_response(user_input)
    log_chat(user_input, bot_response)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat": [{"user": user_input, "bot": bot_response}]
    })
