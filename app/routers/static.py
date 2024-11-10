from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logger import logger

router = APIRouter()

router.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/login")
async def login_page(request: Request):
    logger.info(f'{request.headers=}')
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
