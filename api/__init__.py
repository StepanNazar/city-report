from typing import TYPE_CHECKING

from apiflask import APIFlask
from flask import current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jwt import PyJWTError
from sqlalchemy import Engine, MetaData, event

from api.config import DevConfig

if TYPE_CHECKING:
    from api.blueprints.uploads.services import StorageService

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
authorizations = {
    "jwt_access_token": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
    "jwt_refresh_token": {
        "type": "apiKey",
        "in": "cookie",
        "name": "refresh_token_cookie",
    },
    "csrf_refresh_token": {
        "type": "apiKey",
        "in": "header",
        "name": "X-CSRF-TOKEN",
    },
}


def register_routes(app):
    """Register all routes for the API."""

    from api.blueprints.admin import admin, models, routes
    from api.blueprints.ai_comments import ai_comments, models, routes  # noqa: F811
    from api.blueprints.auth import auth, models, routes  # noqa: F811
    from api.blueprints.comments import comments, models, routes  # noqa: F811
    from api.blueprints.locations import locations, models, routes  # noqa: F811
    from api.blueprints.posts import models, posts, routes  # noqa: F811
    from api.blueprints.solutions import models, routes, solutions  # noqa: F811
    from api.blueprints.uploads import models, routes, uploads_bp  # noqa: F811
    from api.blueprints.users import models, routes, users  # noqa: F401, F811

    app.security_schemes = authorizations
    app.register_blueprint(admin)
    app.register_blueprint(ai_comments)
    app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(locations)
    app.register_blueprint(posts)
    app.register_blueprint(solutions)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(users)


db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
jwt = JWTManager()


class CustomAPIFlask(APIFlask):
    storage_service: "StorageService"


def get_app() -> CustomAPIFlask:
    return current_app  # type: ignore[return-value]


def create_app(config):
    app = APIFlask(__name__, title="City Report API", docs_path="/")

    if hasattr(config, "CORS_ORIGINS"):
        CORS(app, supports_credentials=True, origins=config.CORS_ORIGINS)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    app.storage_service = config.STORAGE_SERVICE  # type: ignore[attr-defined]

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        if "sqlite" in str(dbapi_conn.__class__):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    register_routes(app)

    @app.errorhandler(PyJWTError)
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(error):
        return {"message": str(error)}, 401

    return app


if __name__ == "__main__":
    app = create_app(DevConfig)

    app.run(debug=True, port=5000, ssl_context="adhoc")
