from flask_restful import Resource, reqparse, abort

register_post_args = reqparse.RequestParser()
reg_post_args_list = [
    ("first_name", str),
    ("last_name", str),
    ("email", str),
    ("password", str),
    ("confirm_password", str),
]
for x in reg_post_args_list:
    register_post_args.add_argument(
        x[0], type=x[1], help=f"{x[0]} is Required", required=True
    )


class Register(Resource):
    def post(self):
        args = register_post_args.parse_args()

        # Checks
        mail_domain = args["email"].split("@")[1]
        accepted_domains = ("gmail.com", "yahoo.in", "hotmail.com")
        allowed_special_char = r"!@#$%^&()_+{}:;[]|<>,\.?~/"
        if not mail_domain in accepted_domains:
            abort(400, "Only gmail.com, yahoo.in or hotmail.com is accepted.")
        if not args['password'] == args['confirm_password']:
            abort(400, "Password and Confirm Password not matching.")
        if len(args['password']) < 8:
            abort(400, "Password length must be at least 8 character.")
        if not any(ch.isdigit() for ch in args['password']):
            abort(400, "Password must contain at least 1 digit.")
        if not any(ch in allowed_special_char for ch in args['password']):
            abort(400, "Password must contain at least 1 special character.")

        # NOTE: Checks for existing user account
        # END

        # NOTE: Email Verification
        # END

