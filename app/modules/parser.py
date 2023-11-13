from flask_restful import reqparse


def parse_arg(args: tuple):
    arg_p = reqparse.RequestParser()
    for name, arg_type, required, location in args:
        loc = location if location else ("json", "values")
        arg_p.add_argument(
            name,
            type=arg_type,
            help=f"{name} is Required",
            required=required,
            location=loc,
        )
    return arg_p
