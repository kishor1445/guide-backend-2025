from flask_restful import reqparse


def parse_arg(args: tuple):
    arg_p = reqparse.RequestParser()
    for arg in args:
        arg_p.add_argument(
            arg[0], type=arg[1], help=f"{arg[0]} is Required", required=arg[2]
        )
    return arg_p
