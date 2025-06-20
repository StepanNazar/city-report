from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from api.config import DevConfig


def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    return app


authorizations = {
    "jwt_access_token": {"type": "apiKey", "in": "header", "name": "Authorization"},
    "jwt_refresh_token": {
        "type": "apiKey",
        "in": "cookie",
        "name": "refresh_token_cookie",
    },
}
api = Api(validate=True, authorizations=authorizations, security="jwt_access_token")
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

from api import models, routes  # noqa

if __name__ == "__main__":
    app = create_app(DevConfig)

    app.run(debug=True, port=5000, ssl_context="adhoc")
