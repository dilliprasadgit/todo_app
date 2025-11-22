from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db
from utils import get_loggedin_user

templates=Jinja2Templates(directory="templates")


router = APIRouter()



@router.get('/details/delete/{details_id}')
def delete_details(request: Request, details_id: int):
    user = get_loggedin_user(request)
    if user:
        db.table('tasks').delete().eq('id', details_id).execute()
        return RedirectResponse('/dashboard', status_code=303)

    return RedirectResponse('/login', status_code=303)
