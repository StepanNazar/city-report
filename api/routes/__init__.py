from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

from api import api
from .auth import auth
from .posts import posts

api.add_namespace(posts)
api.add_namespace(auth)


@api.errorhandler(PyJWTError)
@api.errorhandler(JWTExtendedException)
def handle_jwt_errors(error):
    return {'message': str(error)}, 401
