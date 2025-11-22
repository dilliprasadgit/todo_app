from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.config.db import db

templates=Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/signup")
def show_signup_page(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@router.post("/signup")
def login_user(request:Request , email=Form(...),password=Form(...)):
    result=db.auth.sign_up({
        "email":email,
        "password":password
    })
    if result:
        return RedirectResponse('/login')

@router.get('/')
def home():
    return RedirectResponse('/login')


@router.get("/login")
def show_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})


@router.post("/login")
def login_user(request:Request , email=Form(...),password=Form(...)):
    result=db.auth.sign_in_with_password({
        "email":email,
        "password":password
    })

    if result.session.access_token:
        response=RedirectResponse('/dashboard',status_code=303)
        response.set_cookie(key="user_session", value=result.session.access_token,max_age=3600)
        return response
   