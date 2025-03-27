from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Internal backend server address
BACKEND_SERVER = "http://10.128.0.6:9567"
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def display_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/insert/{content}")
async def add_new_document(content: str):
    backend_resp = requests.get(f"{BACKEND_SERVER}/insert/{content}")
    print(f"Document to insert: {content}")
    if backend_resp.status_code == 200:
        return backend_resp.json()
    return JSONResponse(status_code=backend_resp.status_code, content=backend_resp.json())


@app.get("/search/{keyword}")
async def fetch_document(keyword: str):
    backend_resp = requests.get(f"{BACKEND_SERVER}/get/{keyword}")
    print(f"Search query: {keyword}")
    if backend_resp.status_code == 200:
        return backend_resp.json()
    return JSONResponse(status_code=backend_resp.status_code, content=backend_resp.json())
