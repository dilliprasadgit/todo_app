from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db
from utils import get_loggedin_user

templates=Jinja2Templates(directory="templates")


router = APIRouter()

@router.get('/tasks/{task_id}')
def show_edit_task(request: Request, task_id: int):
    if get_loggedin_user(request):
        result = db.table('tasks').select('*').eq('id', task_id).execute()

        if result.data:
            return templates.TemplateResponse("edit_task.html", {
                "request": request,
                "task": result.data[0]
            })

    return RedirectResponse('/login', status_code=303)


@router.post('/task/{task_id}')
def update_task(request:Request,task_id,taskTitle=Form(...),taskDescription=Form(...),status=Form(...)):
    if get_loggedin_user(request):
        result=db.table("tasks").update({
            'title':taskTitle,
            'description':taskDescription,
            'status':status
        }).eq('id',int(task_id)).execute()
        if result.data:
            return templates.TemplateResponse("edit_task_successfully.html",{"request":request})
    return RedirectResponse('/login', status_code=303)



