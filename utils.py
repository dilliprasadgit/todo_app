
from fastapi import Request
from src.config.db import db


def get_loggedin_user(request:Request):
    token=request.cookies.get('user_session')
    if token:
        result=db.auth.get_user(token)
        if result:
            return result.user