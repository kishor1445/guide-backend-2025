import os

from flask import request, make_response, jsonify
from flask_restful import Resource
import jwt
import datetime


class Login(Resource):
    def get(self):
        auth = request.authorization

        if auth and auth.username == "kishor" and auth.password == "password":
            token = jwt.encode(
                {
                    "user": auth.username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                os.getenv("SECRET_KEY"),
                algorithm="HS256",
            )
            return jsonify({"token": token})

        return make_response(
            "Could not verify!",
            401,
            {"WWW-Authenticate": 'Basic realm-"login Required"'},
        )
