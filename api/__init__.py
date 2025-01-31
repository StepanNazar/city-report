import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from api.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
authorizations = {
    'jwt_access_token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'jwt_refresh_token': {
        'type': 'apiKey',
        'in': 'cookie',
        'name': 'refresh_token_cookie'
    }
}
api = Api(app, validate=True, authorizations=authorizations, security='jwt_access_token')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from api import models, routes  # noqa


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
