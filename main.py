import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

# just for testing
# from resources.helloworld import HelloWorld, ProtectedHelloWorld
from resources.auth import Login

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# just for testing
# api.add_resource(HelloWorld, "/helloworld")
# api.add_resource(ProtectedHelloWorld, "/secret")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)
