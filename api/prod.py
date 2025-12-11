import os

from api import create_app
from api.blueprints.uploads.services import LocalFolderStorageService
from api.config import Config


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    DEBUG = False
    STORAGE_SERVICE = LocalFolderStorageService()
    JWT_COOKIE_CSRF_PROTECT = True


app = create_app(ProdConfig)
