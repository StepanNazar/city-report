from apiflask import APIFlask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jwt import PyJWTError
from sqlalchemy import MetaData

from api.config import DevConfig

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

    from api.blueprints.admin import admin
    from api.blueprints.ai_comments import ai_comments
    from api.blueprints.auth import auth
    from api.blueprints.comments import comments
    from api.blueprints.locations import locations
    from api.blueprints.posts import posts
    from api.blueprints.solutions import solutions
    from api.blueprints.uploads import uploads
    from api.blueprints.users import users

    app.security_schemes = authorizations
    app.register_blueprint(admin)
    app.register_blueprint(ai_comments)
    app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(locations)
    app.register_blueprint(posts)
    app.register_blueprint(solutions)
    app.register_blueprint(uploads)
    app.register_blueprint(users)


db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
jwt = JWTManager()


def create_app(config):
    app = APIFlask(__name__, title="City Report API", docs_path="/")

    if hasattr(config, "CORS_ORIGINS"):
        CORS(app, supports_credentials=True, origins=config.CORS_ORIGINS)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    @app.errorhandler(PyJWTError)
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(error):
        return {"message": str(error)}, 401

    return app


if __name__ == "__main__":
    app = create_app(DevConfig)

    app.run(debug=True, port=5000, ssl_context="adhoc")
