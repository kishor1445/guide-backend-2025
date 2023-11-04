import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/guide_selection'
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# mail
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

mongo = PyMongo(app)
mail = Mail(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
