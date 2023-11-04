import os
import jwt
from flask import request
from functools import wraps
from app import app


def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing!"}, 403
        token = token.replace("Bearer ", "")
        print(token)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except BaseException as e:
            print(e)
            return {"message": "Token is invalid"}, 403
        return f(data=data, *args, **kwargs)

    return decorated
