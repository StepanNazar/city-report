from apiflask import APIFlask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
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

    from api import models  # noqa
    from api.routes import register_routes

    register_routes(app)
    return app


if __name__ == "__main__":
    app = create_app(DevConfig)

    app.run(debug=True, port=5000, ssl_context="adhoc")
