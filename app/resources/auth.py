import secrets
from datetime import datetime, timedelta
from flask import make_response, jsonify
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
from app.models.users import Users
from app.modules.parser import parse_arg
from app import bcrypt, mail, app


reg_post_args_list = (
    ("first_name", str),
    ("last_name", str),
    ("email", str),
    ("password", str),
    ("confirm_password", str),
    ("guide", bool)
)
register_post_args = parse_arg(reg_post_args_list)
login_post_args_list = (
    ("email", str),
    ("password", str)
)
login_post_args = parse_arg(login_post_args_list)
verify_post_args_list = (
    ("v_code", str),
)
verify_post_args = parse_arg(verify_post_args_list)


class Login(Resource):
    def __init__(self):
        self.users = Users()

    def post(self):
        args = login_post_args.parse_args()
        user = self.users.find(args["email"])
        if user and bcrypt.check_password_hash(user["password"], args["password"]):
            access_token = create_access_token(identity=args['email'])
            return jsonify({"access_token": access_token})

        return make_response(jsonify({"message": "Invalid Credentials"}), 400)


class Register(Resource):
    def __init__(self):
        self.users = Users()

    def post(self):
        args = register_post_args.parse_args()

        # Checks
        mail_domain = args["email"].split("@")[1]
        accepted_domains = ("gmail.com", "yahoo.in", "hotmail.com")
        allowed_special_char = r"!@#$%^&()_+{}:;[]|<>,\.?~/"
        if mail_domain not in accepted_domains:
            abort(400, message="Only gmail.com, yahoo.in or hotmail.com is accepted.")
        if not args['password'] == args['confirm_password']:
            abort(400, message="Password and Confirm Password not matching.")
        if len(args['password']) < 8:
            abort(400, message="Password length must be at least 8 character.")
        if not any(ch.isdigit() for ch in args['password']):
            abort(400, message="Password must contain at least 1 digit.")
        if not any(ch in allowed_special_char for ch in args['password']):
            abort(400, message="Password must contain at least 1 special character.")

        # Checks for existing user account
        user = self.users.find(args['email'])
        if user:
            abort(400, message="Email ID already registered.")

        h_pass = bcrypt.generate_password_hash(args["password"]).decode('utf-8')
        verification_code = secrets.token_urlsafe(5)
        msg = Message('Verification Code', sender=app.config['MAIL_USERNAME'], recipients=[args['email']])
        msg.body = f'Your verification code is: {verification_code}'
        print("Verification Code Generated:", verification_code)
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
            abort(500, message="An Error Occurred")
        self.users.add(args, h_pass, verification_code, datetime.utcnow() + timedelta(minutes=30))
        return jsonify({"message": "Account Created Successfully. An Verification Code has been sent to your Email."})


class Verify(Resource):
    def __init__(self):
        self.users = Users()

    @jwt_required()
    def post(self):
        args = verify_post_args.parse_args()
        user_email = get_jwt_identity()
        user = self.users.find(user_email)
        if args["v_code"] == user["verification_code"]:
            if datetime.utcnow() < user["verification_code_exp"]:
                self.users.verified(user_email)
                return jsonify({"message": "Successfully Verified"})
            else:
                abort(403, message="Verification Code Expired")
        else:
            abort(403, message="Invalid Verification Code")

