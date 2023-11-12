from app import mongo


class UserDB:
    def __init__(self, collection):
        self.collection = mongo.db[collection]

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def find(self, query):
        return self.collection.find_one(query)

    def verified(self, email):
        email = {"email": email}
        update = {
            "$unset": {
                "verification_code": "",
                "verification_code_exp": "",
            },
            "$set": {"verified": True},
        }
        self.collection.update_one(email, update)

    def update_pass(self, email, new_pass):
        email = {"email": email}
        update = {"$set": {"password": new_pass}}
        self.collection.update_one(email, update)

    def add_field(self, email, key, value):
        email = {"email": email}
        update = {
            "$set": {
                key: value,
            }
        }
        self.collection.update_one(email, update)

    def remove_field(self, email, key):
        email = {"email": email}
        update = {"$unset": {key: ""}}
        self.collection.update_one(email, update)
