# IMPORT SECTION
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():

    # App object area
    app = Flask(__name__)

    # App configuration area
    app.config.from_object("config.app_config")

    # DB object area
    db.init_app(app)

    # Schema area
    ma.init_app(app)

    # JWT and bcrypt area for authentication
    bcrypt.init_app(app)
    jwt.init_app(app)

    # CLI commands area
    from commands import db_commands
    app.register_blueprint(db_commands)

    #import controllers and activate blueprints
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app