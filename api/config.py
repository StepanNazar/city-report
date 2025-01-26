import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
        minutes=os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES") or 15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(
        days=os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS") or 30)
    JWT_TOKEN_LOCATION = ["cookies", "headers"]


class DevConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    pass


class ProdConfig(Config):
    JWT_COOKIE_SECURE = True

