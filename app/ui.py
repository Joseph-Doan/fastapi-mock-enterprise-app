from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.data.store import devices_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password":
        return RedirectResponse(url="/devices", status_code=302)
    return RedirectResponse(url="/", status_code=302)


@router.get("/devices", response_class=HTMLResponse)
def devices_page(request: Request):
    return templates.TemplateResponse(
        "devices.html",
        {"request": request, "devices": devices_db},
    )
