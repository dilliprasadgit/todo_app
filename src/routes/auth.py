from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.config.db import db

templates = Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/signup")
def show_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def signup_user(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        result = db.auth.sign_up({
            "email": email,
            "password": password
        })
        if result:
            return RedirectResponse('/login', status_code=303)
    except Exception as e:
        print(f"Signup Error: {e}")
        # In a real app, you'd pass the error to the template
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Signup failed. Please try again."})

@router.get('/')
def home():
    return RedirectResponse('/login')


@router.get("/login")
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        result = db.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    
        if result.session.access_token:
            response = RedirectResponse('/dashboard', status_code=303)
            response.set_cookie(key="user_session", value=result.session.access_token, max_age=3600)
            return response
    except Exception as e:
        print(f"Login Error: {e}")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@router.get("/logout")
def logout():
    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie("user_session")
    return response
