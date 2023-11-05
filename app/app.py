from flask import Blueprint
from flask_restful import Api
from .resources.auth import Login, Register, Verify
from .resources.user import GetUser

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Verify, '/verify')

api.add_resource(GetUser, '/getuser')


def create_app():
    from app import app
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
