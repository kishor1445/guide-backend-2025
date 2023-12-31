from .helper import UserDB
from app import mongo


class Students(UserDB):
    def __init__(self):
        super().__init__("students")

    def add(self, args, image_url, hash_pass, v_code, v_code_exp):
        self.collection.insert_one(
            {
                "reg_no": args["reg_no"],
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

    def add(self, args, img_url, hash_pass, v_code, v_code_exp):
        if self.collection.find_one({"serial_no": args["serial_no"]}):
            raise ValueError("serial_no already exists")
        self.collection.insert_one(
            {
                "first_name": args["first_name"],
                "last_name": args["last_name"],
                "emp_id": args["emp_id"],
                "serial_no": args["serial_no"],
                "designation": args["designation"],
                "domain_1": args["domain_1"],
                "domain_2": args.get("domain_2", None),
                "domain_3": args.get("domain_3", None),
                "email": args["email"],
                "avatar_filename": img_url,
                "password": hash_pass,
                "verified": False,
                "verification_code": v_code,
                "verification_code_exp": v_code_exp,
            }
        )


class Team(UserDB):
    def __init__(self):
        super().__init__("team")

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
        self.collection.insert_one(
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
                "document": {
                    "filename": args['doc_name'],
                    "file_type": args['doc_type'],
                },
                "ppt": {
                    'filename': args['ppt_name']
                },
                "rs_paper": {
                    'filename': args['rs_paper_name'],
                    'file_type': args['rs_paper_type']
                },
                "guide_form": {
                    'filename': args['guide_form_name'],
                    'file_type': args['guide_form_type']
                },
                "app_video": {
                    'filename': args['app_video_name'],
                    'file_type': args['app_video_type']
                },
                "product_video": {
                    'filename': args['product_video_name'],
                    'file_type': args['product_video_type']
                },
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
        )


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
