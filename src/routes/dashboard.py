# from fastapi import APIRouter, Form, Request
# from fastapi.templating import Jinja2Templates
# from src.config.db import db
# from utils import get_loggedin_user

# templates=Jinja2Templates(directory="templates")


# router = APIRouter()



# @router.get("/dashboard")
# def show_dashboard(request:Request):
#     if get_loggedin_user(request):
#             result = db.table('tasks').select("*").execute()
#             print(result.data)
#             if result.data:
#                 return templates.TemplateResponse("dashboard.html",{'request':request,"tasks":result.data})



from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config.db import db
from utils import get_loggedin_user

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/dashboard")
def show_dashboard(request: Request):
    user = get_loggedin_user(request)

    if user:
        # get only logged-in user's tasks
        result = db.table('tasks').select("*").eq("user_id", user.id).execute()
        
        tasks = result.data if result.data else []   # avoid None / empty crash

        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "tasks": tasks}
        )

    return RedirectResponse('/login', status_code=303)
