# IMPORT SECTION
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():

    # App object area
    app = Flask(__name__)

    # App configuartion area
    app.config.from_object("config.app_config")

    # DB object area
    db.init_app(app)

    # Schema area
    ma.init_app(app)

    # commands
    from commands import db_commands
    app.register_blueprint(db_commands)


    #import controllers and activate blueprints
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app