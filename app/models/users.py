from app import mongo


class Users:
    def __init__(self):
        self.collection = mongo.db.users

    def find(self, query):
        return self.collection.find_one(query)

    def add(self, args, hash_pass):
        self.collection.insert_one({
            "email": args["email"],
            "first_name": args["first_name"],
            "last_name": args["last_name"],
            "password": hash_pass,
            "guide": args["guide"]
        })

