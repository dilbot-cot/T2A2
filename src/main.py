# IMPORT SECTION
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():

    # App object area
    app = Flask(__name__)

    # App configuartion area
    app.config.from_object("config.app_config")

    # DB object area
    db = SQLAlchemy(app)

    return app