import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from jwt import PyJWTError

from config import DevConfig


class FixedApi(Api):
    """Fixes the issue with Flask-JWT-Extended errors handling in flask-restx.
    Without this you get 500 status codes instead of 4xx when JWT errors occur."""

    def error_router(self, original_handler, e):
        if (not isinstance(e, PyJWTError) and not isinstance(e, JWTExtendedException)
                and self._has_fr_route()):
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler
        return original_handler(e)


app = Flask(__name__)
app.config.from_object(DevConfig)
api = FixedApi(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

import routes, models  # noqa


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so, "db": db, "User": models.User}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
