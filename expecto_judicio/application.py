# encoding=utf-8
# importing packages and classes
from flask import Flask

from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


# calling the required classes
login_manager = LoginManager()
bcrypt_ = Bcrypt()
db = SQLAlchemy()


def create_app():
    # starting the application
    app = Flask(__name__)

    # Configure the app
    app.config.from_object('expecto_judicio.config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt_.init_app(app)

    return app
