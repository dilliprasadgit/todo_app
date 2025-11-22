from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db
from utils import get_loggedin_user

templates=Jinja2Templates(directory="templates")


router = APIRouter()
            


@router.get("/tasks/new")
def add_new_task(request: Request):
    if get_loggedin_user(request):
        return templates.TemplateResponse("new_task.html", {"request": request})
    return RedirectResponse('/login', status_code=303)
     


@router.post("/tasks/new")
def creat_new_task(
    request: Request,
    taskTitle: str = Form(...),
    taskDescription: str = Form(...),
    status: str = Form(...)
):
    user = get_loggedin_user(request)
    if user:
        user_id = user.id
        result = db.table("tasks").insert({
            'title': taskTitle,
            'description': taskDescription,
            'status': status,
            'user_id': user_id
        }).execute()

        if result.data:
            return templates.TemplateResponse("task_success.html", {"request": request})

    return RedirectResponse('/login', status_code=303)



