from apiflask import APIFlask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api.config import DevConfig

authorizations = {
    "jwt_access_token": {"type": "apiKey", "in": "header", "name": "Authorization"},
    "jwt_refresh_token": {
        "type": "apiKey",
        "in": "cookie",
        "name": "refresh_token_cookie",
    },
}
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS(supports_credentials=True)


def create_app(config):
    app = APIFlask(__name__, title="City Report API", docs_path="/")
    app.security_schemes = authorizations
    cors.init_app(app)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from api import models  # noqa
    from api.routes import register_routes

    register_routes(app)
    return app


if __name__ == "__main__":
    app = create_app(DevConfig)

    app.run(debug=True, port=5000, ssl_context="adhoc")
