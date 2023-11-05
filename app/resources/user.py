from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users import Users


class GetUser(Resource):
    def __init__(self):
        self.users = Users()

    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()
        user = self.users.find_by_email(user_email)
        return jsonify({
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "guide": user["guide"]
        })
