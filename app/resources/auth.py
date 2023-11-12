import secrets
import time
from datetime import datetime, timedelta
from flask import make_response, jsonify, request
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
from app.models.models import Students, Guides
from app.modules.parser import parse_arg
from app import bcrypt, mail, app
from werkzeug.datastructures.file_storage import FileStorage

guide_req = parse_arg((("guide", bool, True, []),))
reg_post_args_list = (
    ("first_name", str, True, []),
    ("last_name", str, True, []),
    ("email", str, True, []),
    ("password", str, True, []),
    ("confirm_password", str, True, []),
    ("guide", bool, True, []),
)
register_post_args = parse_arg(reg_post_args_list)
guide_reg_post_args_list = (
    ("first_name", str, True, []),
    ("last_name", str, True, []),
    ("emp_id", str, True, []),
    ("serial_no", str, True, []),
    ("designation", str, True, []),
    ("domain_1", str, True, []),
    ("domain_2", str, True, []),
    ("domain_3", str, True, []),
    ("email", str, True, []),
    ("my_image", FileStorage, True, ["file"]),
)
guide_reg_post_args = parse_arg(guide_reg_post_args_list)
login_post_args_list = (
    ("email", str, True, []),
    ("password", str, True, []),
    ("guide", bool, True, []),
)
login_post_args = parse_arg(login_post_args_list)
verify_post_args_list = (
    ("email", str, True, []),
    ("password", str, True, []),
    ("v_code", str, True, []),
    ("guide", bool, True, [])
)
verify_post_args = parse_arg(verify_post_args_list)
reset_pass_post_args_list = (
    ("password", str, True, []),
    ("new_password", str, True, []),
    ("guide", bool, True, [])
)
reset_pass_post_args = parse_arg(reset_pass_post_args_list)
forgot_pass_post_args = parse_arg((("email", str, True, []), ("guide", bool, True, [])))


class Login(Resource):
    def __init__(self):
        self.students = Students()
        self.guides = Guides()

    def post(self):
        args = login_post_args.parse_args()
        if args['guide']:
            acc = self.guides.find_by_email(args["email"])
        else:
            acc = self.students.find_by_email(args["email"])
        if acc and bcrypt.check_password_hash(acc["password"], args["password"]):
            if acc["verified"]:
                access_token = create_access_token(
                    identity=f"{args['email']}{1 if args['guide'] else 0}", expires_delta=timedelta(hours=5)
                )
                return jsonify({"access_token": access_token})
            else:
                abort(403, message="Account Verification Required")

        return make_response(jsonify({"message": "Invalid Credentials"}), 400)


class Register(Resource):
    def __init__(self):
        self.students = Students()
        self.guides = Guides()
        self.current = None

    def post(self):
        is_guide = guide_req.parse_args()["guide"]
        if is_guide:
            args = guide_reg_post_args.parse_args()
            self.current = self.guides
        else:
            args = register_post_args.parse_args()
            self.current = self.students

        # Checks
        mail_domain = args["email"].split("@")[1]
        accepted_domains = ("gmail.com", "yahoo.in", "hotmail.com")
        allowed_special_char = r"!@#$%^&()_+{}:;[]|<>,\.?~/"
        if mail_domain not in accepted_domains:
            abort(400, message="Only gmail.com, yahoo.in or hotmail.com is accepted.")
        if not args["password"] == args["confirm_password"]:
            abort(400, message="Password and Confirm Password not matching.")
        if len(args["password"]) < 8:
            abort(400, message="Password length must be at least 8 character.")
        if not any(ch.isdigit() for ch in args["password"]):
            abort(400, message="Password must contain at least 1 digit.")
        if not any(ch in allowed_special_char for ch in args["password"]):
            abort(400, message="Password must contain at least 1 special character.")

        # Checks for existing user account
        if is_guide:
            acc = self.guides.find_by_email(args["email"])
        else:
            acc = self.students.find_by_email(args["email"])
        if acc:
            abort(400, message="Email ID already registered.")

        h_pass = bcrypt.generate_password_hash(args["password"]).decode("utf-8")
        verification_code = secrets.token_urlsafe(5)
        msg = Message(
            "Verification Code",
            sender=app.config["MAIL_USERNAME"],
            recipients=[args["email"]],
        )
        msg.body = f"Your verification code is: {verification_code}\nThis code is valid for only 30 minutes"
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
            abort(500, message="An Error Occurred")
        self.current.add(
                args,
                h_pass,
                verification_code,
                datetime.utcnow() + timedelta(minutes=30),
            )
        return jsonify(
            {
                "message": "Account Created Successfully. An Verification Code has been sent to your Email."
            }
        )


class Verify(Resource):
    def __init__(self):
        self.current = None
        self.students = Students()
        self.guides = Guides()

    def post(self):
        args = verify_post_args.parse_args()
        if args['guide']:
            acc = self.guides.find_by_email(args['email'])
            self.current = self.guides
        else:
            acc = self.students.find_by_email(args["email"])
            self.current = self.students

        if acc and bcrypt.check_password_hash(acc["password"], args["password"]):
            if acc["verified"]:
                abort(403, message="Account Already Verified")
            if args["v_code"] == acc["verification_code"]:
                if datetime.utcnow() < acc["verification_code_exp"]:
                    self.current.verified(args["email"])
                    return jsonify({"message": "Successfully Verified"})
                else:
                    abort(403, message="Verification Code Expired")
            else:
                abort(403, message="Invalid Verification Code")
        else:
            abort(403, message="Invalid Credentials")


class ResetPass(Resource):
    def __init__(self):
        self.students = Students()
        self.guides = Guides()
        self.current = None

    @jwt_required()
    def post(self):
        args = reset_pass_post_args.parse_args()
        email = get_jwt_identity()[:-1]
        if args['guide']:
            acc = self.guides.find_by_email(email)
            self.current = self.guides
        else:
            acc = self.students.find_by_email(email)
            self.current = self.students
        if not bcrypt.check_password_hash(acc["password"], args["password"]):
            abort(403, message="Invalid Password")
        h_pass = bcrypt.generate_password_hash(args["new_password"]).decode("utf-8")

        self.current.update_pass(email, h_pass)
        return jsonify(message="Password Updated Successfully")

    def get(self):
        token = request.args.get("token")
        if not token:
            abort(403, message="Missing Reset Token")
        acc = self.students.find({"reset_token": token})
        self.current = self.students
        if not acc:
            self.guides.find({"reset_token": token})
            self.current = self.guides
        if not acc:
            abort(403, message="Invalid Reset Token")
        user_email = acc["email"]
        h_pass = bcrypt.generate_password_hash("SIST@2025").decode("utf-8")
        self.current.update_pass(user_email, h_pass)
        self.current.remove_field(user_email, "reset_token")
        return jsonify(message="Password Updated Successfully")


class ForgotPass(Resource):
    def __init__(self):
        self.current = None
        self.students = Students()
        self.guides = Guides()

    def post(self):
        args = forgot_pass_post_args.parse_args()
        url_token = secrets.token_urlsafe()
        if args['guide']:
            acc = self.guides.find_by_email(args["email"])
            self.current = self.guides
        else:
            acc = self.students.find_by_email(args['email'])
            self.current = self.students
        if acc:
            self.current.add_field(args["email"], "reset_token", url_token)
            msg = Message(
                "Reset password",
                sender=app.config["MAIL_USERNAME"],
                recipients=[args["email"]],
            )
            msg.body = (
                f"Your Account Password Reset URL: {request.root_url}api/reset_password?token={url_token}\n"
                f"Your New Password: SIST@2025\n"
                f"NOTE: We recommend you to change your password when you login to your account."
            )
            mail.send(msg)
        else:
            time.sleep(4)  # To prevent time based account enumeration attack
        return jsonify(
            {
                "message": "You will get reset link to your email if your account is found"
            }
        )
