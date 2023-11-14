import os
from flask import jsonify, send_file
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Students, Guides
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
from app.modules.secure import allowed_image_file
from app.modules.parser import parse_arg
from app import app


file_arg_list = (
    ("file", FileStorage, True, "files"),
    ("email", str, True, ["form"]),
)
file_arg = parse_arg(file_arg_list)


class GetInfo(Resource):
    def __init__(self):
        self.students = Students()
        self.guides = Guides()

    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        email, guide = jwt_identity[:-1], int(jwt_identity[-1])
        if guide:
            acc = self.guides.find_by_email(email)
        else:
            acc = self.students.find_by_email(email)
        if acc is None:
            abort(403, message="Account Not Found")
        # Remove Unnecessary/Sensitive info
        for v in ('password', '_id'):
            acc.pop(v)
        return jsonify(
            acc
        )


class IsGuide(Resource):
    def __init__(self):
        self.guides = Guides()

    @jwt_required()
    def get(self):
        email = get_jwt_identity()[:-1]
        acc = self.guides.find_by_email(email)
        return True if acc else False


class Avatar(Resource):

    @jwt_required()
    def get(self, _id):
        filename = secure_filename(_id)
        if not allowed_image_file(filename):
            abort(400, message="The given file extension is not allowed")
        avatar_path = os.path.abspath(os.path.join(app.config["GUIDE_AVATAR_UPLOAD"], filename))
        if not os.path.exists(avatar_path):
            abort(404, message="Avatar not found")
        return send_file(avatar_path)


class ProjectDetails1(Resource):
    def post(self):
        ...