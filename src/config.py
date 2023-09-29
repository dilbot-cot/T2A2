import os

class Config(object):
    # accesses the .env file to get the SECRET KEY value
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # accesses the .env fileto get the DATABASE URL
        value = os.environ.get("DATABASE_URL")
        if not value:
            raise ValueError("DATABSE_URL is not defined")
        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True

# access the flaskenv file to work out what state the app is in and run the appropriate Config.
environment = os.environ.get("FLASK_ENV")
if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()