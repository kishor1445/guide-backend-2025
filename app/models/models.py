from .helper import UserDB
from gridfs import GridFS
from app import mongo


class Students(UserDB):
    def __init__(self):
        super().__init__("students")

    def add(self, args, hash_pass, v_code, v_code_exp):
        self.collection.insert_one(
            {
                "email": args["email"],
                "first_name": args["first_name"],
                "last_name": args["last_name"],
                "password": hash_pass,
                "verified": False,
                "verification_code": v_code,
                "verification_code_exp": v_code_exp,
            }
        )


class Guides(UserDB):
    def __init__(self):
        super().__init__("guides")

    def add(self, args, hash_pass, v_code, v_code_exp):
        self.collection.insert_one(
            {
                "name": args["name"],
                "emp_id": args["emp_id"],
                "serial_no": args["serial_no"],
                "designation": args["designation"],
                "domain_1": args["domain_1"],
                "domain_2": args.get("domain_2", None),
                "domain_3": args.get("domain_3", None),
                "email": args["email"],
                "password": hash_pass,
                "verified": False,
                "verification_code": v_code,
                "verification_code_exp": v_code_exp,
            }
        )


class Team(UserDB):
    def __init__(self):
        super().__init__("team")
        self.fs = GridFS(mongo.db, "team")

    def add(self, args):
        if args.get("no_of_members", None) is None:
            no_of_members = 1
        else:
            if 1 <= args["no_of_members"] <= 2:
                no_of_members = args["no_of_members"]
            else:
                raise ValueError(
                    f"no_of_members should be either 1 or 2 but it has {args['no_of_members']}"
                )
        if args.get("type", None) is None:
            _type = "Project Type"
        elif args["type"] in ("Application Based", "Product Based"):
            _type = args["type"]
        else:
            raise ValueError(
                f"type value should be Application Based or Product Based. But got {args['type']}"
            )
        return self.collection.insert_one(
            {
                "team_id": args["team_id"],
                "project_name": args["project_name"],
                "project_domain": args["project_domain"],
                "project_description": args["project_description"],
                "no_of_members": no_of_members,
                # Members
                "reg_no_1": args["reg_no_1"],
                "student_1_name": args["student_1_name"],
                "student_1_email": args["student_1_email"],
                "student_1_no": args["student_1_no"],
                "reg_no_2": args["reg_no_2"],
                "student_2_name": args["student_2_name"],
                "student_2_email": args["student_2_email"],
                "student_2_no": args["student_2_no"],
                # Files
                # TODO: file
                "document": {
                    "filename": f"{args['team_id']}_document.pdf",
                    "file_type": "pdf",
                },
                "ppt": None,
                "rs_paper": None,
                "guide_form": None,
                "app_video": None,
                "product_video": None,
                # Approval
                "profile_approved": False,
                "guide_approved": False,
                "rs_paper_approved": False,
                "docs_approved": False,
                "ppt_approved": False,
                # Guide
                "guide": args["guide"],
                "guide_email": args["guide_email"],
                # Result
                "review_2_marks": 10,
                "review_3_marks": 10,
                "communicated": False,
                "accepted": False,
                "payment_done": False,
                "type": _type,
            }
        ).inserted_id


class Credit(UserDB):
    def __init__(self):
        super().__init__("credit")

    def add(self, args):
        self.collection.insert_one(
            {
                "name": args["name"],
                "role": args["role"],
                # TODO: img field
            }
        )
