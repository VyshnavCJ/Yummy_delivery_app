from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

from dotenv import load_dotenv
load_dotenv()

import os

url = os.environ.get("MONGO_URL")

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
     "host": url
}
app.config['SECRET_KEY'] = 'b7a0786c03e7158170cdf7b9'
db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
