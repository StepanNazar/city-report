import os

from api import create_app
from api.blueprints.uploads.services import (
    LocalFolderStorageService,
    SupabaseStorageService,
)
from api.config import Config


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    DEBUG = False
    if (
        os.environ.get("SUPABASE_URL")
        and os.environ.get("SUPABASE_KEY")
        and os.environ.get("SUPABASE_BUCKET")
    ):
        STORAGE_SERVICE = SupabaseStorageService(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"],
            os.environ["SUPABASE_BUCKET"],
        )
    else:
        STORAGE_SERVICE = LocalFolderStorageService()
    JWT_COOKIE_CSRF_PROTECT = True


app = create_app(ProdConfig)
