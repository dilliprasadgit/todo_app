from fastapi import FastAPI


from src.routes.auth import router as auth_router
from src.routes.dashboard import router as dashboard_router
from src.routes.tasks import router as tasks_route
from src.routes.edit_task import router as edit_router
from src.routes.delete import router as delete_router



app=FastAPI(title="Todo App")


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(tasks_route)
app.include_router(edit_router)
app.include_router(delete_router)
