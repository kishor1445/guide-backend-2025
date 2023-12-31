from flask import Blueprint
from flask_restful import Api
from .resources.auth import Login, Register, Verify, ResetPass, ForgotPass
from .resources.user import GetInfo, IsGuide, Avatar

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Verify, "/verify")
api.add_resource(ResetPass, "/reset_password")
api.add_resource(ForgotPass, "/forgot_password")

api.add_resource(GetInfo, "/get_info")
api.add_resource(IsGuide, "/is_guide")
api.add_resource(Avatar, '/avatar/<_id>')



def create_app():
    from app import app

    app.register_blueprint(api_bp, url_prefix="/api")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
